from typing import List, Optional

from _common import get_uv_version, must_pass
from _config import check_parent_config
from create_venv import create_venv
from generate_stubs import generate_stubs
from install_dependencies import install_dependencies
from install_uv import install_uv, update_uv


def setup_environment(dependency_groups: Optional[List[str]] = None) -> None:
    if dependency_groups is None:
        dependency_groups = []

    # Load the parent config
    must_pass(check_parent_config(prefix="1/8"))

    # Install uv
    if get_uv_version(prefix="2/8") is None:
        must_pass(install_uv(prefix="3/8"))

    # Update uv
    must_pass(update_uv(prefix="4/8"))

    # Verify installation
    must_pass(get_uv_version(prefix="5/8") is not None)

    # Create a virtual environment
    venv_path = create_venv(prefix="6/8")
    must_pass(venv_path is not None and venv_path.exists())

    # Install dependencies in the virtual environment
    must_pass(
        install_dependencies(
            dependency_groups=dependency_groups,
            prefix="7/8",
        )
    )

    # Generate stubs
    must_pass(generate_stubs(prefix="8/8"))
