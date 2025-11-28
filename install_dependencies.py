import subprocess
from pathlib import Path
from typing import List, Union

from _common import format_prefix, must_pass, run_cmd
from _config import PROJECTS
from _logging import get_logger

log = get_logger()


def install_dependencies(
    projects: List[Path] = PROJECTS,
    dependency_groups: Union[List[str], None] = None,
    prefix: Union[str, None] = None,
) -> bool:
    if dependency_groups is None:
        dependency_groups = []

    log.info(format_prefix(prefix) + "Installing dependencies...")
    for path in projects:
        log.debug(f"Installing project '{path}'...")
        try:
            # Build the command
            cmd = ["uv", "pip", "install", str(path)]
            if len(dependency_groups) > 0:
                cmd.append("--group")
                cmd.extend(dependency_groups)

            # Run the command
            run_cmd(cmd=cmd, check=False)
            log.debug(f"Installed project '{path}'")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            log.debug(f"Failed to install project '{path}': {e}")
            return False
    return True


if __name__ == "__main__":
    # Install dependencies in the virtual environment
    must_pass(install_dependencies(prefix="1/1"))
