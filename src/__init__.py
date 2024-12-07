from mobase import IPlugin

from .plugin import GamePlugin


def createPlugin() -> IPlugin:
    return GamePlugin()
