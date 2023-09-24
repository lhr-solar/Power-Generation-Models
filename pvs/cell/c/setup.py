# !/bin/python3
# isort: skip_file
"""_summary_
"""

from setuptools import setup
from Cython.Build import cythonize

setup(
    name="three_param_cell",
    ext_modules=cythonize("three_param_cell.pyx"),
    zip_safe=False,
)
