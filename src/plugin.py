from pathlib import Path

from PyQt6.QtCore import QDir, QStandardPaths
from PyQt6.QtGui import QIcon

from mobase import (
    ExecutableForcedLoadSetting,
    ExecutableInfo,
    IOrganizer,
    IPluginGame,
    ISaveGame,
    PluginSetting,
    ProfileSetting,
    VersionInfo,
    getFileVersion,
    getIconForExecutable,
)


class GamePlugin(IPluginGame):
    _gamePath: str = ""
    _organizer: IOrganizer

    # IPlugin Implementation

    def name(self) -> str:
        return "Farming Simulator 25 Support"

    def author(self) -> str:
        return "Cram42"

    def version(self) -> VersionInfo:
        return VersionInfo("1.0.0")

    def description(self) -> str:
        return "Game support for Farming Simulator 25. Requires installer_giants."

    def settings(self) -> list[PluginSetting]:
        return []

    def init(self, organizer: IOrganizer) -> bool:
        self._organizer = organizer
        return True

    # IPluginGame Implementation

    def gameName(self) -> str:
        return "Farming Simulator 25"

    def gameShortName(self) -> str:
        return "farm25"

    def validShortNames(self) -> list[str]:
        return []

    def nexusGameID(self) -> int:
        return 0

    def gameDirectory(self) -> QDir:
        return QDir(self._gamePath)

    def setGamePath(self, path: str) -> None:
        self._gamePath = path

    def dataDirectory(self) -> QDir:
        docsPath = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DocumentsLocation
            )
        )
        dataPath = docsPath.joinpath("My Games/FarmingSimulator2025")
        modsPath = dataPath.joinpath("mods")
        return QDir(str(modsPath))

    def documentsDirectory(self) -> QDir:
        return QDir()

    def savesDirectory(self) -> QDir:
        return QDir()

    def binaryName(self) -> str:
        return "FarmingSimulator2025.exe"

    def binaryPath(self) -> str:
        return str(
            Path(self.gameDirectory().absolutePath()).joinpath(self.binaryName())
        )

    def gameIcon(self) -> QIcon:
        return getIconForExecutable(self.binaryPath())

    def gameVersion(self) -> str:
        return getFileVersion(self.binaryPath())

    def isInstalled(self) -> bool:
        return bool(self._gamePath)

    def getLauncherName(self) -> str:
        return ""

    def executables(self) -> list[ExecutableInfo]:
        execs: list[ExecutableInfo] = []
        execs.append(
            ExecutableInfo(
                self.gameName(),
                self.gameDirectory().absoluteFilePath(self.binaryName()),
            )
        )
        execs.append(
            ExecutableInfo(
                "Dedicated Server",
                self.gameDirectory().absoluteFilePath("dedicatedServer.exe"),
            )
        )
        if self.gameDirectory().exists("Run_FarmingSimulator25.exe"):
            execs.append(
                ExecutableInfo(
                    "Launcher",
                    self.gameDirectory().absoluteFilePath("Run_FarmingSimulator25.exe"),
                )
            )
        return execs

    def executableForcedLoads(self) -> list[ExecutableForcedLoadSetting]:
        return []

    def getSupportURL(self) -> str:
        return ""

    def detectGame(self) -> None:
        pass

    def looksValid(self, directory: QDir) -> bool:
        return directory.exists(self.binaryName())

    def initializeProfile(self, directory: QDir, settings: ProfileSetting) -> None:
        pass

    def listSaves(self, folder: QDir) -> list[ISaveGame]:
        return []

    def setGameVariant(self, variant: str) -> None:
        pass
