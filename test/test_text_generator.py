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

        assert text_gen.replace_keywords('{$greeting}', 1, database) == 'Szanowny Panie Wierzba'

    def test_propose_new_service(self):
        database = Database()

        # test when all is bought
        database.get_subscribed_services = MagicMock(return_value=['a', 'b', 'c'])
        database.get_not_subscribed_services = MagicMock(return_value=[])
        assert text_gen.replace_keywords('{$proposeNewService}', 1,
                                         database) == ('Ptaki ćwierkają, że jest Pani jedną z naszych najlepszych klientek! '
                                                       'Wykupiłaś wszystkie nasze usługi! Zachęcamy do oczekiwania na '
                                                       'nowe przyszłe usługi, które się pojawią niedługo!')

        # test when there is anything to suggest, but something is bought
        database.get_subscribed_services = MagicMock(return_value=['a', 'b', 'c'])
        database.get_not_subscribed_services = MagicMock(return_value=['d', 'e'])
        assert text_gen.replace_keywords('{$proposeNewService}', 1,
                                         database) == ('Zauważyliśmi, że jest Pani zaintereseowana usługą a. Powinnaś '
                                                       'sprawdzić także te usługi: d, e!')

        # test when nothing is bought, but there are more than 2 services in total
        database.get_subscribed_services = MagicMock(return_value=[])
        database.get_not_subscribed_services = MagicMock(return_value=['a', 'b', 'c'])
        assert text_gen.replace_keywords('{$proposeNewService}', 1,
                                         database) == 'Szukasz nowych wrażeń? Sprawdź nasze najlepsze usługi: a, b, c!'

        # test when nothing is bought, but there are less than 3 services in total
        database.get_subscribed_services = MagicMock(return_value=[])
        database.get_not_subscribed_services = MagicMock(return_value=['a', 'b'])
        assert text_gen.replace_keywords('{$proposeNewService}', 1,
                                         database) == 'Szukasz nowych wrażeń? Sprawdź nasze najlepsze usługi: a, b!'

    def test_proposeLengtheningSubscription(self):
        database = Database()
        database.get_subscribed_services = MagicMock(return_value=['abb', 'b', 'c', 'd', 'e'])

        assert text_gen.replace_keywords('{$proposeLengtheningSubscription}', 1,
                                         database) == ('Uwaga! Subskrypcja na abb wkrótce wygaśnie! Szybko! Odnów '
                                                       'subskrypcję!')

    def test_suggestContact(self):
        database = Database()

        assert text_gen.replace_keywords('{$suggestContact}', 1,
                                         database) == ('Cieszymy się, że interesuje się Pani naszymi usługami. W celu '
                                                       'uzyskania więcej informacji, zalecamy odwiedzenie naszej '
                                                       'strony,by sprawdzić nowe produkty, które oferujemy!')

    def test_goodbye(self):
        database = Database()

        assert text_gen.replace_keywords('{$goodbye}', 1,
                                         database) == 'Ciesz się naszymi usługami! \nDC Drying Paint Services'

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
                                        'Szanowny Panie Wierzba\n'
                                        '\n'
                                        'Zauważyliśmi, że jest Pan zaintereseowany usługą abba. Powinienieś sprawdzić '
                                        'także te usługi: d, e!\n'
                                        '\n'
                                        'Uwaga! Subskrypcja na abba wkrótce wygaśnie! Szybko! Odnów subskrypcję!\n'
                                        '\n'
                                        'Cieszymy się, że interesuje się Pan naszymi usługami. W celu uzyskania '
                                        'więcej informacji, zalecamy odwiedzenie naszej strony,by sprawdzić nowe '
                                        'produkty, które oferujemy!\n'
                                        '\n'
                                        'Ciesz się naszymi usługami! \n'
                                        'DC Drying Paint Services')

    def test_0_subscribed_services(self):
        database = Database()
        database.get_user_sex = MagicMock(return_value='F')
        database.get_user_surname = MagicMock(return_value='Kowalska')
        database.get_subscribed_services = MagicMock(return_value=[])
        database.get_not_subscribed_services = MagicMock(return_value=['debohra', 'esda'])
        assert text_gen.get_propose_mail_text(1, database) == (''
                                            'Szanowna Pani Kowalska\n'
                                            '\n'
                                            'Szukasz nowych wrażeń? Sprawdź nasze najlepsze usługi: debohra, esda!\n'
                                            '\n'
                                            '\n'
                                            '\n'
                                            'Cieszymy się, że interesuje się Pani naszymi usługami. W celu uzyskania '
                                            'więcej informacji, zalecamy odwiedzenie naszej strony,by sprawdzić nowe '
                                            'produkty, które oferujemy!\n'
                                            '\n'
                                            'Ciesz się naszymi usługami! \n'
                                            'DC Drying Paint Services')

    def test_everything_subscribed(self):
        database = Database()
        database.get_user_sex = MagicMock(return_value='M')
        database.get_user_surname = MagicMock(return_value='Wierzba')
        database.get_subscribed_services = MagicMock(return_value=['abba', 'b', 'c'])
        database.get_not_subscribed_services = MagicMock(return_value=[])
        assert text_gen.get_propose_mail_text(1, database) == (''
                                        'Szanowny Panie Wierzba\n'
                                        '\n'
                                        'Ptaki ćwierkają, że jest Pan jednym z naszych najlepszym klientów! Wykupiłeś '
                                        'wszystkie nasze usługi! Zachęcamy do oczekiwania na nowe przyszłe usługi, '
                                        'które się pojawią niedługo!\n'
                                        '\n'
                                        'Uwaga! Subskrypcja na abba wkrótce wygaśnie! Szybko! Odnów subskrypcję!\n'
                                        '\n'
                                        'Cieszymy się, że interesuje się Pan naszymi usługami. W celu uzyskania '
                                        'więcej informacji, zalecamy odwiedzenie naszej strony,by sprawdzić nowe '
                                        'produkty, które oferujemy!\n'
                                        '\n'
                                        'Ciesz się naszymi usługami! \n'
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
                ('Szanowny Panie Wierzba\n'
                 '\n'
                 'Dziękujemy za zamówienie poniższych produktów:\n'
                 '- green\n'
                 '\n'
                 'Faktura znajduje się w załącznikach.\n'
                 '\n'
                 'Twoje zamówienie\n'
                 '\n'
                 'Numer zamówienia:\r123553\n'
                 'Metoda płatności:\rVISA/Mastercard - 1234\n'
                 'Data zamówienia:\r2016-08-31\n'
                 'Całkowita kwota:\r1,315.00 USD\n'
                 '\n'
                 'Cieszymy się, że interesuje się Pan naszymi usługami. W celu uzyskania '
                 'więcej informacji, zalecamy odwiedzenie naszej strony,by sprawdzić nowe '
                 'produkty, które oferujemy!\n'
                 '\n'
                 'Ciesz się naszymi usługami! \n'
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
                ('Szanowna Pani Wierzba\n'
                 '\n'
                 'Dziękujemy za zamówienie poniższych produktów:\n'
                 '- green\n'
                 '- yellow\n'
                 '- red\n'
                 '\n'
                 'Faktura znajduje się w załącznikach.\n'
                 '\n'
                 'Twoje zamówienie\n'
                 '\n'
                 'Numer zamówienia:\r123553\n'
                 'Metoda płatności:\rVISA/Mastercard - 1234\n'
                 'Data zamówienia:\r2016-08-31\n'
                 'Całkowita kwota:\r1,315.00 USD\n'
                 '\n'
                 'Cieszymy się, że interesuje się Pani naszymi usługami. W celu uzyskania '
                 'więcej informacji, zalecamy odwiedzenie naszej strony,by sprawdzić nowe '
                 'produkty, które oferujemy!\n'
                 '\n'
                 'Ciesz się naszymi usługami! \n'
                 'DC Drying Paint Services'))
