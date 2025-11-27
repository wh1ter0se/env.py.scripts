import json
from pathlib import Path
from typing import List, Optional, TypedDict

from _common import format_prefix


class ParentConfig(TypedDict):
    VENV_LOCATION: Path
    PYTHON_VERSION: Optional[str]
    PROJECTS: List[Path]
    DEV_DEP_GROUPS: List["str"]
    PIPELINE_DEP_GROUPS: List["str"]


DEFAULT_PARENT_CONFIG = ParentConfig(
    VENV_LOCATION=Path(".venv"),
    PYTHON_VERSION=None,
    PROJECTS=[],
    DEV_DEP_GROUPS=["dev", "test"],
    PIPELINE_DEP_GROUPS=["pipeline", "test"],
)

VENV_LOCATION: Path = DEFAULT_PARENT_CONFIG["VENV_LOCATION"]
PYTHON_VERSION: Optional[str] = DEFAULT_PARENT_CONFIG["PYTHON_VERSION"]
PROJECTS: List[Path] = DEFAULT_PARENT_CONFIG["PROJECTS"]
DEV_DEP_GROUPS: List["str"] = DEFAULT_PARENT_CONFIG["DEV_DEP_GROUPS"]
PIPELINE_DEP_GROUPS: List["str"] = DEFAULT_PARENT_CONFIG["PIPELINE_DEP_GROUPS"]


def create_parent_config(
    parent_config_path: Path,
    prefix: Optional[str] = None,
) -> None:
    # Resolve the path
    parent_config_path = parent_config_path.resolve()

    # Check if there is an existing file
    if parent_config_path.exists():
        print(
            format_prefix(prefix)
            + f"Overwriting parent config at '{parent_config_path}' with defaults..."
        )
    else:
        print(
            format_prefix(prefix)
            + f"Writing new parent config at '{parent_config_path}' with defaults..."
        )

    # Write the defaults to file
    try:
        with open(parent_config_path, "w") as f:
            json.dump(DEFAULT_PARENT_CONFIG, f)
        print(format_prefix(prefix) + "Parent config generated using defaults")
    except Exception as e:
        print(
            format_prefix(prefix)
            + f"Exception while reading parent config at '{parent_config_path}': {e}"
        )
        return


def check_parent_config(
    parent_config_path: Optional[Path] = None,
    prefix: Optional[str] = None,
) -> None:
    # Populate the path (if not provided)
    if parent_config_path is None:
        parent_config_path = Path("script_config.json")

    # Resolve the path
    parent_config_path = parent_config_path.resolve()

    # Check for the config file
    if not parent_config_path.exists():
        print(
            format_prefix(prefix) + f"No parent config found at '{parent_config_path}"
        )
        create_parent_config(parent_config_path=parent_config_path)

    # Try to load the config
    parent_config: ParentConfig
    try:
        print(format_prefix(prefix) + "Reading parent config...")
        with open(parent_config_path) as f:
            parent_config = json.load(f)
    except Exception as e:
        print(
            format_prefix(prefix)
            + f"Exception while reading parent config at '{parent_config_path}': {e}"
        )
        return

    # Check for each variale
    if "VENV_LOCATION" in parent_config.keys():
        global VENV_LOCATION
        VENV_LOCATION = parent_config["VENV_LOCATION"]

    if "PYTHON_VERSION" in parent_config.keys():
        global PYTHON_VERSION
        PYTHON_VERSION = parent_config["PYTHON_VERSION"]

    if "PROJECTS" in parent_config.keys():
        global PROJECTS
        PROJECTS = parent_config["PROJECTS"]

    if "DEV_DEP_GROUPS" in parent_config.keys():
        global DEV_DEP_GROUPS
        DEV_DEP_GROUPS = parent_config["DEV_DEP_GROUPS"]

    if "PIPELINE_DEP_GROUPS" in parent_config.keys():
        global PIPELINE_DEP_GROUPS
        PIPELINE_DEP_GROUPS = parent_config["PIPELINE_DEP_GROUPS"]
