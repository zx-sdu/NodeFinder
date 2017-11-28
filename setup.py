"""Usage: pip install .[dev]"""

import re
from setuptools import setup, find_packages

README = r"""TODO"""

with open('./nodefinder/__init__.py', 'r') as f:
    MATCH_EXPR = "__version__[^'\"]+(['\"])([^'\"]+)"
    VERSION = re.search(MATCH_EXPR, f.read()).group(2).strip()

setup(
    name='nodefinder',
    version=VERSION,
    author='Dominik Gresch, TODO',
    author_email='greschd@gmx.ch, TODO',
    description='TODO',
    install_requires=['numpy', 'scipy'],
    extras_require={
        'dev': ['pytest', 'yapf==0.20', 'pre-commit', 'prospector']
    },
    long_description=README,
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English', 'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Development Status :: 4 - Beta'
    ],
    license='GPL',
    keywords=[],
    packages=find_packages()
)
