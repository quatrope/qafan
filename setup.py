#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: BSD-3 (https://tldrlegal.com/license/bsd-3-clause-license-(revised))
# Copyright (c) 2022, QuatroPe
# All rights reserved.


# =============================================================================
# DOCS
# =============================================================================

"""This file is for distribute qafan

"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import pathlib

from setuptools import setup


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

REQUIREMENTS = ["typer"]

with open(PATH / "README.md") as fp:
    LONG_DESCRIPTION = fp.read()

DESCRIPTION = "Collection of script to improve the QA of Python project"

with open(PATH / "qafan" / "__init__.py") as fp:
    VERSION = (
        [line for line in fp.readlines() if line.startswith("__version__")][0]
        .split("=", 1)[-1]
        .strip()
        .replace('"', "")
    )


# =============================================================================
# FUNCTIONS
# =============================================================================


def do_setup():
    setup(
        name="qafan",
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        author="QuatroPe",
        author_email="jbcabral@unc.edu.ar",
        url="htthttps://github.com/quatrope/qafan",
        license="3 Clause BSD",
        keywords=["qa", "tools", "scripts"],
        classifiers=(
            "Development Status :: 4 - Beta",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Scientific/Engineering",
        ),
        packages=["qafan"],
        install_requires=REQUIREMENTS,
        entry_points={
            "console_scripts": [
                "check-testdir=qafan.checktestdir:main",
                "check-apidocsdir=qafan.checkapidocsdir:main",
                "check-headers=qafan.checkheaders:main",
            ]
        },
    )


if __name__ == "__main__":
    do_setup()
