#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: BSD-3 (https://tldrlegal.com/license/bsd-3-clause-license-(revised))
# Copyright (c) 2022, QuatroPe
# All rights reserved.


# =============================================================================
# DOCS
# =============================================================================

"""Tool to check if each python module has a corresponding test module."""

# =============================================================================
# IMPORTS
# =============================================================================

import pathlib

import attr

import typer

from . import _base


# =============================================================================
# FUNCTIONS
# =============================================================================


def check_test_structure(test_dir, reference_dir):

    test_dir = pathlib.Path(test_dir)
    reference_dir = pathlib.Path(reference_dir)

    if not test_dir.exists():
        raise OSError(f"'{test_dir}' do no exist")
    if not reference_dir.exists():
        raise OSError(f"'{reference_dir}' do no exist")

    reference = list(reference_dir.glob("**/*.py"))

    result = {}
    for ref in reference:
        if ref.name == "__init__.py":
            continue

        # essentially we remove the parent dir
        *dirs, ref_name = ref.relative_to(reference_dir).parts
        while ref_name.startswith("_"):
            ref_name = ref_name[1:]

        search_dir = test_dir
        for subdir in dirs:
            search_dir /= subdir

        search = search_dir / f"test_{ref_name}"

        result[str(ref)] = (str(search), search.exists())

    return result


# =============================================================================
# CLI
# =============================================================================


@attr.s(frozen=True)
class CheckTestDir(_base.CLIBase):
    """Check if the structure of test directory is equivalent to those of the
    project.

    """

    def check(
        self,
        test_dir: str = typer.Argument(..., help="Path to the test structure."),
        reference_dir: str = typer.Option(..., help="Path to the reference structure."),
        verbose: bool = typer.Option(default=False, help="Show all the result"),
    ):
        """Check if the structure of test directory is equivalent to those
        of the project.

        """
        try:
            check_result = check_test_structure(test_dir, reference_dir)
        except Exception as err:
            typer.echo(typer.style(str(err), fg=typer.colors.RED))
            raise typer.Exit(code=1)

        all_tests_exists = True
        for ref, test_result in check_result.items():

            test, test_exists = test_result

            if test_exists:
                fg = typer.colors.GREEN
                status = ""
            else:
                all_tests_exists = False
                fg = typer.colors.RED
                status = typer.style("[NOT FOUND]", fg=typer.colors.YELLOW)

            if verbose or not test_exists:
                msg = f"{ref} -> {test} {status}"
                typer.echo(typer.style(msg, fg=fg))

        if all_tests_exists:
            final_fg = typer.colors.GREEN
            final_status = "Test structure ok!"
            exit_code = 0
        else:
            final_fg = typer.colors.RED
            final_status = "Structure not equivalent!"
            exit_code = 1

        typer.echo("-------------------------------------")
        typer.echo(typer.style(final_status, fg=final_fg))
        raise typer.Exit(code=exit_code)


def main():
    """Run the checktestdir.py cli interface."""
    CheckTestDir().run()


if __name__ == "__main__":
    main()
