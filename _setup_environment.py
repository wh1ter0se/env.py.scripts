from typing import List, Optional

import _config
from _common import check_connecion, get_uv_version, must_pass
from create_venv import create_venv
from generate_stubs import generate_stubs
from install_dependencies import install_dependencies
from install_uv import install_uv, update_uv


def setup_environment(dependency_groups: Optional[List[str]] = None) -> None:
    print()

    # Populate defaults
    if dependency_groups is None:
        dependency_groups = []

    # Check connection
    must_pass(check_connecion(prefix="1/9"))

    # Load the parent config
    must_pass(_config.check_parent_config(prefix="2/9"))

    # Install uv
    if get_uv_version(prefix="3/9") is None:
        must_pass(install_uv(prefix="4/9"))

    # Update uv
    update_uv(prefix="5/9")

    # Verify installation
    must_pass(get_uv_version(prefix="6/9") is not None)

    # Create a virtual environment
    venv_path = create_venv(prefix="7/9")
    must_pass(venv_path is not None and venv_path.exists())

    # Install dependencies in the virtual environment
    must_pass(
        install_dependencies(
            dependency_groups=dependency_groups,
            prefix="8/9",
        )
    )

    # Generate stubs
    must_pass(generate_stubs(prefix="9/9"))

    print()
