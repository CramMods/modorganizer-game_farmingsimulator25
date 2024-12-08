from mobase import IPlugin

from .plugin import FS25GamePlugin


def createPlugin() -> IPlugin:
    return FS25GamePlugin()
