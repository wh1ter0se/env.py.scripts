import _config
from _setup_environment import setup_environment

if __name__ == "__main__":
    setup_environment(dependency_groups=_config.PIPELINE_DEP_GROUPS)
