from dataclasses import dataclass

from . import user_dto, bundle_info

@dataclass
class ClientInfo:
    basic: user_dto.UserDto
    subscription: str
    bundles: list[bundle_info.BundleInfo]
