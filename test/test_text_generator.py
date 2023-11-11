import inspect
import unittest
from unittest.mock import MagicMock

import src.text_generator as text_gen
from src.csvDatabase import CSVDatabase
from src.database_context import DatabaseContext
from src.invoice_generator import Invoice
from src.text_generator import Database
from src.user_dto import UserDto

import utils.data_set as data_set


class TestReplaceKeywords(unittest.TestCase):
    def setUp(self) -> None:
        self.context = DatabaseContext("db")
        self.db = Database(self.context)

    def tearDown(self) -> None:
        self.context.destroy()
    def test_greeting(self):
        self.db.get_user_sex = MagicMock(return_value='M')
        self.db.get_user_surname = MagicMock(return_value='Wierzba')

        assert text_gen.replace_keywords('{$greeting}', '1', self.db) == 'Szanowny Panie Wierzba'

    def test_propose_new_service(self):
        self.db.get_user_sex = MagicMock(return_value='F')

        # test when all is bought
        self.db.get_subscribed_packets = MagicMock(return_value=['a', 'b', 'c'])
        self.db.get_not_subscribed_packets = MagicMock(return_value=[])
        assert text_gen.replace_keywords('{$proposeNewService}', '1',
                                         self.db) == ('Ptaki ćwierkają, że jest Pani jedną z naszych najlepszych klientek! '
                                                       'Wykupiłaś wszystkie nasze usługi! Zachęcamy do oczekiwania na '
                                                       'nowe przyszłe usługi, które się pojawią niedługo!')

        # test when there is anything to suggest, but something is bought
        self.db.get_subscribed_packets = MagicMock(return_value=['a', 'b', 'c'])
        self.db.get_not_subscribed_packets = MagicMock(return_value=['d', 'e'])
        assert text_gen.replace_keywords('{$proposeNewService}', '1',
                                         self.db) == ('Zauważyliśmi, że jest Pani zainteresowana usługą a. Powinna Pani '
                                                       'sprawdzić także te usługi: d, e!')

        # test when nothing is bought, but there are more than 2 services in total
        self.db.get_subscribed_packets = MagicMock(return_value=[])
        self.db.get_not_subscribed_packets = MagicMock(return_value=['a', 'b', 'c'])
        assert text_gen.replace_keywords('{$proposeNewService}', '1',
                                         self.db) == 'Szukasz nowych wrażeń? Sprawdź nasze najlepsze usługi: a, b, c!'

        # test when nothing is bought, but there are less than 3 services in total
        self.db.get_subscribed_packets = MagicMock(return_value=[])
        self.db.get_not_subscribed_packets = MagicMock(return_value=['a', 'b'])
        assert text_gen.replace_keywords('{$proposeNewService}', '1',
                                         self.db) == 'Szukasz nowych wrażeń? Sprawdź nasze najlepsze usługi: a, b!'

        # test when something is bought, but there are more than 3 services in total
        self.db.get_subscribed_packets = MagicMock(return_value=['d'])
        self.db.get_not_subscribed_packets = MagicMock(return_value=['a', 'b', 'c','e'])
        assert text_gen.replace_keywords('{$proposeNewService}', '1',
                                         self.db) == 'Zauważyliśmi, że jest Pani zainteresowana usługą d. Powinna Pani sprawdzić także te usługi: a, b, c!'

    def test_proposeLengtheningSubscription(self):
        self.db.get_user_sex = MagicMock(return_value='M')
        self.db.get_subscription = MagicMock(return_value='abb')

        assert text_gen.replace_keywords('{$proposeLengtheningSubscription}', '1',
                                         self.db) == ('Uwaga! Subskrypcja na abb wkrótce wygaśnie! Szybko! Odnów '
                                                       'subskrypcję!')

    def test_suggestContact(self):
        self.db.get_user_sex = MagicMock(return_value='F')

        assert text_gen.replace_keywords('{$suggestContact}', '1',
                                         self.db) == ('Cieszymy się, że interesuje się Pani naszymi usługami. W celu '
                                                       'uzyskania więcej informacji, zalecamy odwiedzenie naszej '
                                                       'strony,by sprawdzić nowe produkty, które oferujemy!')

    def test_goodbye(self):
        self.db.get_user_sex = MagicMock(return_value='M')

        assert text_gen.replace_keywords('{$goodbye}', '1',
                                         self.db) == 'Ciesz się naszymi usługami! \nDC Drying Paint Services'

    def test_subscribedServices(self):
        self.db.get_user_sex = MagicMock(return_value='M')
        self.db.get_subscribed_packets = MagicMock(return_value=['a', 'b', 'c', 'd', 'e'])

        assert text_gen.replace_keywords('{$subscribedServices}', '1', self.db) == 'a, b, c, d, e'

    def test_not_subscribedServices(self):
        self.db.get_user_sex = MagicMock(return_value='M')
        self.db.get_not_subscribed_packets = MagicMock(return_value=['a', 'b', 'c', 'd', 'e'])

        assert text_gen.replace_keywords('{$notSubscribedServices}', '1', self.db) == 'a, b, c, d, e'


class TestProposeMailText(unittest.TestCase):
    def setUp(self) -> None:
        self.context = DatabaseContext("db")
        self.db = Database(self.context)

    def tearDown(self) -> None:
        self.context.destroy()
    def test_simple_mail(self):
        self.db.get_user_sex = MagicMock(return_value='M')
        self.db.get_user_surname = MagicMock(return_value='Wierzba')
        self.db.get_subscription = MagicMock(return_value='abba')
        self.db.get_subscribed_packets = MagicMock(return_value=['aaaa', 'b', 'c'])
        self.db.get_not_subscribed_packets = MagicMock(return_value=['d', 'e'])
        assert text_gen.get_propose_mail_text('1', self.db) == (''
                                        'Szanowny Panie Wierzba\n'
                                        '\n'
                                        'Zauważyliśmi, że jest Pan zainteresowany usługą aaaa. Powinienien Pan sprawdzić '
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
        self.db.get_user_sex = MagicMock(return_value='F')
        self.db.get_user_surname = MagicMock(return_value='Kowalska')
        self.db.get_subscription = MagicMock(return_value='')
        self.db.get_subscribed_packets = MagicMock(return_value=[])
        self.db.get_not_subscribed_packets = MagicMock(return_value=['debohra', 'esda'])
        assert text_gen.get_propose_mail_text('1', self.db) == (''
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
        self.db.get_user_sex = MagicMock(return_value='M')
        self.db.get_user_surname = MagicMock(return_value='Wierzba')
        self.db.get_subscription = MagicMock(return_value='abba')
        self.db.get_subscribed_packets = MagicMock(return_value=['abba', 'b', 'c'])
        self.db.get_not_subscribed_packets = MagicMock(return_value=[])
        assert text_gen.get_propose_mail_text('1', self.db) == (''
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
    def setUp(self) -> None:
        self.context = DatabaseContext("db")
        self.db = Database(self.context)

    def tearDown(self) -> None:
        self.context.destroy()
    def test_one_product(self):
        self.db.get_user_sex = MagicMock(return_value='M')
        self.db.get_user_surname = MagicMock(return_value='Wierzba')

        male_client = data_set.generate_male_client_info()

        invoice = Invoice(male_client)
        invoice.invoice_number = 123553
        invoice.invoice_date = '2016-08-31'

        assert (text_gen.get_invoice_mail_text(male_client.basic.id, invoice, self.db) ==
                ('Szanowny Panie Wierzba\n'
                 '\n'
                 'Aktualna subskrypcja: Podstawowy\n'
                 'Kwota: 12.99 PLN\n'                 
                 '\n'
                 'Dziękujemy za zamówienie poniższych pakietów:\n'
                  '- Miesięczny\n'
                  '- Rodzinny\n'
                  '\n'
                 'Faktura znajduje się w załącznikach.\n'
                 '\n'
                 'Twoje zamówienie\n'
                 '\n'
                 'Numer zamówienia:\r123553\n'                 
                 'Data zamówienia:\r2016-08-31\n'
                 'Całkowita kwota:\r35.97 PLN\n'
                 '\n'
                 'Cieszymy się, że interesuje się Pan naszymi usługami. W celu uzyskania '
                 'więcej informacji, zalecamy odwiedzenie naszej strony,by sprawdzić nowe '
                 'produkty, które oferujemy!\n'
                 '\n'
                 'Ciesz się naszymi usługami! \n'
                 'DC Drying Paint Services'))

    def test_multiple_product(self):
        self.db = Database(DatabaseContext("db"))
        self.db.get_user_sex = MagicMock(return_value='F')
        self.db.get_user_surname = MagicMock(return_value='Wierzba')

        male_client = data_set.generate_male_client_info()

        invoice = Invoice(male_client)
        invoice.invoice_number = 123553
        invoice.invoice_date = '2016-08-31'

        assert (text_gen.get_invoice_mail_text(male_client.basic.id, invoice, self.db) ==
                ('Szanowna Pani Wierzba\n'
                 '\n'
                 'Aktualna subskrypcja: Podstawowy\n'
                 'Kwota: 12.99 PLN\n'
                 '\n'
                 'Dziękujemy za zamówienie poniższych pakietów:\n'
                 '- Miesięczny\n'
                 '- Rodzinny\n'
                 '\n'
                 'Faktura znajduje się w załącznikach.\n'
                 '\n'
                 'Twoje zamówienie\n'
                 '\n'
                 'Numer zamówienia:\r123553\n'
                 'Data zamówienia:\r2016-08-31\n'
                 'Całkowita kwota:\r35.97 PLN\n'
                 '\n'
                 'Cieszymy się, że interesuje się Pani naszymi usługami. W celu uzyskania '
                 'więcej informacji, zalecamy odwiedzenie naszej strony,by sprawdzić nowe '
                 'produkty, które oferujemy!\n'
                 '\n'
                 'Ciesz się naszymi usługami! \n'
                 'DC Drying Paint Services'))
