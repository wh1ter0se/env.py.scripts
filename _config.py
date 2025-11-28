import json
from pathlib import Path
from typing import List, Optional, TypedDict

from _common import format_prefix
from _logging import get_logger

log = get_logger()


class ParentConfig(TypedDict):
    VENV_LOCATION: str
    PYTHON_VERSION: Optional[str]
    PROJECTS: List[str]
    DEV_DEP_GROUPS: List["str"]
    PIPELINE_DEP_GROUPS: List["str"]


DEFAULT_PARENT_CONFIG_PATH = Path(".script_config.json")
DEFAULT_PARENT_CONFIG = ParentConfig(
    VENV_LOCATION=".venv",
    PYTHON_VERSION=None,
    PROJECTS=[],
    DEV_DEP_GROUPS=["dev", "test"],
    PIPELINE_DEP_GROUPS=["pipeline", "test"],
)

VENV_LOCATION: Path = Path(DEFAULT_PARENT_CONFIG["VENV_LOCATION"])
PYTHON_VERSION: Optional[str] = DEFAULT_PARENT_CONFIG["PYTHON_VERSION"]
PROJECTS: List[str] = DEFAULT_PARENT_CONFIG["PROJECTS"]
DEV_DEP_GROUPS: List["str"] = DEFAULT_PARENT_CONFIG["DEV_DEP_GROUPS"]
PIPELINE_DEP_GROUPS: List["str"] = DEFAULT_PARENT_CONFIG["PIPELINE_DEP_GROUPS"]


def create_parent_config(
    parent_config_path: Path,
    prefix: Optional[str] = None,
) -> bool:
    # Resolve the path
    parent_config_path = parent_config_path.resolve()

    # Check if there is an existing file
    if parent_config_path.exists():
        log.info(
            format_prefix(prefix)
            + f"Overwriting parent config at '{parent_config_path}' with defaults..."
        )
    else:
        log.info(
            format_prefix(prefix)
            + f"Writing new parent config at '{parent_config_path}' with defaults..."
        )

    # Write the defaults to file
    try:
        with open(parent_config_path, "w") as f:
            json.dump(dict(DEFAULT_PARENT_CONFIG), f, indent=4)
        log.info("Parent config generated using defaults")
        return True
    except Exception as e:
        log.error(
            f"\tException while reading parent config at '{parent_config_path}': {e}"
        )
        return False


def check_parent_config(
    parent_config_path: Optional[Path] = None,
    prefix: Optional[str] = None,
) -> bool:
    log.info(format_prefix(prefix) + "Loading parent config...")
    # Populate the path (if not provided)
    if parent_config_path is None:
        parent_config_path = DEFAULT_PARENT_CONFIG_PATH

    # Resolve the path
    parent_config_path = parent_config_path.resolve()

    # Check for the config file
    if parent_config_path.exists():
        log.debug("Found parent config")
    else:
        log.warning(f"\tNo parent config found at '{parent_config_path}")
        if not create_parent_config(parent_config_path=parent_config_path):
            return False

    # Try to load the config
    parent_config: ParentConfig
    try:
        with open(parent_config_path) as f:
            parent_config = json.load(f)
        log.debug("Parent config loaded")
    except Exception as e:
        log.error(
            f"\tException while reading parent config at '{parent_config_path}': {e}"
        )
        return False

    # Check for each variable
    if "VENV_LOCATION" in parent_config.keys():
        log.debug("Found VENV_LOCATION")
        global VENV_LOCATION
        VENV_LOCATION = Path(parent_config["VENV_LOCATION"])

    if "PYTHON_VERSION" in parent_config.keys():
        log.debug("Found PYTHON_VERSION")
        global PYTHON_VERSION
        PYTHON_VERSION = parent_config["PYTHON_VERSION"]

    if "PROJECTS" in parent_config.keys():
        log.debug("Found PROJECTS")
        global PROJECTS
        PROJECTS = parent_config["PROJECTS"]

    if "DEV_DEP_GROUPS" in parent_config.keys():
        log.debug("Found DEV_DEP_GROUPS")
        global DEV_DEP_GROUPS
        DEV_DEP_GROUPS = parent_config["DEV_DEP_GROUPS"]

    if "PIPELINE_DEP_GROUPS" in parent_config.keys():
        log.debug("Found PIPELINE_DEP_GROUPS")
        global PIPELINE_DEP_GROUPS
        PIPELINE_DEP_GROUPS = parent_config["PIPELINE_DEP_GROUPS"]

    return True
