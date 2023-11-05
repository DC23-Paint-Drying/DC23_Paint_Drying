from dataclasses import dataclass
import json

@dataclass
class BundleInfo:
    id: str
    email: str
    name: str
    date_from: str
    date_to: str

    def to_json(self) -> str:
        return json.dumps(self.__dict__)
