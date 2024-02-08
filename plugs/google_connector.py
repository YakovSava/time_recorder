from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


class GDrive:

    def __init__(self, service:bool=True):
        if service:
            settings = {
                "client_config_backend": "service",
                "service_config": {
                    "client_json_file_path": "service_secrets.json",
                }
            }

            gauth = GoogleAuth(settings=settings)

            gauth.ServiceAuth()
        else:
            gauth = GoogleAuth()

            gauth.LoadCredentialsFile("credentials.txt")
            if gauth.credentials is None:
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                gauth.Refresh()
            else:
                gauth.Authorize()
            gauth.SaveCredentialsFile("credentials.txt")
        self._drive = GoogleDrive(gauth)

    def load_file(self, filename: str="table.xlsx") -> int:
        file = self._drive.CreateFile({'title': filename})
        file.SetContentFile(filename)
        file.Upload()
        return file['id']

    def update_loaded_file(self, file_id: str=None, filename: str="table.xlsx") -> bool:
        if file_id is None:
            raise
        try:
            file = self._drive.CreateFile({'id': file_id})
            file.SetContentFile(filename)
            file.Upload()
        except Exception as ex:
            # print(ex)
            return False
        else:
            trs = self._check_file_in_trash(file_id=file_id)
            #print('File in trash - ', trs)
            return True and (not trs)

    def test_check_trash(self):
        print('Files in trash - ',
              list(map(lambda x: x['id'], self._drive.ListFile({'q': "trashed=true"}).GetList())))

    def _check_file_in_trash(self, file_id: str=None) -> bool:
        if file_id is None:
            raise
        return file_id in list(map(lambda x: x['id'], self._drive.ListFile({'q': "trashed=true"}).GetList()))

    def _untrash(self, file_id: str=None) -> bool:
        try:
            file = self._drive.CreateFile({'id': file_id})
            file.UnTrash()
            if self._check_file_in_trash(file_id):
                return False
            return True
        except:
            return False

    def repair(self, file_id: str=None, filename: str="table.xlsx") -> None or str:
        if not file_id:
            raise
        tmp = self._untrash(file_id)
        #print('File untrash - ', tmp)
        if tmp:
            #print('File trashed')
            self.update_loaded_file(
                file_id=file_id,
                filename=filename
            )
            return
        else:
            #print("File reloaded")
            return self.load_file(filename=filename)


class GDriveTest:

    def __init__(self):
        ...

    def load_file(self, filename: str="table.xlsx") -> int:
        ...

    def update_loaded_file(self, file_id: str=None, filename: str="table.xlsx") -> bool:
        ...

    def test_check_trash(self):
        ...

    def _check_file_in_trash(self, file_id: str=None) -> bool:
        ...

    def _untrash(self, file_id: str=None) -> bool:
        ...

    def repair(self, file_id: str=None, filename: str="table.xlsx") -> None or str:
        ...
