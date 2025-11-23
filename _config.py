from pathlib import Path
from typing import List, Optional

VENV_LOCATION: Path = Path(".venv")
PYTHON_VERSION: Optional[str] = None
PROJECTS: List[Path] = []
DEV_DEP_GROUPS = ["dev", "test"]
PIPELINE_DEP_GROUPS = ["pipeline", "test"]
