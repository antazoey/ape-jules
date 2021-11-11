from ape import plugins
from ape.api.config import ConfigItem

from .config import JulesConfig


@plugins.register(plugins.Config)
def config_class():
    return JulesConfig
