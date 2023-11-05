import uuid
import unittest
import json

from src.bundle_info import BundleInfo
from src.client_info import ClientInfo
import src.database_context
from src.subscription_info import SubscriptionInfo
from src.user_dto import UserDto
from src import manifest


class DataBaseContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.context = src.database_context.DatabaseContext("db")

    def tearDown(self) -> None:
        self.context.destroy()

    def test_json_serialization(self):
        user = UserDto("testName", "testFirstName", "testSurname", 99, "test@email.com", "other", "2023-01-01 00:00:00")
        subscription = SubscriptionInfo('basic', "2023-01-01 00:00:00")
        bundles = [BundleInfo(str(uuid.uuid4()), "test@email.com", "monthly", "1980-01-01", "2040-12-20"),
                   BundleInfo(str(uuid.uuid4()), "test@email.com", "family", "1980-01-01", "2040-12-20")]
        info = ClientInfo(user, subscription, bundles)
        data = json.loads(info.to_json())
        assert data["basic"]["name"] == "testFirstName"
        assert data["subscription"]["subscription_level"] == manifest.SUBSCRIPTIONS["basic"]["name"]
        assert data["bundles"][0]["name"] == manifest.PACKETS["monthly"]["name"]


    def test_read_write(self):
        user = UserDto("testName", "testFirstName", "testSurname", 99, "test@email.com", "other", "2023-01-01 00:00:00")
        subscription = SubscriptionInfo('basic', "2023-01-01 00:00:00")
        bundles = [BundleInfo(str(uuid.uuid4()), "test@email.com", "YellowPaintPremium", "1980-01-01", "2040-12-20"),
                   BundleInfo(str(uuid.uuid4()), "test@email.com", "NoAds", "1980-01-01", "2040-12-20")]
        info = ClientInfo(user, subscription, bundles)
        assert user.username == "testName"
        assert user.name == "testFirstName"
        assert user.surname == "testSurname"
        assert user.age == 99
        assert user.email == "test@email.com"
        assert user.gender == "other"
        assert user.timestamp == "2023-01-01 00:00:00"

        assert subscription.subscription_level == 'basic'
        assert subscription.subscription_timestamp == "2023-01-01 00:00:00"

        assert len(bundles) == 2

        assert bundles[0].name == "YellowPaintPremium"
        assert bundles[1].name == "NoAds"

        self.context.serialize(info)
        client = self.context.get_client_by_email("test@email.com")

        assert client.basic.username == "testName"
        assert client.basic.name == "testFirstName"
        assert client.basic.surname == "testSurname"
        assert client.basic.age == "99"
        assert client.basic.email == "test@email.com"
        assert client.basic.gender == "other"
        assert client.basic.timestamp == "2023-01-01 00:00:00"

        assert client.subscription.subscription_level == "basic"
        assert client.subscription.subscription_timestamp == "2023-01-01 00:00:00"

        assert len(client.bundles) == 2

        for bundle in client.bundles:
            assert bundle.email == "test@email.com"

        assert client.bundles[0].name == "YellowPaintPremium"
        assert client.bundles[1].name == "NoAds"
