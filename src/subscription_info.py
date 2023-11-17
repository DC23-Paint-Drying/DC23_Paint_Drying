from dataclasses import dataclass
import json


@dataclass
class SubscriptionInfo:
    subscription_level: str
    subscription_timestamp: str

    def to_json(self) -> str:
        return json.dumps(self.__dict__)
