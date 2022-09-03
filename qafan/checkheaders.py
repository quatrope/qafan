#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: BSD-3 (https://tldrlegal.com/license/bsd-3-clause-license-(revised))
# Copyright (c) 2022, QuatroPe
# All rights reserved.


# =============================================================================
# DOCS
# =============================================================================

"""Tool to check if the headers of all python files are correct."""


# =============================================================================
# IMPORTS
# =============================================================================


import pathlib
from typing import List, OrderedDict

import attr

import typer

from . import _base


# =============================================================================
# FUNCTIONS
# =============================================================================


def lines_rstrip(text):
    return "\n".join(line.rstrip() for line in text.splitlines())


def check_file_header(fpath, header_tpl):
    if not isinstance(fpath, pathlib.Path):
        fpath = pathlib.Path(fpath)

    lines = len(header_tpl.splitlines())
    with open(fpath) as fp:
        fheader = "".join(fp.readlines()[:lines])
        fheader = lines_rstrip(fheader)

    header_ok = fheader == header_tpl

    return header_ok


# =============================================================================
# CLI
# =============================================================================


@attr.s(frozen=True)
class CheckHeaders(_base.CLIBase):
    """Check if python files contain the appropriate header."""

    def check(
        self,
        sources: List[pathlib.Path] = typer.Argument(
            ..., help="Path to the test structure."
        ),
        header_template: pathlib.Path = typer.Option(
            ..., help="Path to the header template."
        ),
        verbose: bool = typer.Option(default=False, help="Show all the result"),
    ):
        """Check if python files contain the appropriate header."""

        results = OrderedDict()

        try:

            header_tpl = lines_rstrip(header_template.read_text())

            for src in sources:
                if src.is_dir():
                    for fpath in src.glob("**/*.py"):
                        results[fpath] = check_file_header(fpath, header_tpl)
                elif src.suffix in (".py",):
                    results[src] = check_file_header(src, header_tpl)
                else:
                    raise ValueError(f"Invalid file type {src.suffix}")

        except OSError as err:
            typer.echo(typer.style(str(err), fg=typer.colors.RED))
            raise typer.Exit(code=1)

        all_headers_ok = True
        for fpath, header_ok in results.items():
            if header_ok:
                fg = typer.colors.GREEN
                status = "HEADER MATCH"
            else:
                all_headers_ok = False
                fg = typer.colors.RED
                status = typer.style("HEADER DOES NOT MATCH", fg=typer.colors.YELLOW)
            if verbose or not header_ok:
                msg = f"{fpath} -> {status}"
                typer.echo(typer.style(msg, fg=fg))

        if all_headers_ok:
            final_fg = typer.colors.GREEN
            final_status = "All files has the correct header"
            exit_code = 0
        else:
            final_fg = typer.colors.RED
            final_status = "Not all headers match!"
            exit_code = 1

        typer.echo("-------------------------------------")
        typer.echo(typer.style(final_status, fg=final_fg))

        raise typer.Exit(code=exit_code)


def main():
    """Run the checkheaders.py cli interface."""
    CheckHeaders().run()


if __name__ == "__main__":
    main()
