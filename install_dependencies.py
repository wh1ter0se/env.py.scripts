import subprocess
from enum import Enum
from typing import List, Optional, Union

import _config
from _common import format_prefix, must_pass, run_cmd
from _logging import get_logger

log = get_logger()


class DependencyGroupSet(Enum):
    baseline = 0
    dev = 1
    pipeline = 2


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
            cmd = ["uv", "pip", "install", project]
            for dependency_group in dependency_groups:
                cmd.append("--group")
                cmd.append(dependency_group)

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


def install_dependencies_by_set(
    projects: Optional[List[str]] = None,
    dependency_group_set: DependencyGroupSet = DependencyGroupSet.baseline,
    prefix: Union[str, None] = None,
) -> bool:
    # Grab the current lsit from _config
    dependency_groups = []
    if dependency_group_set == DependencyGroupSet.dev:
        dependency_groups.extend(_config.DEV_DEP_GROUPS)
    elif dependency_group_set == DependencyGroupSet.pipeline:
        dependency_groups.extend(_config.PIPELINE_DEP_GROUPS)

    # Run parent
    return install_dependencies(
        projects=projects,
        dependency_groups=dependency_groups,
        prefix=prefix,
    )


if __name__ == "__main__":
    # Install dependencies in the virtual environment
    must_pass(install_dependencies(prefix="1/1"))
