import subprocess
from pathlib import Path
from typing import List, Optional, Union

import _config
from _common import format_prefix, must_pass, run_cmd
from _logging import get_logger

log = get_logger()


def install_dependencies(
    projects: Optional[List[str]] = None,
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
    for project in projects:
        log.debug(f"Installing dependencies for project '{project}'...")
        try:
            # Build the command
            project_path = Path(project).resolve()
            cmd = ["uv", "pip", "install", str(project_path)]
            if len(dependency_groups) > 0:
                cmd.append("--group")
                cmd.extend(dependency_groups)
            print(f"`{' '.join(cmd)}`")

            # Run the command
            proc = run_cmd(cmd=cmd, check=True, stdout=subprocess.PIPE)
            log.debug(f"Installed dependencies for project '{project}'")
            log.debug(proc.stdout)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            log.error(f"Failed to install project '{project}': {e}")
            return False

    log.debug("All dependencies installed")
    return True


if __name__ == "__main__":
    # Install dependencies in the virtual environment
    must_pass(install_dependencies(prefix="1/1"))
