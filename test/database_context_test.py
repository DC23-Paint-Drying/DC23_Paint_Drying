import uuid
import unittest

from src.bundle_info import BundleInfo
from src.client_info import ClientInfo
import src.database_context
from src.user_dto import Gender, UserDto

class DataBaseContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.context = src.database_context.DatabaseContext("db")

    def tearDown(self) -> None:
        self.context.destroy()

    def test_read_write(self):
        user = UserDto("testName", "testFirstName", "testSurname", "test@email.com", Gender("other"))
        bundles = [BundleInfo(str(uuid.uuid4()), "test@email.com", "YellowPaintPremium", "1980-01-01", "2040-12-20"), BundleInfo(str(uuid.uuid4()), "test@email.com", "NoAds", "1980-01-01", "2040-12-20")]
        info = ClientInfo(user, "basic", bundles)
        assert user.username == "testName"
        assert user.name== "testFirstName"
        assert user.surname == "testSurname"
        assert user.email == "test@email.com"
        assert user.gender == Gender("other")


        assert len(bundles) == 2

        assert bundles[0].name == "YellowPaintPremium"
        assert bundles[1].name == "NoAds"

        self.context.serialize(info)
        client = self.context.get_client_by_email("test@email.com")

        assert client.basic.username == "testName"
        assert client.basic.name== "testFirstName"
        assert client.basic.surname == "testSurname"
        assert client.basic.email == "test@email.com"
        assert client.basic.gender == Gender("other")

        assert client.subscription == "basic"

        assert len(client.bundles) == 2

        for bundle in client.bundles:
            assert bundle.email == "test@email.com"

        assert client.bundles[0].name == "YellowPaintPremium"
        assert client.bundles[1].name == "NoAds"
        
