import uuid
from dataclasses import dataclass, field
import json


@dataclass
class BundleInfo:
    email: str
    name: str
    date_from: str
    date_to: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_json(self) -> str:
        return json.dumps(self.__dict__)
