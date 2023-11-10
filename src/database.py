from typing import List

from .database_context import DatabaseContext
from .manifest import SUBSCRIPTIONS, PACKETS


class Database:
    def __init__(self, db: DatabaseContext) -> None:
        self.db: DatabaseContext = db

    """
    Database object is used for retrieving data from the database.
    At the moment is used for generating mail text, however tested with mocks.
    """
    def get_user_sex(self, user_id: str) -> str:
        """
        Function which returns user sex
        :param user_id:
        :return: one of string values: 'M' or 'F'
        """

        client = self.db.basic_db.get_client(user_id)

        if client['gender'] == 'female':
            return 'F'
        else:
            return 'M'

    def get_subscribed_packets(self, user_id: str) -> List[str]:
        """
        Function which retrieves all services subscribed by user
        :param user_id:
        :return: list of names of subscribed services
        """

        email = self.db.basic_db.get_client(user_id)['email']
        client = self.db.get_client_by_email(email)
        names = []
        for packet in client.bundles:
            names.append(PACKETS[packet.name]['name'])

        return names

    def get_not_subscribed_packets(self, user_id: str) -> List[str]:
        """
        Function which retrieves all services NOT subscribed by user
        :param user_id:
        :return: list of names of NOT subscribed services
        """

        email = self.db.basic_db.get_client(user_id)['email']
        client = self.db.get_client_by_email(email)
        subscribed = client.bundles
        not_subscribed = []

        subscribed_packets_names = [x.name for x in subscribed]

        for packet in PACKETS.keys():
            if packet not in subscribed_packets_names:
                not_subscribed.append(PACKETS[packet]['name'])

        return not_subscribed

    def get_subscription(self, user_id: str) -> str:
        """
        Function which retrieves all services subscribed by user
        :param user_id:
        :return: list of names of subscribed services
        """

        email = self.db.basic_db.get_client(user_id)['email']
        client = self.db.get_client_by_email(email)

        return SUBSCRIPTIONS[client.subscription.subscription_level]['name']

    def get_user_surname(self, user_id: str) -> str:
        """
        Function returning the user surname
        :param user_id:
        :return: user surname as string
        """

        return self.db.basic_db.get_client(user_id)['surname']
