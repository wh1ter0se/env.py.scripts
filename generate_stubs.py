import subprocess
from pathlib import Path
from typing import List, Union

from _common import format_prefix, must_pass, run_cmd
from _config import PROJECTS
from _logging import get_logger

log = get_logger()


def generate_stubs(
    projects: List[Path] = PROJECTS,
    prefix: Union[str, None] = None,
) -> bool:
    log.info(format_prefix(prefix) + "Generating stubs...")
    for project in projects:
        log.debug(f"Generating stubs for '{project.name}'...")
        try:
            run_cmd(
                [
                    "uv",
                    "run",
                    "stubgen",
                    "-p",
                    project.name,
                    "-o",
                    f"{project.name}/stubs",
                ]
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            log.error(f"Unable to generate stubs for '{project.name}")
            return False

    log.debug("All stubs generated")
    return True


if __name__ == "__main__":
    # Generate stubs
    must_pass(generate_stubs(prefix="1/1"))
