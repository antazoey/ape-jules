from ape import plugins

from .config import JulesConfig


@plugins.register(plugins.Config)
def config_class():
    return JulesConfig
