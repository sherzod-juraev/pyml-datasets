"""Development tooling of pyml-datasets: build, generate and legal checks.

The scripts are used during development and in CI only and are not part of the installed
package. Run them from the repository root, for example ``python -m scripts.generate``.
"""

from pathlib import Path
from typing import Final

ROOT: Final = Path(__file__).resolve().parents[1]
