import subprocess
from pathlib import Path
from typing import List, Optional, Union

import _config
from _common import format_prefix, must_pass, run_cmd
from _logging import get_logger

log = get_logger()


def install_dependencies(
    projects: Optional[List[Path]] = None,
    dependency_groups: Union[List[str], None] = None,
    prefix: Union[str, None] = None,
) -> bool:
    # Populate defaultsi
    if projects is None:
        projects = _config.PROJECTS
    if dependency_groups is None:
        dependency_groups = []

    # Install each project's dependency list
    log.info(format_prefix(prefix) + "Installing dependencies...")
    for path in projects:
        log.debug(f"Installing dependencies for project '{path}'...")
        try:
            # Build the command
            cmd = ["uv", "pip", "install", str(path)]
            if len(dependency_groups) > 0:
                cmd.append("--group")
                cmd.extend(dependency_groups)

            # Run the command
            run_cmd(cmd=cmd, check=False)
            log.debug(f"Installed dependencies for project '{path}'")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            log.error(f"Failed to install project '{path}': {e}")
            return False

    log.debug("All dependencies installed")
    return True


if __name__ == "__main__":
    # Install dependencies in the virtual environment
    must_pass(install_dependencies(prefix="1/1"))
