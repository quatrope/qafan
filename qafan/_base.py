#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: BSD-3 (https://tldrlegal.com/license/bsd-3-clause-license-(revised))
# Copyright (c) 2022, QuatroPe
# All rights reserved.


# =============================================================================
# DOCS
# =============================================================================

"""Base functionalities for all QAFan tools"""


# =============================================================================
# IMPORTS
# =============================================================================

import inspect


import attr

import typer

from . import VERSION


# =============================================================================
# CLI
# =============================================================================

FOOTNOTE = """
This software is under the BSD 3-Clause License.
Copyright (c) 2022, QuatroPe.
For bug reporting or other instructions please check:
https://github.com/quatrope/qafan

""".strip()


@attr.s(frozen=True)
class CLIBase:
    """Base class for all QA-Fan CLI tools."""

    footnotes = FOOTNOTE

    run = attr.ib(init=False)

    @run.default
    def _set_run_default(self):
        app = typer.Typer()
        for k in dir(self):
            if k.startswith("_"):
                continue
            v = getattr(self, k)
            if inspect.ismethod(v):
                decorator = app.command()
                decorator(v)

        return app

    def version(
        self,
        ctx: typer.Context,
    ):

        cmd = ctx.command_path.split()[0]
        typer.echo(f"{cmd} v.{VERSION}")
