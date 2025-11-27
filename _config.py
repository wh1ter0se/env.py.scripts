import json
from pathlib import Path
from typing import List, Optional, TypedDict


class ParentConfig(TypedDict):
    VENV_LOCATION: Path
    PYTHON_VERSION: Optional[str]
    PROJECTS: List[Path]
    DEV_DEP_GROUPS: List["str"]
    PIPELINE_DEP_GROUPS: List["str"]


VENV_LOCATION: Path = Path(".venv")
PYTHON_VERSION: Optional[str] = None
PROJECTS: List[Path] = []
DEV_DEP_GROUPS: List["str"] = ["dev", "test"]
PIPELINE_DEP_GROUPS: List["str"] = ["pipeline", "test"]


def check_parent_config(
    parent_config_path: Path = Path("../script_config.json"),
) -> None:
    # Check for the config file
    if not parent_config_path.exists():
        return

    # Try to load the config
    parent_config: ParentConfig
    try:
        with open(parent_config_path) as f:
            parent_config = json.load(f)
    except Exception:
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
