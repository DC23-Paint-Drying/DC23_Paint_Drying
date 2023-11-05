from typing import List

from .csvDatabase import CSVDatabase
from .manifest import SUBSCRIPTIONS, PACKETS


class Database:
    def __init__(self, db: CSVDatabase) -> None:
        self.db: CSVDatabase = db

    """
    Database object is used for retrieving data from the database.
    At the moment is used for generating mail text, however tested with mocks.
    """
    def get_user_sex(self, user_id) -> str:
        """
        Function which returns user sex
        :param self:
        :param user_id:
        :return: one of string values: 'M' or 'F'
        """

        client = self.db.get_client(user_id)

        if client['gender'] == 'female':
            return 'F'
        else:
            return 'M'


    def get_subscribed_packets(self, user_id) -> List[str]:
        """
        Function which retrieves all services subscribed by user
        :param self:
        :param user_id:
        :return: list of names of subscribed services
        """

        client = self.db.get_client(user_id)

        packets = client['packets']

        for packet in packets:
            packet = PACKETS[packet]['name']

        return packets

    def get_not_subscribed_packets(self, user_id) -> List[str]:
        """
        Function which retrieves all services NOT subscribed by user
        :param self:
        :param user_id:
        :return: list of names of NOT subscribed services
        """

        client = self.db.get_client(user_id)
        subscribed = client['packets']
        not_subscribed = []

        for service in PACKETS.keys():
            if service not in subscribed:
                not_subscribed.append(PACKETS[service]['name'])

        return not_subscribed

    def get_subscription(self, user_id) -> str:
        """
        Function which retrieves all services subscribed by user
        :param self:
        :param user_id:
        :return: list of names of subscribed services
        """

        client = self.db.get_client(user_id)

        return SUBSCRIPTIONS[client['subscription']]['name']

    def get_user_surname(self, user_id) -> str:
        """
        Function returning the user surname
        :param self:
        :param user_id:
        :return: user surname as string
        """

        return self.db.get_client(user_id)['surname']
