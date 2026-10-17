"""Download helper for the recipes: a file is used only if its SHA-256 digest matches."""

import hashlib
import urllib.request
from pathlib import Path
from typing import Final

_CACHE_DIR: Final = Path(__file__).resolve().parents[2] / ".cache" / "raw"
_TIMEOUT_SECONDS: Final = 60


def download(url: str, sha256: str) -> bytes:
    """Download a file, or read it from the local cache, and verify its digest.

    A recipe pins the digest of the file it was written for. If the source changes the
    file, the build stops instead of silently saving different data. After a deliberate
    update, review the new file and replace the digest in the recipe.

    Parameters
    ----------
    url : str
        Address of the file, must start with ``https://``.
    sha256 : str
        Expected SHA-256 digest of the file, as lowercase hexadecimal text.

    Returns
    -------
    bytes
        Content of the file.

    Raises
    ------
    ValueError
        If the address is not an https address, or the digest does not match.
    """
    if not url.startswith("https://"):
        raise ValueError(f"Only https downloads are allowed, got {url!r}.")

    cached = _CACHE_DIR / sha256
    if cached.is_file():
        data = cached.read_bytes()
    else:
        with urllib.request.urlopen(url, timeout=_TIMEOUT_SECONDS) as response:  # noqa: S310
            data = response.read()

    digest = hashlib.sha256(data).hexdigest()
    if digest != sha256:
        raise ValueError(
            f"{url} has SHA-256 {digest}, expected {sha256}. The source changed the file: "
            "review the new version and its license before updating the digest in the recipe."
        )

    cached.parent.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(data)
    return data
