import subprocess
from pathlib import Path
from typing import List, Union

from _common import format_prefix, must_pass, run_cmd
from _config import PROJECTS


def generate_stubs(
    projects: List[Path] = PROJECTS,
    prefix: Union[str, None] = None,
) -> bool:
    print(format_prefix(prefix) + "Generating stubs...")
    for project in projects:
        print(f"\tGenerating stubs for '{project.name}'...")
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
            print(f"\tUnable to generate stubs for '{project.name}")
            return False

    print("\tAll stubs generated")
    return True


if __name__ == "__main__":
    # Generate stubs
    must_pass(generate_stubs(prefix="7/7"))
