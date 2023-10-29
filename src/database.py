from typing import List


class Database:
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

        # TO IMPLEMENT

        return ''

    def get_subscribed_services(self, user_id) -> List[str]:
        """
        Function which retrieves all services subscribed by user
        :param self:
        :param user_id:
        :return: list of names of subscribed services
        """

        # TO IMPLEMENT

        return []

    def get_not_subscribed_services(self, user_id) -> List[str]:
        """
        Function which retrieves all services NOT subscribed by user
        :param self:
        :param user_id:
        :return: list of names of NOT subscribed services
        """

        # TO IMPLEMENT

        return []

    def get_user_surname(self, user_id) -> str:
        """
        Function returning the user surname
        :param self:
        :param user_id:
        :return: user surname as string
        """

        # TO IMPLEMENT

        return ''
