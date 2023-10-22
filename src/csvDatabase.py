import csv
import os
import shutil
from tempfile import NamedTemporaryFile
from typing import List
from typing import Dict
from typing import Callable


class CSVDatabase:
    def __init__(self, filename: str, fields: List[str] = None) -> None:
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
        with open(self._filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self._fields)
            writer.writeheader()

    def _read_headers(self):
        with open(self._filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self._fields = reader.fieldnames

    def add_client(self, client_data: Dict) -> None:
        if self.get_client(client_data["id"]):
            raise KeyError(f"Client with id {client_data['id']} already exists.")

        with open(self._filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self._fields)

            writer.writerow(client_data)

    def get_client(self, client_id: str) -> Dict | None:
        with open(self._filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=self._fields)
            for data in reader:
                if data["id"] == client_id:
                    return data

        return None

    def update_client(self, client_data: Dict) -> None:
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
        clients = []

        with open(self._filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=self._fields)

            next(reader)  # skip headers row
            for data in reader:
                if predicate is None or predicate(data):
                    clients.append(data)

        return clients

    def drop_database(self) -> None:
        if os.path.isfile(self._filename):
            os.remove(self._filename)
