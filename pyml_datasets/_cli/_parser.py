"""The argument parser of the command line."""

import argparse
from functools import partial

from rich_argparse import RawDescriptionRichHelpFormatter

from .._types import TASKS
from ._commands import SORT_KEYS, list_command, show_command


class _HelpFormatter(RawDescriptionRichHelpFormatter):
    """Colored help text. Nothing in it is read as rich markup."""

    help_markup = False
    text_markup = False


def add_list_options(parser: argparse.ArgumentParser) -> None:
    """Add the options of ``list`` to a parser.

    The ``scripts`` command line adds the same options to its own ``list``, so both accept
    the same arguments.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        Parser of the ``list`` command.
    """
    parser.add_argument(
        "--task",
        choices=TASKS,
        help="show only the datasets of this task",
    )
    parser.add_argument(
        "--sort",
        choices=SORT_KEYS,
        default="name",
        help="order of the rows (default: %(default)s)",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="reverse the order, for example the largest dataset first",
    )


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
        epilog=(
            "examples:\n"
            "  pyml-datasets list\n"
            "  pyml-datasets list --task regression --sort samples --reverse\n"
            "  pyml-datasets show iris"
        ),
    )
    commands = parser.add_subparsers(dest="command", metavar="COMMAND", required=True)
    add_command = partial(commands.add_parser, formatter_class=_HelpFormatter)

    listing = add_command("list", help="show a table of the datasets")
    add_list_options(listing)
    listing.set_defaults(handler=list_command)

    show = add_command("show", help="show the facts about one dataset")
    show.add_argument("name", help="dataset name, for example 'iris'")
    show.set_defaults(handler=show_command)
    return parser
