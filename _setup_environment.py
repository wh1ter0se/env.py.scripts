from _config import DEV_DEP_GROUPS
from _common import must_pass, get_uv_version
from install_uv import install_uv, update_uv
from create_venv import create_venv
from python.install_dependencies import install_dependencies
from generate_stubs import generate_stubs


def setup_environment(dependency_groups: list[str] = []) -> None:
    # Install uv
    if get_uv_version(prefix="1/7") is None:
        must_pass(install_uv(prefix="2/7"))

    # Update uv
    must_pass(update_uv(prefix="3/7"))

    # Verify installation
    must_pass(get_uv_version(prefix="4/7") is not None)

    # Create a virtual environment
    venv_path = create_venv(prefix="5/7")
    must_pass(venv_path is not None and venv_path.exists())

    # Install dependencies in the virtual environment
    must_pass(
        install_dependencies(
            dependency_groups=dependency_groups,
            prefix="6/7",
        )
    )

    # Generate stubs
    must_pass(generate_stubs(prefix="7/7"))
