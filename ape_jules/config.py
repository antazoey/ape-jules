from pathlib import Path

from ape.api.config import PluginConfig

DEFAULT_MESSAGE = "Jules hacks"


class JulesConfig(PluginConfig):
    message: str = DEFAULT_MESSAGE
    projects_directory: str = str(Path.home() / "ApeProjects")
    editor: str = "code"
