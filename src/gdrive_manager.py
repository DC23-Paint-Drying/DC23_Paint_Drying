import logging
import os

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


class GdriveManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(format="%(levelname)s:%(asctime)s: %(message)s", level=logging.INFO)
        self.drive = GoogleDrive(self.login_with_service_account())

    def login_with_service_account(self) -> GoogleAuth:
        """
        Google Drive service with a service account.
        note: for the service account to work, you need to share the folder or
        files with the service account email.
        """
        config_path = os.environ.get("CONFIG_FILE_PATH", "")
        settings = {
            "client_config_backend": "service",
            "service_config": {
                "client_json_file_path": config_path,
            }
        }
        gauth = GoogleAuth(settings=settings)
        gauth.ServiceAuth()
        return gauth

    def search_for_id(self, name: str, parent_id: str = 'root') -> str:
        """
        Finds a file or directory and if it exists then returns its id
        :param name: name of a searched file or directory
        :param parent_id: id of a parent directory
        """
        if name != '':
            file_list = self.drive.ListFile({'q': f"'{parent_id}' in parents and trashed=false"}).GetList()
            for file in file_list:
                if file['title'] == name:
                    return file['id']
        return ''

    def read_file(self, filename: str, directory_name: str = '') -> str:
        """
        Reads file from Google Drive.
        :param filename: name of a file
        :param directory_name: name of a directory with file
        """
        dir_id = self.search_for_id(name=directory_name)
        if dir_id == '':
            self.logger.info(f"Directory {directory_name} doesn't exist. Using root id")
            dir_id = 'root'
        file_id = self.search_for_id(filename, parent_id=dir_id)
        file = self.drive.CreateFile({'id': file_id})
        file.GetContentFile(filename)
        return filename

    def create_directory(self, directory_name: str) -> str:
        """
        Creates new directory.
        :param directory_name: name of a directory to create
        """
        file_metadata = {
            'title': directory_name,
            'parents': [{'id': 'root'}],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        directory = self.drive.CreateFile(file_metadata)
        directory.Upload()
        self.logger.info(directory['id'])
        self.logger.info(directory['title'])
        return directory['id']

    def upload_file(self, filename: str, directory_name: str) -> None:
        """
        Uploads new file to Google Drive
        :param filename: name of a file to upload
        :param directory_name: name of a directory where file will be stored
        """
        self.logger.info(f"Uploading file {filename}")
        dir_id = self.search_for_id(name=directory_name) if directory_name != '' else 'root'
        if dir_id == '':
            self.logger.info(f"Directory {directory_name} doesn't exist. Creating directory")
            dir_id = self.create_directory(directory_name=directory_name)
        file = self.drive.CreateFile({'title': filename, 'parents': [{'id': dir_id}]})
        file.SetContentFile(filename)
        file.Upload()

    def update_file(self, filename: str, directory_name: str = '') -> None:
        """
        Updates file if it exists, else creates new file
        :param filename: name of an updated file
        :param directory_name: name of a directory with a file
        """
        dir_id = self.search_for_id(name=directory_name) if directory_name != '' else 'root'
        if dir_id == '':
            self.logger.info(f"Directory {directory_name} doesn't exist. Saving file at root")
            dir_id = 'root'
        file_id = self.search_for_id(name=filename, parent_id=dir_id)
        if file_id == '':
            self.logger.info(f"File {filename} doesn't exist. Uploading new file")
            self.upload_file(filename=filename, directory_name=directory_name)
        else:
            self.logger.info(f"Updating file")
            file = self.drive.CreateFile({'title': filename, 'id': file_id, 'parents': [dir_id]})
            file.SetContentFile(filename)
            file.Upload()

    def list_files(self, directory_name: str = '') -> list[str]:
        dir_id = self.search_for_id(name=directory_name) if directory_name != '' else 'root'
        if dir_id != '':
            file_list = self.drive.ListFile({'q': f"'{dir_id}' in parents and trashed=false"}).GetList()
            return [file['title'] for file in file_list]
        else:
            self.logger.info(f"Directory {directory_name} doesn't exist")
            return []

    def drop_gdrive(self):
        file_list = self.drive.ListFile({'q': f"'root' in parents and trashed=false"}).GetList()
        self.logger.info("Removing all files")
        for file in file_list:
            file.Delete()
