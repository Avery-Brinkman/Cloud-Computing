class UserFile:
    def __init__(self, id: int, fileName: str, uploader: int):
        self.id = id
        self.fileName = fileName
        self.uploader = uploader
        self.localName = f"{self.id}_{self.fileName}"
