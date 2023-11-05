import unittest
import uuid

from src.bundle_info import BundleInfo
from src.client_info import ClientInfo
from src.csvDatabase import CSVDatabase
from src.database import Database
from src.database_context import DatabaseContext
from src.subscription_info import SubscriptionInfo
from src.user_dto import UserDto

import utils.data_set as data_set


class DatabaseTests(unittest.TestCase):

    def setUp(self) -> None:
        self.context = DatabaseContext("db")
        self.db = Database(self.context)

    def tearDown(self) -> None:
        self.context.destroy()

    def test_get_user_sex(self):
        male_client = data_set.generate_male_client_info()
        female_client = data_set.generate_female_client_info()
        self.context.serialize(male_client)
        self.context.serialize(female_client)

        assert self.db.get_user_sex(male_client.basic.id) == 'M'
        assert self.db.get_user_sex(female_client.basic.id) == 'F'


    def test_get_subscribed_packets(self):
        male_client = data_set.generate_male_client_info()
        self.context.serialize(male_client)

        assert self.db.get_subscribed_packets(male_client.basic.id) == ['Miesięczny','Rodzinny']


    def test_get_not_subscribed_packets(self):
        female_client = data_set.generate_female_client_info()
        self.context.serialize(female_client)

        assert self.db.get_not_subscribed_packets(female_client.basic.id) == ['Miesięczny','Rodzinny']

    def test_get_subscription(self):
        male_client = data_set.generate_male_client_info()
        self.context.serialize(male_client)
        assert self.db.get_subscription(male_client.basic.id) == 'Podstawowy'

    def test_get_user_surname(self):
        male_client = data_set.generate_male_client_info()
        self.context.serialize(male_client)
        assert self.db.get_user_surname(male_client.basic.id) == 'testSurname'
