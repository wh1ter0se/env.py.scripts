from _setup_environment import setup_environment
from install_dependencies import DependencyGroupSet

if __name__ == "__main__":
    setup_environment(dependency_group_set=DependencyGroupSet.dev)
