import subprocess
from typing import List, Optional

from _common import (
    format_prefix,
    get_uv_version,
    must_pass,
    run_cmd,
    user_is_running_windows,
)
from _logging import get_logger

log = get_logger()


def get_pip_alias(prefix: Optional[str] = None) -> Optional[List[str]]:
    """Checks for a binding to pip (Python package installer)"""
    log.info(format_prefix(prefix) + "Checking for pip alias...")
    aliases = [
        ["pip"],
        ["pip3"],
        ["python", "-m", "pip"],
        ["python3", "-m", "pip"],
        ["python", "-m", "pip3"],
        ["python3", "-m", "pip3"],
    ]
    for alias in aliases:
        try:
            alias.append("--version")
            run_cmd(cmd=alias, check=True)
            log.debug(f"Found pip alias ({' '.join(alias)})")
            return alias
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    log.debug("No pip alias found")
    return None


def install_uv(prefix: Optional[str]) -> bool:
    """Install uv, if not already installed."""
    log.info(format_prefix(prefix) + "Installing uv...")

    # Install via curl (if possible)
    if not user_is_running_windows():
        log.debug("*nix detected, installing uv via curl...")
        try:
            run_cmd(
                cmd="curl -LsSf https://astral.sh/uv/install.sh | sh",
                shell=True,
                check=False,
            )
            run_cmd(
                cmd=["uv", "--version"],
                check=True,
            )
            log.debug("Successfully installed uv")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            log.warning("Failed to install uv via curl")

    # Check for existing pip installation
    pip_alias = get_pip_alias()
    if pip_alias is None:
        return False

    # Install via pip
    log.debug("Installing uv via pip...")
    try:
        run_cmd(
            cmd=[*pip_alias, "install", "uv"],
            check=True,
        )
        run_cmd(
            cmd=["uv", "--version"],
            check=True,
        )
        log.debug("Successfully installed uv")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        log.warning("Failed to install uv via pip.")

    log.warning("Unable to install uv")
    return False


def update_uv(prefix: Optional[str]) -> bool:
    """Update uv to the latest version."""
    log.info(format_prefix(prefix) + "Updating uv...")

    # Update through uv
    log.debug("Updating uv directly...")
    try:
        run_cmd(
            cmd=["uv", "self", "update"],
            check=True,
        )
        log.debug("Successfully updated uv")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        log.warning("Failed to update uv directly")

    # Check for existing pip installation
    pip_alias = get_pip_alias()
    if pip_alias is None:
        return False

    # Update through pip
    log.debug("Updating uv via pip...")
    try:
        run_cmd(
            cmd=[*pip_alias, "install", "--upgrade", "uv"],
            check=True,
        )
        log.debug("Successfully updated uv")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        log.warning("Failed to update uv via pip")

    log.warning("Unable to update uv")
    return False


if __name__ == "__main__":
    # Install uv
    if get_uv_version(prefix="1/4") is None:
        must_pass(install_uv(prefix="2/4"))

    # Update uv
    update_uv(prefix="3/4")

    # Verify installation
    must_pass(get_uv_version(prefix="4/4") is not None)
