from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GDrive:

    def __init__(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self._drive = GoogleDrive(gauth)

    def load_exc_file(self, filename:str="table.xlsx") -> int:
        file = self._drive.CreateFile({'title': filename})
        file.SetContentFile(filename)
        file.Upload()
        return file['id']

    def update_loaded_file(self, file_id:str=None, filename:str="table.xlsx") -> bool:
        if file_id is None:
            raise
        try:
            file = self._drive.CreateFile({'id': file_id})
            file.SetContentFile(filename)
            file.Upload()
        except:
            return False
        else:
            return (True and self._check_file_in_trash(file_id=file_id))

    def test_check_trash(self):
        print(list(map(lambda x: x['id'], self._drive.ListFile({'q': "trashed=true"}).GetList())))

    def _check_file_in_trash(self, file_id:str=None) -> bool:
        if file_id is None:
            raise
        return file_id in list(map(lambda x: x['id'], self._drive.ListFile({'q': "trashed=true"}).GetList()))

    def _untrash(self, file_id:str=None) -> bool:
        file = self._drive.CreateFile({'id': file_id})
        file.UnTrash()
        if self._check_file_in_trash(file_id):
            return False
        return True

    def repair(self, file_id:str=None, filename:str="table.xlsx"):
        if not file_id:
            raise
        if self._untrash(file_id):
            self.load_exc_file(filename=filename)
        else:
            self.update_loaded_file(
                file_id=file_id,
                filename=filename
            )