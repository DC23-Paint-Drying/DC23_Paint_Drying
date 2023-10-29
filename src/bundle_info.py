from dataclasses import dataclass

@dataclass
class BundleInfo:
    id: str
    email: str
    name: str
    date_from: str
    date_to: str
