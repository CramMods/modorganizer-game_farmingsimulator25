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

from .gamedetector import IGameDetector, SteamGameDetector
from .moddatachecker import FS25ModDataChecker
from .moddatacontent import FS25ModDataContent


class FS25GamePlugin(IPluginGame):
    _gamePath: str = ""
    _organizer: IOrganizer
    _gameDetectors: list[IGameDetector] = [
        SteamGameDetector(),
    ]

    # IPlugin Implementation

    def name(self) -> str:
        return "Farming Simulator 25 Support"

    def localizedName(self) -> str:
        # TODO: Translation stuff
        return self.name()

    def author(self) -> str:
        return "Cram42"

    def version(self) -> VersionInfo:
        return VersionInfo("1.3.0")

    def description(self) -> str:
        return "Game support for Farming Simulator 25."

    def settings(self) -> list[PluginSetting]:
        return []

    def init(self, organizer: IOrganizer) -> bool:
        self._organizer = organizer
        self._organizer.gameFeatures().registerFeature(
            self, FS25ModDataChecker(), 0, True
        )
        self._organizer.gameFeatures().registerFeature(
            self, FS25ModDataContent(), 0, True
        )
        return True

    # IPluginGame Implementation

    def gameName(self) -> str:
        return "Farming Simulator 25"

    def gameShortName(self) -> str:
        return "farmingsimulator25"

    def validShortNames(self) -> list[str]:
        return ["FS25"]

    def nexusGameID(self) -> int:
        return 7052

    def gameDirectory(self) -> QDir:
        return QDir(self._gamePath)

    def setGamePath(self, path: str) -> None:
        self._gamePath = path

    def dataDirectory(self) -> QDir:
        return QDir(self.dataRootDirectory().absoluteFilePath("mods"))

    def documentsDirectory(self) -> QDir:
        return self.dataRootDirectory()

    def savesDirectory(self) -> QDir:
        return self.dataRootDirectory()

    def binaryName(self) -> str:
        return "FarmingSimulator2025.exe"

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
                self.binaryPath(),
            )
        )
        execs.append(
            ExecutableInfo(
                "Dedicated Server",
                self.gameDirectory().absoluteFilePath("dedicatedServer.exe"),
            )
        )
        return execs

    def executableForcedLoads(self) -> list[ExecutableForcedLoadSetting]:
        return []

    def getSupportURL(self) -> str:
        return "https://www.farming-simulator.com/"

    def detectGame(self) -> None:
        for detector in self._gameDetectors:
            path = detector.detect()
            if path is not None:
                self.setGamePath(path)
                break

    def looksValid(self, directory: QDir) -> bool:
        return directory.exists(self.binaryName())

    def initializeProfile(self, directory: QDir, settings: ProfileSetting) -> None:
        pass

    def listSaves(self, folder: QDir) -> list[ISaveGame]:
        return []

    def setGameVariant(self, variant: str) -> None:
        pass

    # Extra

    def binaryPath(self) -> str:
        return self.gameDirectory().absoluteFilePath(self.binaryName())

    def dataRootDirectory(self) -> QDir:
        docsDir = QDir(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DocumentsLocation
            )
        )
        return QDir(docsDir.absoluteFilePath("My Games/FarmingSimulator2025"))
