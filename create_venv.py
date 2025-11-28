import shutil
import subprocess
from pathlib import Path
from typing import Optional

from _common import format_prefix, must_pass, run_cmd
from _config import PYTHON_VERSION, VENV_LOCATION, check_parent_config
from _logging import get_logger

log = get_logger()


def remove_existing_venv(
    venv_path: Path,
    prefix: Optional[str],
) -> None:
    log.info(format_prefix(prefix) + "Searching for existing venv...")

    # Remove the existing venv
    if venv_path.exists():
        log.debug("Removing existing venv...")
        shutil.rmtree(venv_path)
        log.debug("Existing venv removed")
    else:
        log.debug("No existing venv found")


def create_venv(
    venv_path: Optional[Path] = None,
    version: Optional[str] = None,
    prefix: Optional[str] = None,
) -> Optional[Path]:
    """Create a virtual environment at the specified path."""
    log.info(format_prefix(prefix) + "Creating venv...")

    # Populate missing vars
    if venv_path is None:
        venv_path = VENV_LOCATION
    if version is None:
        version = PYTHON_VERSION

    # Remove the existing venv
    if venv_path.exists():
        log.debug("Removing existing venv...")
        shutil.rmtree(venv_path)

    # Specify version if provided
    cmd = ["uv", "venv"]
    if version is not None:
        cmd.append("--python")
        cmd.append(version)
    cmd.append(str(venv_path))

    # Create the venv
    try:
        run_cmd(cmd=cmd, check=True)
        log.debug("Venv created")
        return venv_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        log.error("Failed to create venv")

    return None


if __name__ == "__main__":
    # Load the parent config
    must_pass(check_parent_config(prefix="1/2"))

    # Create a virtual environment
    venv_path = create_venv(prefix="2/2")
    must_pass(venv_path is not None and venv_path.exists())
