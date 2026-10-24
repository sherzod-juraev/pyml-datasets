"""Development tooling of pyml-datasets: build, generate and legal checks.

The scripts are used during development and in CI only and are not part of the installed
package. Run them from the repository root, for example ``python -m scripts.generate``.
"""

from datetime import UTC, date, datetime
from pathlib import Path
from typing import Final

ROOT: Final = Path(__file__).resolve().parents[1]


def utc_today() -> date:
    """Return today's date in UTC.

    Every date in the legal evidence and in ``INFO.verified_on`` is a UTC date, because the
    Wayback Machine and the CI work in UTC. Near midnight the local date of a computer can be
    a day ahead of UTC, and the legal check refuses a date that lies in the future.

    Returns
    -------
    date
        The current date in UTC, whatever the time zone of the computer is.
    """
    return datetime.now(UTC).date()
