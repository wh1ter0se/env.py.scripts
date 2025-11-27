import shutil
import subprocess
from pathlib import Path
from typing import Optional

from _common import format_prefix, must_pass, run_cmd
from _config import PYTHON_VERSION, VENV_LOCATION, check_parent_config


def remove_existing_venv(
    venv_path: Path,
    prefix: Optional[str],
) -> None:
    print(format_prefix(prefix) + "Searching for existing venv...")

    # Remove the existing venv
    if venv_path.exists():
        print("\tRemoving existing venv...")
        shutil.rmtree(venv_path)
        print("\tExisting venv removed")
    else:
        print("\tNo existing venv found")


def create_venv(
    venv_path: Optional[Path] = None,
    version: Optional[str] = None,
    prefix: Optional[str] = None,
) -> Optional[Path]:
    """Create a virtual environment at the specified path."""
    print(format_prefix(prefix) + "Creating venv...")

    # Update defaults from parent config (if any)
    check_parent_config()

    # Populate missing vars
    if venv_path is None:
        venv_path = VENV_LOCATION
    if version is None:
        version = PYTHON_VERSION

    # Remove the existing venv
    if venv_path.exists():
        print("\tRemoving existing venv...")
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
        print("\tVenv created")
        return venv_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\tFailed to create venv")

    return None


if __name__ == "__main__":
    # Create a virtual environment
    venv_path = create_venv(prefix="5/7")
    must_pass(venv_path is not None and venv_path.exists())
