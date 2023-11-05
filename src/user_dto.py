import random
from dataclasses import dataclass, asdict, field
import json
import uuid
import xml.etree.ElementTree


@dataclass
class UserDto:
    """
    Data class for storing user information.

    Attributes:
    - username (str): The username of the user.
    - name (str): The user's first name.
    - surname (str): The user's last name.
    - age (int): The user's age.
    - email (str): The user's email address, treated as the user's ID.
    - gender (str): The user's gender.
    - timestamp (str): The timestamp when the user data was created.
    - subscription (str): The name of subscribed subcription.
    - id (str): A unique identifier for the user.
    """

    username: str
    name: str
    surname: str
    age: int
    email: str
    gender: str
    timestamp: str
    subscription: str = ''
    packets: [str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_json(self):
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

    def to_xml(self):
        user_element = xml.etree.ElementTree.Element("User")
        for key, value in asdict(self).items():
            element = xml.etree.ElementTree.Element(key)
            element.text = str(value)
            user_element.append(element)
        return xml.etree.ElementTree.tostring(user_element).decode()

    @classmethod
    def from_xml(cls, xml_str):
        user_element = xml.etree.ElementTree.fromstring(xml_str)
        data = {}
        for element in user_element:
            key = element.tag
            value = element.text
            if value is not None and value.isdigit():
                value = int(value)
            else:
                if value is None:
                    value = ''
                # if data[i] is a list
                if '[' in value:
                    value = value.replace('[','').replace(']','')
                    if value == '':
                        value = []
                    else:
                        value = value.split('.')
            data[key] = value
        return cls(**data)

    def to_csv(self):
        return f"{self.username},{self.name},{self.surname},{self.age},{self.email},{self.gender},{self.timestamp},{self.subscription},[{'.'.join(self.packets)}],{self.id}\n"

    @classmethod
    def from_csv(cls, csv_str):
        data = csv_str.strip().split(',')
        for i in range(len(data)):
            if data[i].isdigit():
                data[i] = int(data[i])
            else:
                # if data[i] is a list
                if '[' in data[i]:
                    data[i] = data[i].replace('[','').replace(']','')
                    if data[i] == '':
                        data[i] = []
                    else:
                        data[i] = data[i].split('.')

        return cls(*data)

    def to_dict(self) -> dict :
        dict = {}
        dict['username'] = self.username
        dict['name'] = self.name
        dict['surname'] = self.surname
        dict['age'] = self.age
        dict['email'] = self.email
        dict['gender'] = self.gender
        dict['timestamp'] = self.timestamp
        dict['subscription'] = self.subscription
        dict['packets'] = self.packets
        dict['id'] = self.id
        return dict
