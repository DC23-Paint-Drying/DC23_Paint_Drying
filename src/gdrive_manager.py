import logging
import os

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


class GdriveManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(format="%(levelname)s:%(asctime)s: %(message)s", level=logging.INFO)
        self.drive = GoogleDrive(self.login_with_service_account())
        self.root_dir_id = self.search_for_id('DC23_Paint_Drying')

    def login_with_service_account(self) -> GoogleAuth:
        """
        Google Drive service with a service account.
        note: for the service account to work, you need to share the folder or
        files with the service account email.
        """
        settings = {
            "client_config_backend": "service",
            "service_config": {
                "client_json_file_path": "service-secrets.json",
            }
        }
        gauth = GoogleAuth(settings=settings)
        gauth.ServiceAuth()
        return gauth

    def search_for_id(self, name: str, parent_id: str = 'root') -> str:
        file_list = self.drive.ListFile({'q': f"'{parent_id}' in parents and trashed=false"}).GetList()
        for file in file_list:
            if file['title'] == name:
                return file['id']
        return ''

    def read_file(self, filename: str, path: str) -> dict:
        """
        Reads file from Google Drive.
        :param filename: name of a file
        :param path: path to a directory with file
        """
        return {}

    def create_directory(self, directory_name: str) -> str:
        file_metadata = {
            'title': directory_name,
            'parents': [{'id': self.root_dir_id}],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        directory = self.drive.CreateFile(file_metadata)
        directory.Upload()
        self.logger.info(directory['id'])
        self.logger.info(directory['title'])
        return directory['id']

    def upload_file(self, filename: str, directory_name: str) -> None:
        dir_id = self.search_for_id(name=directory_name)
        if dir_id == '':
            self.logger.info(f"Directory {directory_name} doesn't exist. Creating directory")
            dir_id = self.create_directory(directory_name=directory_name)
        file = self.drive.CreateFile({'title': filename,
                                      'parents': [{'id': dir_id}]})
        file.SetContentFile(filename)
        file.Upload()

    def update_file(self, filename: str, directory_name: str = '') -> None:
        dir_id = self.search_for_id(name=directory_name)
        if dir_id == '':
            self.logger.info(f"Directory {directory_name} doesn't exist. Saving file at root")
            dir_id = 'root'
        file_id = self.search_for_id(name=filename, parent_id=dir_id)
        if file_id == '':
            self.logger.info(f"File {filename} doesn't exist. Uploading new file")
            self.upload_file(filename=filename, directory_name=directory_name)
        else:
            file = self.drive.CreateFile({'title': filename,
                                          'id': file_id,
                                          'parents': [dir_id]})
            file.SetContentFile(filename)
            file.Upload()


if __name__ == "__main__":
    tmp = GdriveManager()
    a = tmp.create_directory('DC23_Paint_Drying')
    print(a)
