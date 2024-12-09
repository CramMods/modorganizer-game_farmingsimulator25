from mobase import FileTreeEntry, IFileTree, ModDataContent


class MeshContent(ModDataContent.Content):
    ID: int = 0

    def __init__(self):
        super().__init__(self.ID, "Meshes", ":/MO/gui/content/mesh")


class ScriptContent(ModDataContent.Content):
    ID: int = 1

    def __init__(self):
        super().__init__(self.ID, "Scripts", ":/MO/gui/content/script")


class TextureContent(ModDataContent.Content):
    ID: int = 2

    def __init__(self):
        super().__init__(self.ID, "Textures", ":/MO/gui/content/texture")


class FS25ModDataContent(ModDataContent):
    _content: list[int]

    def getAllContents(self) -> list[ModDataContent.Content]:
        return [
            MeshContent(),
            ScriptContent(),
            TextureContent(),
        ]

    def getContentsFor(self, filetree: IFileTree) -> list[int]:
        self._content = []
        filetree.walk(self.walkContent)
        return self._content

    def walkContent(self, path: str, entry: FileTreeEntry) -> IFileTree.WalkReturn:
        if entry.isFile():
            ext = entry.suffix().casefold()
            if ext == "lua":
                self._content.append(ScriptContent.ID)
            if ext == "i3d":
                self._content.append(MeshContent.ID)
            if ext == "dds":
                self._content.append(TextureContent.ID)
        return IFileTree.WalkReturn.CONTINUE
