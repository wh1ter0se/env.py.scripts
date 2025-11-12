import subprocess
from _common import (
    must_pass,
    format_prefix,
    run_cmd,
    user_is_running_windows,
    get_uv_version,
)


def get_pip_alias(prefix: str | None) -> list[str] | None:
    """Checks for a binding to pip (Python package installer)"""
    print(format_prefix(prefix) + "Checking for pip alias...")
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
            print(f"\tFound pip alias ({" ".join(alias)})")
            return alias
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    print("\tNo pip alias found")
    return None


def install_uv(prefix: str | None) -> bool:
    """Install uv, if not already installed."""
    print(format_prefix(prefix) + "Installing uv...")

    # Install via curl (if possible)
    if not user_is_running_windows():
        print("\t*nix detected, installing uv via curl...")
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
            print("\tSuccessfully installed uv via curl")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("\tFailed to install uv via curl")

    # Check for existing pip installation
    pip_alias = get_pip_alias()
    if pip_alias is None:
        return False

    # Install via pip
    print("\tInstalling uv via pip...")
    try:
        run_cmd(
            cmd=[*pip_alias, "install", "uv"],
            check=True,
        )
        run_cmd(
            cmd=["uv", "--version"],
            check=True,
        )
        print("\tSuccessfully installed uv via pip")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\tFailed to install uv via pip.")

    return False


def update_uv(prefix: str | None) -> bool:
    """Update uv to the latest version."""
    print(format_prefix(prefix) + "Updating uv...")

    # Update through uv
    print("\tUpdating uv directly...")
    try:
        run_cmd(
            cmd=["uv", "self", "update"],
            check=True,
        )
        print("\tSuccessfully updated uv directly")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\tFailed to update uv directly")

    # Check for existing pip installation
    pip_alias = get_pip_alias()
    if pip_alias is None:
        return False

    # Update through pip
    print("\tUpdating uv via pip...")
    try:
        run_cmd(
            cmd=[*pip_alias, "install", "--upgrade", "uv"],
            check=True,
        )
        print("\tSuccessfully updated uv via pip")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\tFailed to update uv via pip")

    return False


if __name__ == "__main__":
    # Install uv
    if get_uv_version(prefix="1/4") is None:
        must_pass(install_uv(prefix="2/4"))

    # Update uv
    must_pass(update_uv(prefix="3/4"))

    # Verify installation
    must_pass(get_uv_version(prefix="4/4") is not None)
