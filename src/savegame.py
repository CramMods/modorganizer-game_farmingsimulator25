import xml.etree.ElementTree as et

from PyQt6.QtCore import QDateTime, QDir, QFileInfo

from mobase import ISaveGame


class FS25SaveGame(ISaveGame):
    _dir: QDir
    _xml: et.Element

    def __init__(self, path: str):
        super().__init__()
        self._dir = QDir(path)
        xmlTree = et.parse(self.getMainXmlPath())
        xmlRoot = xmlTree.getroot()
        if not isinstance(xmlRoot, et.Element):
            raise Exception("Invalid XML")
        self._xml = xmlRoot

    def getFilepath(self) -> str:
        return self._dir.absolutePath()

    def getName(self) -> str:
        return self._xml.findtext("./settings/savegameName") or ""

    def allFiles(self) -> list[str]:
        files: list[str] = [self._dir.absolutePath()]
        files.extend([self._dir.absoluteFilePath(f) for f in self._dir.entryList()])
        return files

    def getSaveGroupIdentifier(self) -> str:
        return ""

    def getCreationTime(self) -> QDateTime:
        return QFileInfo(self.getMainXmlPath()).lastModified()

    def getMainXmlPath(self) -> str:
        return self._dir.absoluteFilePath("careerSavegame.xml")
