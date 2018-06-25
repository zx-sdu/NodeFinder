"""
Tests with a single nodal point.
"""

# pylint: disable=redefined-outer-name,unused-argument

import tempfile

import pytest
import numpy as np
import scipy.linalg as la

from nodefinder import run_node_finder
from nodefinder._minimization._fake_potential import FakePotential

NODE_PARAMETERS = pytest.mark.parametrize(
    'node_positions, mesh_size', [
        ([(0.5, 0.5, 0.5)], (1, 2, 1)),
        ([(0.2, 0.9, 0.6), (0.99, 0.01, 0.0), (0.7, 0.2, 0.8)], (3, 3, 3)),
    ]
)


@pytest.fixture
def gap_fct(node_positions):
    """
    Calculates the minimum distance between a given position and the nearest node.
    """
    node_pos_array = np.array(node_positions)

    def inner(x):
        deltas = (np.array(x) - node_pos_array) % 1
        deltas_periodic = np.minimum(deltas, 1 - deltas)
        distances = la.norm(deltas_periodic, axis=-1)
        return np.min(distances)

    return inner


@pytest.fixture(params=[None, FakePotential])
def fake_potential_class(request):
    return request.param


@NODE_PARAMETERS
def test_simple(
    gap_fct,
    node_positions,
    mesh_size,
    fake_potential_class,
    score_nodal_points,
):
    """
    Test that a single nodal point is found.
    """
    result = run_node_finder(
        gap_fct=gap_fct,
        initial_mesh_size=mesh_size,
        fake_potential_class=fake_potential_class
    )
    score_nodal_points(
        result,
        exact_points=node_positions,
        cutoff_accuracy=1e-6,
        cutoff_coverage=1e-6
    )


@NODE_PARAMETERS
def test_save(
    gap_fct, node_positions, mesh_size, fake_potential_class,
    score_nodal_points
):
    """
    Test saving to a file
    """
    with tempfile.NamedTemporaryFile() as named_file:
        result = run_node_finder(
            gap_fct=gap_fct,
            save_file=named_file.name,
            initial_mesh_size=mesh_size,
            fake_potential_class=fake_potential_class,
        )
        score_nodal_points(
            result,
            exact_points=node_positions,
            cutoff_accuracy=1e-6,
            cutoff_coverage=1e-6
        )


@NODE_PARAMETERS
def test_restart(
    gap_fct, node_positions, mesh_size, score_nodal_points,
    fake_potential_class
):
    """
    Test that the calculation is done when restarting from a finished result.
    """

    def invalid_gap_fct(x):
        raise ValueError

    with tempfile.NamedTemporaryFile() as named_file:
        result = run_node_finder(
            gap_fct=gap_fct,
            save_file=named_file.name,
            initial_mesh_size=mesh_size,
            fake_potential_class=fake_potential_class
        )
        score_nodal_points(
            result,
            exact_points=node_positions,
            cutoff_accuracy=1e-6,
            cutoff_coverage=1e-6,
            additional_tag='initial_'
        )

        restart_result = run_node_finder(
            gap_fct=invalid_gap_fct,
            save_file=named_file.name,
            load=True,
            load_quiet=False,
            initial_mesh_size=mesh_size,
            fake_potential_class=fake_potential_class
        )
        score_nodal_points(
            restart_result,
            exact_points=node_positions,
            cutoff_accuracy=1e-6,
            cutoff_coverage=1e-6,
            additional_tag='restart_'
        )
