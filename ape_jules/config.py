from pathlib import Path

from ape.api.config import PluginConfig


class JulesConfig(PluginConfig):
    message: str = "Jules hacks"
    projects_directory: str = str(Path.home() / "ApeProjects")
