import re

from PyQt6.QtCore import qInfo

from mobase import FileTreeEntry, IFileTree, ModDataChecker


class FS25ModDataChecker(ModDataChecker):
    def dataLooksValid(self, filetree: IFileTree) -> ModDataChecker.CheckReturn:
        if len(filetree) > 1:
            qInfo("Invalid: Must only have a single top-level item")
            return ModDataChecker.CheckReturn.INVALID

        for rootEntry in filetree:
            if not rootEntry.fileType() == FileTreeEntry.FileTypes.DIRECTORY:
                qInfo("Invalid: Top-level item must be a directory")
                return ModDataChecker.CheckReturn.INVALID

            if not rootEntry.name().startswith("FS25_"):
                qInfo('Invalid: Directory must start with "FS25_"')
                return ModDataChecker.CheckReturn.INVALID

            if not re.match(r"^[\w|_]+$", rootEntry.name()):
                qInfo("Invalid: Name must contain only alphanumeric or underscore")
                return ModDataChecker.CheckReturn.INVALID

            manifestPath = rootEntry.name() + "/modDesc.xml"
            if not filetree.exists(manifestPath, FileTreeEntry.FileTypes.FILE):
                qInfo('Invalid: modDesc.xml not found"')
                return ModDataChecker.CheckReturn.INVALID

        return ModDataChecker.CheckReturn.VALID
