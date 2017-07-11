#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import numpy as np

import nodefinder

@pytest.fixture
def test_name(request):
    """Returns module_name.function_name for a given test"""
    return request.module.__name__ + '/' + request._parent_request._pyfuncitem.name

@pytest.fixture
def compare_data(request, test_name, scope="session"):
    """Returns a function which either saves some data to a file or (if that file exists already) compares it to pre-existing data using a given comparison function."""
    def inner(compare_fct, data, tag=None):
        full_name = test_name + (tag or '')
        val = request.config.cache.get(full_name, None)
        if val is None:
            request.config.cache.set(full_name, json.loads(json.dumps(data, default=phasemap.io._encoding.encode)))
            raise ValueError('Reference data does not exist.')
        else:
            val = json.loads(
                json.dumps(val, default=phasemap.io._encoding.encode),
                object_hook=phasemap.io._encoding.decode
            )
            assert compare_fct(val, json.loads(
                json.dumps(data, default=phasemap.io._encoding.encode),
                object_hook=phasemap.io._encoding.decode
            )) # get rid of json-specific quirks
    return inner

@pytest.fixture
def compare_equal(compare_data):
    return lambda data, tag=None: compare_data(operator.eq, data, tag)
