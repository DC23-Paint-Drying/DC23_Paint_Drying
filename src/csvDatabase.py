import csv
import os
import shutil
from tempfile import NamedTemporaryFile
from typing import List
from typing import Dict
from typing import Callable


class CSVDatabase:
    def __init__(self, filename: str, fields: List[str] = None) -> None:
        """
        Creates the CSV Database object

        :param filename: Path to the database file. A new file will be created if it does not exist
        :param fields: List of headers of the csv file. Can be automatically read from the file if left as None.
            Header "id" is required.
        """

        self._filename = filename
        self._fields = fields

        if self._fields is None:
            if not os.path.isfile(self._filename):
                raise ValueError("CSV fields must be provided when first creating the file.")
            self._read_headers()

        if "id" not in self._fields:
            raise KeyError("Field \"id\" is required.")

        if not os.path.isfile(self._filename):
            self._initialize_file()

    def _initialize_file(self) -> None:
        """
        Creates a new csv database file, with headers but no client data
        """
        with open(self._filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self._fields)
            writer.writeheader()

    def _read_headers(self):
        """
        Initializes self._fields with values read from the database csv file's headers
        """
        with open(self._filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self._fields = reader.fieldnames

    def add_client(self, client_data: Dict) -> None:
        """
        Adds new client data to the database. Raises KeyError if client with that id already exists

        :param client_data: Dictionary containing the new client's data. Must have an "id" key.
        """
        if self.get_client(client_data["id"]):
            raise KeyError(f"Client with id {client_data['id']} already exists.")

        with open(self._filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self._fields)

            writer.writerow(client_data)

    def get_client(self, client_id: str) -> Dict | None:
        """
        Returns a client with the provided id, or None if client with that id does not exist in the database

        :param client_id: ID of the client to fetch from the database
        """
        with open(self._filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=self._fields)
            for data in reader:
                if data["id"] == client_id:
                    return data

        return None

    def update_client(self, client_data: Dict) -> None:
        """
        Replaces client data with id == client_data["id"] and replaces it with the provided client_data.
        Raises KeyError if client with that id does not exist.

        :param client_data: New client data to replace the previous one
        """
        if not self.get_client(client_data["id"]):
            raise KeyError(f"Client with id {client_data['id']} does not exists.")

        tempfile = NamedTemporaryFile(mode='w', delete=False, newline='')

        with open(self._filename, 'r', newline='') as csvfile, tempfile:
            reader = csv.DictReader(csvfile, fieldnames=self._fields)
            writer = csv.DictWriter(tempfile, fieldnames=self._fields)
            for data in reader:
                if data["id"] == client_data["id"]:
                    writer.writerow(client_data)
                else:
                    writer.writerow(data)
        shutil.move(tempfile.name, self._filename)

    def remove_client(self, client_id: str) -> None:
        """
        Removes client with the provided id from the database

        :param client_id: ID of the client to be removed
        """
        if not self.get_client(client_id):
            raise KeyError(f"Client with id {client_id} does not exists.")

        tempfile = NamedTemporaryFile(mode='w', delete=False, newline='')

        with open(self._filename, 'r', newline='') as csvfile, tempfile:
            reader = csv.DictReader(csvfile, fieldnames=self._fields)
            writer = csv.DictWriter(tempfile, fieldnames=self._fields)
            for data in reader:
                if data["id"] == client_id:
                    pass
                else:
                    writer.writerow(data)
        shutil.move(tempfile.name, self._filename)

    def get_clients(self, predicate: Callable[[Dict], bool] = None) -> List:
        """
        Returns a list of all clients whose data matches the predicate

        Example usage - find all clients with "gold" subscription:
            clients = db.get_clients(lambda client: client["subscription"] == "gold")

        :param predicate: A predicate tested against every client's data.
        """
        clients = []

        with open(self._filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=self._fields)

            next(reader)  # skip headers row
            for data in reader:
                if predicate is None or predicate(data):
                    clients.append(data)

        return clients

    def drop_database(self) -> None:
        """
        Deletes the database file
        """
        if os.path.isfile(self._filename):
            os.remove(self._filename)
