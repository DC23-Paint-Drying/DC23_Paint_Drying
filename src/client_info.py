from dataclasses import dataclass

from . import user_dto, bundle_info, subscription_info


@dataclass
class ClientInfo:
    basic: user_dto.UserDto
    subscription: subscription_info.SubscriptionInfo
    bundles: list[bundle_info.BundleInfo]
