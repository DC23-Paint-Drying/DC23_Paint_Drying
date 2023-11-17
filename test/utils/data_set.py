from src.bundle_info import BundleInfo
from src.client_info import ClientInfo
from src.subscription_info import SubscriptionInfo
from src.user_dto import UserDto


def generate_male_client_info() -> ClientInfo:
    user = UserDto("testName", "testFirstName", "testSurname", 99, "test@email.com", "male", "2023-01-01 00:00:00")
    subscription = SubscriptionInfo('basic', "2023-01-01 00:00:00")
    bundles = [BundleInfo("test@email.com", "monthly", "1980-01-01", "2040-12-20"),
               BundleInfo("test@email.com", "family", "1980-01-01", "2040-12-20")]
    info = ClientInfo(user, subscription, bundles)
    return info


def generate_female_client_info() -> ClientInfo:
    user = UserDto("testName", "testFirstName", "testSurname", 99, "test@email.com", "female", "2023-01-01 00:00:00")
    subscription = SubscriptionInfo('basic', "2023-01-01 00:00:00")
    bundles = []
    info = ClientInfo(user, subscription, bundles)
    return info


def generate_other_client_info() -> ClientInfo:
    user = UserDto("testName", "testFirstName", "testSurname", 99, "test@email.com", "other", "2023-01-01 00:00:00")
    subscription = SubscriptionInfo('basic', "2023-01-01 00:00:00")
    bundles = [BundleInfo("test@email.com", "monthly", "1980-01-01", "2040-12-20"),
               BundleInfo("test@email.com", "family", "1980-01-01", "2040-12-20")]
    info = ClientInfo(user, subscription, bundles)
    return info
