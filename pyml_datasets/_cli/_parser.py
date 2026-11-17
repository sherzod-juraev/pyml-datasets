"""The argument parser of the command line."""

import argparse
from functools import partial

from rich_argparse import RawDescriptionRichHelpFormatter

from ._commands import list_command, show_command


class _HelpFormatter(RawDescriptionRichHelpFormatter):
    """Colored help text. Nothing in it is read as rich markup."""

    help_markup = False
    text_markup = False


def build_parser() -> argparse.ArgumentParser:
    """Create the parser of the ``pyml-datasets`` command.

    Returns
    -------
    argparse.ArgumentParser
        Parser with the sub-commands ``list`` and ``show``. The function that runs the
        chosen command is stored in the ``handler`` attribute of the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog="pyml-datasets",
        description="Look up the datasets bundled with pyml-datasets.",
        formatter_class=_HelpFormatter,
        epilog="examples:\n  pyml-datasets list\n  pyml-datasets show iris",
    )
    commands = parser.add_subparsers(dest="command", metavar="COMMAND", required=True)
    add_command = partial(commands.add_parser, formatter_class=_HelpFormatter)

    listing = add_command("list", help="show a table of all datasets")
    listing.set_defaults(handler=list_command)

    show = add_command("show", help="show the facts about one dataset")
    show.add_argument("name", help="dataset name, for example 'iris'")
    show.set_defaults(handler=show_command)
    return parser
