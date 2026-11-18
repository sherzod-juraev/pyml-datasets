"""The argument parser of the command line."""

import argparse
from functools import partial

from rich_argparse import RawDescriptionRichHelpFormatter

from .._types import TASKS
from ._commands import DEFAULT_LIMIT, SORT_KEYS, list_command, show_command
from ._output import FORMATS


def _positive_int(text: str) -> int:
    """Read a whole number of one or more.

    Parameters
    ----------
    text : str
        Text of the argument.

    Returns
    -------
    int
        The number.

    Raises
    ------
    argparse.ArgumentTypeError
        If the text is not a whole number of one or more.
    """
    if not text.isdecimal() or int(text) < 1:
        raise argparse.ArgumentTypeError(f"{text!r} is not a whole number of 1 or more")
    return int(text)


def _non_negative_int(text: str) -> int:
    """Read a whole number of zero or more.

    Parameters
    ----------
    text : str
        Text of the argument.

    Returns
    -------
    int
        The number.

    Raises
    ------
    argparse.ArgumentTypeError
        If the text is not a whole number of zero or more.
    """
    if not text.isdecimal():
        raise argparse.ArgumentTypeError(f"{text!r} is not a whole number of 0 or more")
    return int(text)


class _HelpFormatter(RawDescriptionRichHelpFormatter):
    """Colored help text. Nothing in it is read as rich markup."""

    help_markup = False
    text_markup = False


def add_output_options(parser: argparse.ArgumentParser) -> None:
    """Add the options that choose the format and the file of the output.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        Parser of a command that prints a table or a report.
    """
    parser.add_argument(
        "--format",
        choices=FORMATS,
        help=(
            "format of the output: text (default), md (Markdown) or json. With --output the "
            "extension .md, .txt or .json chooses it"
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="PATH",
        help=(
            "write the output to this file, always in UTF-8, instead of the terminal. '-' is "
            "the terminal"
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite the file of --output if it exists",
    )


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
        "--name",
        metavar="PATTERN",
        help=(
            "show only the datasets whose name matches the pattern: * (or %%) is any "
            "characters and ? is one character, so 'wine*' starts with wine and '*quality' "
            "ends with quality. Capital letters do not matter. Without them the pattern has "
            "to match the whole name. Quote the pattern"
        ),
    )
    parser.add_argument(
        "--missing",
        action=argparse.BooleanOptionalAction,
        help="show only the datasets that have (--missing) or do not have (--no-missing) "
        "missing values",
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
    parser.add_argument(
        "--offset",
        type=_non_negative_int,
        default=0,
        metavar="N",
        help="skip the first N rows (default: %(default)s)",
    )
    size = parser.add_mutually_exclusive_group()
    size.add_argument(
        "--limit",
        type=_positive_int,
        metavar="N",
        help=f"show at most N rows (default: {DEFAULT_LIMIT})",
    )
    size.add_argument(
        "--all",
        dest="show_all",
        action="store_true",
        help="show every row, without a limit",
    )
    add_output_options(parser)


def add_show_options(parser: argparse.ArgumentParser) -> None:
    """Add the arguments of ``show`` to a parser.

    The ``scripts`` command line adds the same arguments to its own ``show``.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        Parser of the ``show`` command.
    """
    parser.add_argument("name", help="dataset name, for example 'iris'")
    parser.add_argument(
        "--full",
        action="store_true",
        help="also show the changes made to the data and the notes",
    )
    add_output_options(parser)


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
            "  pyml-datasets list --name 'wine*' --no-missing\n"
            "  pyml-datasets list --limit 5 --offset 10\n"
            "  pyml-datasets list --format json\n"
            "  pyml-datasets show iris\n"
            "  pyml-datasets show german_credit --full\n"
            "  pyml-datasets show german_credit --full -o german_credit.md"
        ),
    )
    commands = parser.add_subparsers(dest="command", metavar="COMMAND", required=True)
    add_command = partial(commands.add_parser, formatter_class=_HelpFormatter)

    listing = add_command("list", help="show a table of the datasets")
    add_list_options(listing)
    listing.set_defaults(handler=list_command)

    show = add_command("show", help="show the facts about one dataset")
    add_show_options(show)
    show.set_defaults(handler=show_command)
    return parser
