"""
    Module used for quering stored user data
"""
import os
import inspect
from dataclasses import asdict

from .bundle_info import BundleInfo
from .client_info import ClientInfo
from .user_dto import UserDto
from . import csvDatabase


class DatabaseContext:
    """
        Instance of this class is used for quering stored user data
    """
    def __init__(self, db_path: str) -> None:
        """
            Create database context used for storing user data
            
            Arguments:
                db_path: str
                    Relative path to folder containing database files
        """
        self.db_path = db_path
        if not os.path.isdir(db_path):
            os.mkdir(db_path)
        self.basic_db = csvDatabase.CSVDatabase(self.db_path + "/basic.txt", list(inspect.signature(UserDto).parameters) + ["subscription"])
        self.bundle_db = csvDatabase.CSVDatabase(self.db_path + "/bundles.txt", list(inspect.signature(BundleInfo).parameters))

    def get_client_by_email(self, email: str) -> ClientInfo:
        """
            Get client data class which coresponds to specified email address

            Arguments:
                email: str
                    Used as key for retrieving client data
            Returns:
                ClientInfo
        """
        data = self.basic_db.get_entry_by_field("email", email)[0]
        sub_info = data["subscription"]
        data.pop("subscription")
        bundle_info = self.bundle_db.get_entry_by_field("email", email)
        return ClientInfo(UserDto(**data), sub_info, [BundleInfo(**bundle) for bundle in bundle_info])

    def serialize(self, client: ClientInfo) -> None:
        """
            Save client data on disk

            Arguments:
                client: ClientInfo
                    Data to be saved on disk
            Returns:
                None
        """
        client_info = asdict(client.basic)
        client_info["subscription"] = client.subscription
        try:
            self.basic_db.update_client(client_info)
        except KeyError:
            self.basic_db.add_client(client_info)
        for bundle in client.bundles:
            try:
                self.bundle_db.update_client(asdict(bundle))
            except KeyError:
                self.bundle_db.add_client(asdict(bundle))

    def destroy(self):
        """
            Removes all data on disk (unreversable action)
        """
        self.basic_db.drop_database()
        self.bundle_db.drop_database()
        os.rmdir(self.db_path)
