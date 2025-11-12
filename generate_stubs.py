import subprocess
from _config import PROJECTS
from _common import must_pass, format_prefix, run_cmd
from pathlib import Path


def generate_stubs(
    projects: list[Path] = PROJECTS,
    prefix: str | None = None,
) -> bool:
    print(format_prefix(prefix) + "Generating stubs...")
    for project in projects:
        print(f"\tGenerating stubs for '{project.name}'...")
        try:
            run_cmd()  # TODO
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"\tUnable to generate stubs for '{project.name}")
            return False

    print(f"\tAll stubs generated")
    return True


if __name__ == "__main__":
    # Generate stubs
    must_pass(generate_stubs(prefix="7/7"))
