from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

class GDrive:

    def __init__(self):
        self._drive = GoogleDrive(gauth)

    def send_exc_file(self, filename:str="table.xlsx") -> bool:
        try:
            file = self._drive.CreateFile({'title': filename})
            file.SetContentFile(filename)
            file.Upload()
        except:
            return False
        else:
            return True