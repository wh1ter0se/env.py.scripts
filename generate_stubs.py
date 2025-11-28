import subprocess
from pathlib import Path
from typing import List, Optional, Union

import _config
from _common import format_prefix, must_pass, run_cmd
from _logging import get_logger

log = get_logger()


def generate_stubs(
    projects: Optional[List[str]] = None,
    prefix: Union[str, None] = None,
) -> bool:
    # Populate defaults
    if projects is None:
        projects = _config.PROJECTS

    # Generate stubs for each project
    log.info(format_prefix(prefix) + "Generating stubs...")
    for project in projects:
        project_path = Path(project).resolve()
        log.debug(f"Generating stubs for '{project}'...")
        try:
            run_cmd(
                [
                    "uv",
                    "run",
                    "stubgen",
                    "-p",
                    project,
                    "-o",
                    f"{project_path}/stubs",
                ]
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            log.error(f"Unable to generate stubs for '{project}")
            return False

    log.debug("All stubs generated")
    return True


if __name__ == "__main__":
    # Generate stubs
    must_pass(generate_stubs(prefix="1/1"))
