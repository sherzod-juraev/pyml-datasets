"""The command line of the development scripts.

Run it from the repository root::

    python -m scripts new seeds -l by -t clf   # scaffold of a new dataset
    python -m scripts build seeds              # build the NPZ file
    python -m scripts gen                      # write the files derived from INFO
    python -m scripts legal                    # license and evidence check
    python -m scripts refresh seeds            # build, gen and legal in a row
    python -m scripts check                    # legal and ``gen --check``, as in CI
    python -m scripts list                     # the table of the datasets
    python -m scripts show iris                # the facts about one dataset

Every command returns 0 if it succeeded and 1 if not (2 for an unknown dataset name), and the
errors go to ``stderr``, so CI can use it as a gate. The commands call the modules of this
package, which only compute and return results; everything is printed here, through
:mod:`scripts._console`. ``list`` and ``show`` are the ``pyml-datasets`` command of the
package, called in the same process, so the output is the one users see.
"""

import argparse
from collections.abc import Callable, Mapping, Sequence
from functools import partial
from pathlib import Path
from typing import Final

from rich_argparse import RawDescriptionRichHelpFormatter

from pyml_datasets._cli import main as package_cli
from pyml_datasets._cli._parser import add_list_options, add_show_options
from pyml_datasets._types import LICENSE_IDS, TASKS
from scripts import ROOT, _console, build_datasets, check_legal, generate, new_dataset, utc_today
from scripts._console import Cell
from scripts.recipes import recipe_names

LICENSE_ALIASES: Final = {"cc0": "CC0-1.0", "by": "CC-BY-4.0", "cc-by": "CC-BY-4.0"}
TASK_ALIASES: Final = {"clf": "classification", "reg": "regression"}

_SCAFFOLD_NOTES: Final = (
    ("pyml_datasets/datasets/", "INFO (provenance, license) and the load function"),
    ("scripts/recipes/", "build(): how the arrays are made"),
    ("tests/expected/", "facts from the source, for the tests"),
    ("docs/source/datasets/", "page for students"),
    ("legal/evidence/", "where and when the license was read"),
)


def _resolver(
    kind: str, choices: Sequence[str], aliases: Mapping[str, str]
) -> Callable[[str], str]:
    """Build a function that turns a full name or a short name into the full name.

    Parameters
    ----------
    kind : str
        What is parsed, for the error message.
    choices : sequence of str
        The full names.
    aliases : mapping of str to str
        Short name and the full name it stands for. A short name whose full name is not in
        ``choices`` is ignored.

    Returns
    -------
    callable
        Function from a string to a full name, for the ``type`` of an argument. It ignores
        the case and raises ``argparse.ArgumentTypeError`` for an unknown value.
    """
    known = {choice.lower(): choice for choice in choices}
    known.update({alias: full for alias, full in aliases.items() if full in choices})
    allowed = ", ".join([*choices, *(alias for alias in aliases if aliases[alias] in choices)])

    def resolve(value: str) -> str:
        """Return the full name of ``value``, or raise if it is not known."""
        try:
            return known[value.lower()]
        except KeyError:
            raise argparse.ArgumentTypeError(
                f"{value!r} is not a {kind}, use one of: {allowed}"
            ) from None

    return resolve


resolve_license: Final = _resolver("license", LICENSE_IDS, LICENSE_ALIASES)
resolve_task: Final = _resolver("task", TASKS, TASK_ALIASES)


def _yes(flag: bool) -> Cell:
    """Return a green ``yes`` or a red ``no``."""
    return _console.green("yes") if flag else _console.red("no")


def _note_for(relative: str) -> str:
    """Return what goes into a scaffold file, from its path relative to the root."""
    for prefix, text in _SCAFFOLD_NOTES:
        if relative.startswith(prefix):
            return text
    return ""


def _new(args: argparse.Namespace) -> int:
    """Create the files of a new dataset."""
    try:
        created = new_dataset.create(args.name, args.license_id, args.task, utc_today().isoformat())
    except (ValueError, FileExistsError) as error:
        _console.fail(str(error))
        return 1
    rows: list[Sequence[Cell]] = []
    for path in created:
        relative = path.relative_to(ROOT).as_posix()
        rows.append((relative, _note_for(relative)))
    _console.print_table(f"Created the files of {args.name}", ["File", "What goes into it"], rows)
    _console.note("Search for TODO and fill the files in, then run:")
    _console.note(f"  python -m scripts refresh {args.name}")
    _console.note("The steps are in CONTRIBUTING.md, 'Adding a dataset'.")
    return 0


def _unknown_names(names: Sequence[str]) -> list[str]:
    """Return the names that have no recipe."""
    available = recipe_names()
    return [name for name in names if name not in available]


def _build_names(names: Sequence[str], output_dir: Path, force: bool) -> int:
    """Build the datasets, print a summary, and return the exit code."""
    unknown = _unknown_names(names)
    if unknown:
        _console.fail(f"No recipe for: {', '.join(unknown)}. Recipes: {', '.join(recipe_names())}.")
        return 2
    results: list[build_datasets.BuildResult] = []
    for name in names:
        with _console.out.status(f"Building {name}"):
            results.append(build_datasets.build_dataset(name, output_dir, force))
    rows: list[Sequence[Cell]] = [
        (
            result.name,
            _console.green("built") if result.built else _console.dim("kept"),
            " x ".join(map(str, result.shape)) if result.shape else "",
            f"{result.size_kib:.1f}",
        )
        for result in results
    ]
    _console.print_table(
        "Data files", ["Dataset", "Result", "X shape", "Size (KiB)"], rows, numeric=(3,)
    )
    if any(not result.built for result in results):
        _console.note("Kept files were not rebuilt, use --force to replace them.")
    return 0


def _build(args: argparse.Namespace) -> int:
    """Build the data files of the given datasets, or of all of them."""
    code = _build_names(args.names or list(recipe_names()), args.output_dir, args.force)
    if code == 0:
        _console.note("Next: python -m scripts gen")
    return code


def _generate(check: bool) -> int:
    """Write the generated files, or check them, and return the exit code."""
    try:
        stale = generate.run(check=check)
    except FileNotFoundError as error:
        _console.fail(str(error))
        return 1
    if not stale:
        _console.ok("Generated files are up to date.")
        return 0
    state = _console.red("out of date") if check else _console.green("written")
    _console.print_table(
        "Generated files",
        ["File", "State"],
        [(path.relative_to(ROOT).as_posix(), state) for path in stale],
    )
    if check:
        _console.fail("Run `python -m scripts gen` and commit the result.")
        return 1
    return 0


def _gen(args: argparse.Namespace) -> int:
    """Write or check the files derived from ``INFO``."""
    return _generate(args.check)


def _legal_check() -> int:
    """Run the legal check, print a table and the messages, and return the exit code."""
    problems = check_legal.collect_problems()
    errors: dict[str, int] = {}
    warnings: dict[str, int] = {}
    for message in problems.errors:
        owner = check_legal.owner_of(message)
        errors[owner] = errors.get(owner, 0) + 1
    for message in problems.warnings:
        owner = check_legal.owner_of(message)
        warnings[owner] = warnings.get(owner, 0) + 1
    rows: list[Sequence[Cell]] = []
    for row in check_legal.summarize():
        if errors.get(row.name):
            result = _console.red(f"{errors[row.name]} error(s)")
        elif warnings.get(row.name):
            result = _console.yellow(f"{warnings[row.name]} warning(s)")
        else:
            result = _console.green("ok")
        rows.append(
            (
                row.name,
                row.license,
                row.verified_on,
                str(row.age),
                _yes(row.has_evidence),
                _yes(row.has_archive),
                _yes(row.has_maintainer_check),
                result,
            )
        )
    _console.print_table(
        "Legal check",
        [
            "Dataset",
            "License",
            "Verified",
            "Age (d)",
            "Evidence",
            "Archive",
            "Maintainer",
            "Result",
        ],
        rows,
        numeric=(3,),
        caption=(
            f"{len(rows)} dataset(s), {len(problems.errors)} error(s), "
            f"{len(problems.warnings)} warning(s)."
        ),
    )
    for message in problems.warnings:
        _console.warn(message)
    for message in problems.errors:
        _console.fail(message)
    if problems.errors:
        return 1
    _console.ok("Legal check passed.")
    return 0


def _legal(args: argparse.Namespace) -> int:
    """Check licenses and evidence."""
    return _legal_check()


def _refresh(args: argparse.Namespace) -> int:
    """Build one dataset, generate the derived files and check the result."""
    _console.step(f"Build {args.name}")
    code = _build_names([args.name], build_datasets.OUTPUT_DIR, args.force)
    if code != 0:
        return code
    _console.step("Generate the derived files")
    code = _generate(check=False)
    if code != 0:
        return code
    _console.step("Check licenses and evidence")
    return _legal_check()


def _list(args: argparse.Namespace) -> int:
    """Run ``pyml-datasets list`` of the package."""
    argv = ["list", "--sort", args.sort]
    if args.task is not None:
        argv += ["--task", args.task]
    if args.reverse:
        argv.append("--reverse")
    return package_cli(argv)


def _show(args: argparse.Namespace) -> int:
    """Run ``pyml-datasets show`` of the package."""
    return package_cli(["show", args.name, *(["--full"] if args.full else [])])


def _check(args: argparse.Namespace) -> int:
    """Run the checks of the ``legal`` Nox session."""
    _console.step("Check licenses and evidence")
    legal_code = _legal_check()
    _console.step("Check the generated files")
    generate_code = _generate(check=True)
    return 1 if legal_code or generate_code else 0


class _HelpFormatter(RawDescriptionRichHelpFormatter):
    """Colored help text. Nothing in it is read as rich markup."""

    help_markup = False
    text_markup = False


def build_parser() -> argparse.ArgumentParser:
    """Create the parser of the command line.

    Returns
    -------
    argparse.ArgumentParser
        Parser with one sub-command for every command of the module docstring.
    """
    parser = argparse.ArgumentParser(
        prog="python -m scripts",
        description="Development tools of pyml-datasets.",
        formatter_class=_HelpFormatter,
        epilog=(
            "examples:\n"
            "  python -m scripts new seeds -l by -t clf\n"
            "  python -m scripts refresh seeds\n"
            "  python -m scripts check"
        ),
    )
    commands = parser.add_subparsers(dest="command", metavar="COMMAND", required=True)
    add_command = partial(commands.add_parser, formatter_class=_HelpFormatter)

    new = add_command("new", help="create the files of a new dataset")
    new.add_argument("name", help="dataset name, for example 'seeds'")
    new.add_argument(
        "-l",
        "--license",
        dest="license_id",
        required=True,
        type=resolve_license,
        metavar="LICENSE",
        help=f"license of the dataset: {', '.join(LICENSE_IDS)} (short: cc0, by)",
    )
    new.add_argument(
        "-t",
        "--task",
        required=True,
        type=resolve_task,
        metavar="TASK",
        help=f"task of the dataset: {', '.join(TASKS)} (short: clf, reg)",
    )
    new.set_defaults(handler=_new)

    build = add_command("build", help="build the NPZ data files")
    build.add_argument(
        "names",
        nargs="*",
        metavar="NAME",
        help="datasets to build, all by default",
    )
    build.add_argument(
        "-f", "--force", action="store_true", help="replace the files that already exist"
    )
    build.add_argument(
        "--output-dir",
        type=Path,
        default=build_datasets.OUTPUT_DIR,
        help="directory for the NPZ files (default: pyml_datasets/data)",
    )
    build.set_defaults(handler=_build)

    gen = add_command("gen", help="write the files derived from INFO")
    gen.add_argument(
        "--check",
        action="store_true",
        help="do not write, fail if a generated file is out of date",
    )
    gen.set_defaults(handler=_gen)

    listing = add_command("list", help="show a table of the datasets (pyml-datasets list)")
    add_list_options(listing)
    listing.set_defaults(handler=_list)

    show = add_command("show", help="show the facts about one dataset (pyml-datasets show)")
    add_show_options(show)
    show.set_defaults(handler=_show)

    legal = add_command("legal", help="check licenses and evidence")
    legal.set_defaults(handler=_legal)

    refresh = add_command("refresh", help="build a dataset, then run gen and legal")
    refresh.add_argument("name", help="dataset name")
    refresh.add_argument(
        "-f", "--force", action="store_true", help="replace the data file if it exists"
    )
    refresh.set_defaults(handler=_refresh)

    check = add_command(
        "check", help="run the legal check and the generated files check, as CI does"
    )
    check.set_defaults(handler=_check)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command line interface.

    Parameters
    ----------
    argv : sequence of str, optional
        Command line arguments, ``sys.argv[1:]`` if not given.

    Returns
    -------
    int
        Exit code: 0 on success, 1 if a check failed, 2 for a name that is not known.
    """
    args = build_parser().parse_args(argv)
    code: int = args.handler(args)
    return code
