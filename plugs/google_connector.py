from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GDrive:

    def __init__(self):
        gauth = GoogleAuth()
        # gauth.LocalWebserverAuth()
        self._drive = GoogleDrive(gauth)

    def load_exc_file(self, filename:str="table.xlsx") -> int:
        file = self._drive.CreateFile({'title': filename})
        file.SetContentFile(filename)
        file.Upload()
        return file['id']

    def update_loaded_file(self, file_id:int=None, filename:str="table.xlsx") -> bool:
        if file_id is None:
            raise
        try:
            file = self._drive.CreateFile({'id': file_id})
            file.SetContentFile(filename)
            file.Upload()
        except:
            return False
        else:
            return True