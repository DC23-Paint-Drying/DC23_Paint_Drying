from dataclasses import dataclass
import json

from . import user_dto, bundle_info, subscription_info
from . import manifest


@dataclass
class ClientInfo:
    basic: user_dto.UserDto
    subscription: subscription_info.SubscriptionInfo
    bundles: list[bundle_info.BundleInfo]

    def to_json(self, pretty_print: bool = True) -> str:
        data = {
            'basic': json.loads(self.basic.to_json()),
            'subscription': json.loads(self.subscription.to_json()),
            'bundles': [json.loads(bundle.to_json()) for bundle in self.bundles]
        }
        if pretty_print:
            del data['basic']['timestamp']
            del data['basic']['id']
            del data['subscription']['subscription_timestamp']
            data['subscription']['subscription_level'] = manifest.SUBSCRIPTIONS[data['subscription']['subscription_level']]['name']
            for bundle in data['bundles']:
                bundle['name'] = manifest.PACKETS[bundle['name']]['name']
        return json.dumps(data)
