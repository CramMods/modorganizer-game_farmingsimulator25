import winreg
from pathlib import Path
from typing import TypedDict, cast

import vdf

from .detector import IGameDetector


class _AppManifestContent(TypedDict):
    appid: str
    name: str
    installdir: str


class _AppManifest(TypedDict):
    AppState: _AppManifestContent


class _LibraryFolder(TypedDict):
    path: str


class _LibraryFolders(TypedDict):
    libraryfolders: dict[str, _LibraryFolder]


class AppManifest:
    _data: _AppManifest
    _path: Path

    def __init__(self, path: str | Path):
        self._path = Path(path)
        with open(path, "r", encoding="utf-8") as f:
            self._data = cast(_AppManifest, vdf.parse(f, _AppManifest))  # type: ignore

    def id(self) -> int:
        return int(self._data["AppState"]["appid"])

    def name(self) -> str:
        return self._data["AppState"]["name"]

    def installPath(self) -> Path:
        return self._path.parent.joinpath(
            "common",
            self._data["AppState"]["installdir"],
        )


class LibraryFolders:
    _data: _LibraryFolders

    def __init__(self, path: str | Path):
        with open(path, "r", encoding="utf-8") as f:
            self._data = cast(_LibraryFolders, vdf.parse(f, _LibraryFolders))  # type: ignore

    def paths(self) -> list[Path]:
        return [Path(lf["path"]) for lf in self._data["libraryfolders"].values()]


class SteamGameDetector(IGameDetector):
    APPID: int = 2300320

    def detect(self) -> str | None:
        for app in self.getSteamApps():
            if app.id() == self.APPID:
                return str(app.installPath().absolute())
        return None

    def getSteamPath(self) -> Path | None:
        try:
            with winreg.OpenKeyEx(
                winreg.HKEY_CURRENT_USER, "Software\\Valve\\Steam"
            ) as key:
                value, valueType = winreg.QueryValueEx(key, "SteamExe")
                if valueType == winreg.REG_SZ:
                    return Path(value).parent
                else:
                    return None
        except FileNotFoundError:
            return None

    def getLibraryPaths(self) -> list[Path]:
        steamPath = self.getSteamPath()
        if steamPath is None:
            return []
        vdfPath = steamPath.joinpath("steamapps", "libraryfolders.vdf")
        return LibraryFolders(vdfPath).paths()

    def getSteamApps(self) -> list[AppManifest]:
        manifests: list[AppManifest] = []

        libraryPaths = self.getLibraryPaths()
        for libraryPath in libraryPaths:
            manifestPaths = libraryPath.joinpath("steamapps").glob("appmanifest_*.acf")
            for manifestPath in manifestPaths:
                manifests.append(AppManifest(manifestPath))

        return manifests
