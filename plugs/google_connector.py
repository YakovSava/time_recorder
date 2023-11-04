from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

class GDrive:

    def __init__(self):
        gauth = GoogleAuth()
        # gauth.LocalWebserverAuth()
        self._drive = GoogleDrive(gauth)

    def send_exc_file(self, filename:str="table.xlsx") -> bool:
        file = self._drive.CreateFile({'title': filename})
        file.SetContentFile(filename)
        file.Upload()