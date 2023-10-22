from dataclasses import dataclass, asdict
from enum import Enum
import json
import xml.etree.ElementTree


class Gender(str, Enum):
    OTHER = 'other'
    MALE = 'male'
    FEMALE = 'female'


@dataclass
class UserDto:
    """
        Data class for storing user information.

        Attributes:
        - username (str): The username of the user.
        - name (str): The user's first name.
        - surname (str): The user's last name.
        - email (str): The user's email address, treated as the user's ID.
        - gender (Gender): The user's gender, chosen from the Gender enum.
    """
    username: str
    name: str
    surname: str
    email: str
    gender: Gender

    def to_json(self):
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        data['gender'] = Gender(data['gender'])
        return cls(**data)

    def to_xml(self):
        user_element = xml.etree.ElementTree.Element("User")
        for key, value in asdict(self).items():
            element = xml.etree.ElementTree.Element(key)
            element.text = value
            user_element.append(element)
        return xml.etree.ElementTree.tostring(user_element).decode()

    @classmethod
    def from_xml(cls, xml_str):
        user_element = xml.etree.ElementTree.fromstring(xml_str)
        data = {element.tag: element.text for element in user_element}
        data['gender'] = Gender(data['gender'])
        return cls(**data)

    def to_csv(self):
        return f"{self.username},{self.name},{self.surname},{self.email},{self.gender.value}\n"

    @classmethod
    def from_csv(cls, csv_str):
        data = csv_str.strip().split(',')
        data[-1] = Gender(data[-1])
        return cls(*data)
