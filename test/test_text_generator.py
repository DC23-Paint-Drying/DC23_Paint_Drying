import unittest
from unittest.mock import MagicMock
import src.text_generator as text_gen
from src.text_generator import Database


class InvoiceMock:
    products = []
    number = 0
    payment = 'VISA/Mastercard - 1234'
    date = ''
    price = 0


class TestReplaceKeywords(unittest.TestCase):
    def test_greeting(self):
        database = Database()
        database.get_user_sex = MagicMock(return_value='M')
        database.get_user_surname = MagicMock(return_value='Wierzba')

        assert text_gen.replace_keywords('{$greeting}', 1, database) == 'Dear Mr Wierzba'

    def test_propose_new_service(self):
        database = Database()

        # test when all is bought
        database.get_subscribed_services = MagicMock(return_value=['a', 'b', 'c'])
        database.get_not_subscribed_services = MagicMock(return_value=[])
        assert text_gen.replace_keywords('{$proposeNewService}', 1,
                                         database) == ('It seems, you are one of our best customers! You\'ve bought '
                                                       'all of our services! Stay tuned for more!')

        # test when there is anything to suggest, but something is bought
        database.get_subscribed_services = MagicMock(return_value=['a', 'b', 'c'])
        database.get_not_subscribed_services = MagicMock(return_value=['d', 'e'])
        assert text_gen.replace_keywords('{$proposeNewService}', 1,
                                         database) == ('It seems, you are very interested in service a. You should '
                                                       'also check these services: d, e!')

        # test when nothing is bought, but there are more than 2 services in total
        database.get_subscribed_services = MagicMock(return_value=[])
        database.get_not_subscribed_services = MagicMock(return_value=['a', 'b', 'c'])
        assert text_gen.replace_keywords('{$proposeNewService}', 1,
                                         database) == 'Looking for new action? Check our best services: a, b, c!'

        # test when nothing is bought, but there are less than 3 services in total
        database.get_subscribed_services = MagicMock(return_value=[])
        database.get_not_subscribed_services = MagicMock(return_value=['a', 'b'])
        assert text_gen.replace_keywords('{$proposeNewService}', 1,
                                         database) == 'Looking for new action? Check our best services: a, b!'

    def test_proposeLengtheningSubscription(self):
        database = Database()
        database.get_subscribed_services = MagicMock(return_value=['abb', 'b', 'c', 'd', 'e'])

        assert text_gen.replace_keywords('{$proposeLengtheningSubscription}', 1,
                                         database) == ('The subscription for abb will soon expire! Quick! Renew the '
                                                       'subscription!')

    def test_suggestContact(self):
        database = Database()

        assert text_gen.replace_keywords('{$suggestContact}', 1,
                                         database) == ('We are glad, you are interested in our services. For more '
                                                       'information, we suggest visiting our website to check new '
                                                       'products we offer!')

    def test_goodbye(self):
        database = Database()

        assert text_gen.replace_keywords('{$goodbye}', 1,
                                         database) == 'Enjoy our services \nDC Drying Paint Services'

    def test_subscribedServices(self):
        database = Database()
        database.get_subscribed_services = MagicMock(return_value=['a', 'b', 'c', 'd', 'e'])

        assert text_gen.replace_keywords('{$subscribedServices}', 1, database) == 'a, b, c, d, e'

    def test_not_subscribedServices(self):
        database = Database()
        database.get_not_subscribed_services = MagicMock(return_value=['a', 'b', 'c', 'd', 'e'])

        assert text_gen.replace_keywords('{$notSubscribedServices}', 1, database) == 'a, b, c, d, e'


class TestProposeMailText(unittest.TestCase):
    def test_simple_mail(self):
        database = Database()
        database.get_user_sex = MagicMock(return_value='M')
        database.get_user_surname = MagicMock(return_value='Wierzba')
        database.get_subscribed_services = MagicMock(return_value=['abba', 'b', 'c'])
        database.get_not_subscribed_services = MagicMock(return_value=['d', 'e'])
        assert text_gen.get_propose_mail_text(1, database) == (''
                                                               'Dear Mr Wierzba\n'
                                                               '\n'
                                                               'It seems, you are very interested in service abba. '
                                                               'You should also check these '
                                                               'services: d, e!\n'
                                                               '\n'
                                                               'The subscription for abba will soon expire! Quick! '
                                                               'Renew the subscription!\n'
                                                               '\n'
                                                               'We are glad, you are interested in our services. For '
                                                               'more information, we '
                                                               'suggest visiting our website to check new products we '
                                                               'offer!\n'
                                                               '\n'
                                                               'Enjoy our services \n'
                                                               'DC Drying Paint Services')

    def test_0_subscribed_services(self):
        database = Database()
        database.get_user_sex = MagicMock(return_value='F')
        database.get_user_surname = MagicMock(return_value='Kowalska')
        database.get_subscribed_services = MagicMock(return_value=[])
        database.get_not_subscribed_services = MagicMock(return_value=['debohra', 'esda'])
        assert text_gen.get_propose_mail_text(1, database) == (''
                                                               'Dear Mrs Kowalska\n'
                                                               '\n'
                                                               'Looking for new action? Check our best services: '
                                                               'debohra, esda!\n'
                                                               '\n'
                                                               '\n'
                                                               '\n'
                                                               'We are glad, you are interested in our services. For '
                                                               'more information, we '
                                                               'suggest visiting our website to check new products we '
                                                               'offer!\n'
                                                               '\n'
                                                               'Enjoy our services \n'
                                                               'DC Drying Paint Services')

    def test_everything_subscribed(self):
        database = Database()
        database.get_user_sex = MagicMock(return_value='M')
        database.get_user_surname = MagicMock(return_value='Wierzba')
        database.get_subscribed_services = MagicMock(return_value=['abba', 'b', 'c'])
        database.get_not_subscribed_services = MagicMock(return_value=[])
        assert text_gen.get_propose_mail_text(1, database) == (''
                                                               'Dear Mr Wierzba\n'
                                                               '\n'
                                                               'It seems, you are one of our best customers! You\'ve '
                                                               'bought all of our services! Stay tuned for more!\n'
                                                               '\n'
                                                               'The subscription for abba will soon expire! Quick! '
                                                               'Renew the subscription!\n'
                                                               '\n'
                                                               'We are glad, you are interested in our services. For '
                                                               'more information, we '
                                                               'suggest visiting our website to check new products we '
                                                               'offer!\n'
                                                               '\n'
                                                               'Enjoy our services \n'
                                                               'DC Drying Paint Services')


class TestInvoice(unittest.TestCase):
    def test_one_product(self):
        database = Database()
        database.get_user_sex = MagicMock(return_value='M')
        database.get_user_surname = MagicMock(return_value='Wierzba')

        invoice = InvoiceMock()
        invoice.products = ['green']
        invoice.number = 123553
        invoice.date = '2016-08-31'
        invoice.price = 1315

        assert (text_gen.get_invoice_mail_text(1, invoice, database) ==
                ('Dear Mr Wierzba\n'
                 '\n'
                 'Thank you for your order for the following products:\n'
                 '-green\n'
                 '\n'
                 'Please find your invoice attached to this email.\n'
                 '\n'
                 'Your order\n'
                 '\n'
                 'Reference no.:\r123553\n'
                 'Payment method:\rVISA/Mastercard - 1234\n'
                 'Order date:\r2016-08-31\n'
                 'Grand total:\r1,315.00 USD\n'
                 '\n'
                 'We are glad, you are interested in our services. For more information, we '
                 'suggest visiting our website to check new products we offer!\n'
                 '\n'
                 'Enjoy our services \n'
                 'DC Drying Paint Services'))

    def test_multiple_product(self):
        database = Database()
        database.get_user_sex = MagicMock(return_value='F')
        database.get_user_surname = MagicMock(return_value='Wierzba')

        invoice = InvoiceMock()
        invoice.products = ['green', 'yellow', 'red']
        invoice.number = 123553
        invoice.date = '2016-08-31'
        invoice.price = 1315

        assert (text_gen.get_invoice_mail_text(1, invoice, database) ==
                ('Dear Mrs Wierzba\n'
                 '\n'
                 'Thank you for your order for the following products:\n'
                 '-green\n'
                 '-yellow\n'
                 '-red\n'
                 '\n'
                 'Please find your invoice attached to this email.\n'
                 '\n'
                 'Your order\n'
                 '\n'
                 'Reference no.:\r123553\n'
                 'Payment method:\rVISA/Mastercard - 1234\n'
                 'Order date:\r2016-08-31\n'
                 'Grand total:\r1,315.00 USD\n'
                 '\n'
                 'We are glad, you are interested in our services. For more information, we '
                 'suggest visiting our website to check new products we offer!\n'
                 '\n'
                 'Enjoy our services \n'
                 'DC Drying Paint Services'))
