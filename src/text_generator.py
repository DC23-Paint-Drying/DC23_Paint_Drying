from src.database import Database
from src.invoice_generator import Invoice


def replace_keywords(text: str, user_id: str, database: Database) -> str:
    """
    Modifies text containing keywords in format {$word}
    List of all keywords: \n
    -{$greeting}
    -{$proposeNewService}
    -{$proposeLengtheningSubscription}
    -{$suggestContact}
    -{$goodbye}
    -{$subscribedServices}
    -{$notSubscribedServices}
    :param text: text to be modified
    :param user_id: id of user, to whom the mail is sent
    :param database: the database object - at the moment mock object
    :return:
    """

    user_is_male = database.get_user_sex(user_id) == 'M'

    if '{$greeting}' in text:
        if user_is_male:
            text = text.replace('{$greeting}',
                                'Szanowny Panie ' + database.get_user_surname(user_id))
        if not user_is_male:
            text = text.replace('{$greeting}',
                                'Szanowna Pani ' + database.get_user_surname(user_id))

    if '{$proposeNewService}' in text:
        subscribed_packets = database.get_subscribed_packets(user_id)
        not_subscribed_packets = database.get_not_subscribed_packets(user_id)

        if len(not_subscribed_packets) > 0:
            if len(subscribed_packets) > 0:
                if len(not_subscribed_packets) > 3:
                    services = ", ".join(not_subscribed_packets[0:3])
                else:
                    services = ", ".join(not_subscribed_packets)
                text = text.replace('{$proposeNewService}',
                                    'Zauważyliśmi, że jest '+('Pan zainteresowany ' if user_is_male else 'Pani zainteresowana ') +
                                                                                                   'usługą ' +
                                    subscribed_packets[0] + '. '+('Powinienien Pan' if user_is_male else 'Powinna Pani')+' '
                                    'sprawdzić także te usługi: ' + services + '!')
            else:
                if len(not_subscribed_packets) >= 3:
                    text = text.replace('{$proposeNewService}',
                                        'Szukasz nowych wrażeń? Sprawdź nasze najlepsze usługi: ' + ', '.join(
                                            not_subscribed_packets[0:3]) + '!')
                else:
                    text = text.replace('{$proposeNewService}',
                                        'Szukasz nowych wrażeń? Sprawdź nasze najlepsze usługi: ' +
                                        ', '.join(not_subscribed_packets) + '!')
        else:
            text = text.replace('{$proposeNewService}',
                                'Ptaki ćwierkają, że jest '+('Pan jednym z naszych najlepszym klientów! Wykupił Pan' if user_is_male else
                                'Pani jedną z naszych najlepszych klientek! Wykupiła Pani')+' wszystkie nasze usługi! '
                                'Zachęcamy do oczekiwania na nowe usługi, które pojawią się niedługo!')

    if '{$proposeLengtheningSubscription}' in text:
        subscription = database.get_subscription(user_id)
        if subscription != '':
            text = text.replace('{$proposeLengtheningSubscription}',
                                'Uwaga! Subskrypcja ' + subscription +
                                ' wkrótce wygaśnie! Szybko! Odnów subskrypcję!')
        else:
            # delete mark, because there is nothing to propose
            text = text.replace('{$proposeLengtheningSubscription}',
                                '')

    if '{$suggestContact}' in text:
        text = text.replace('{$suggestContact}',
                            'Cieszymy się, że interesuje się '+('Pan' if user_is_male else 'Pani')+' naszymi usługami. W celu uzyskania dodatkowych informacji, zalecamy '
                            'odwiedzenie naszej strony, by sprawdzić nowe produkty, które oferujemy!')

    if '{$goodbye}' in text:
        text = text.replace('{$goodbye}',
                            'Ciesz się naszymi usługami! \nDC Drying Paint Services')

    if '{$subscribedServices}' in text:
        text = text.replace('{$subscribedServices}',
                            ', '.join(database.get_subscribed_packets(user_id)))

    if '{$notSubscribedServices}' in text:
        text = text.replace('{$notSubscribedServices}', ', '.join(database.get_not_subscribed_packets(user_id)))

    return text


def get_propose_mail_text(user_id: str, database: Database) -> str:
    """
    function for creating mail text procedurally
    :param user_id:
    :param database: the database object - at the moment mock object
    :return: mail text
    """
    mail_text = ('{$greeting}\n'
                 '\n'
                 '{$proposeNewService}\n'
                 '\n'
                 '{$proposeLengtheningSubscription}\n'
                 '\n'
                 '{$suggestContact}\n'
                 '\n'
                 '{$goodbye}')
    return replace_keywords(mail_text, user_id, database)


def get_invoice_mail_text(user_id: str, invoice: Invoice, database: Database) -> str:
    """
    function for creating mail text (for sending invoices) procedurally
    :param user_id:
    :param invoice: the invoice object - at the moment mock object
    :param database: the database object - at the moment mock object
    :return:
    """
    products = ''
    if len(invoice.client_packets) > 0:
        for packet in invoice.client_packets:
            products += "- " + packet[0] + "\n"

    mail_text = ('{$greeting}\n'
                 '\n'
                 'Aktualna subskrypcja: ' + invoice.client_subscription + '\n'
                 'Kwota: ' + f'{invoice.client_subscription_cost} PLN' + '\n'
                 +
                 (
                     ('\nDziękujemy za zamówienie poniższych pakietów:\n'
                     + products) if len(invoice.client_packets) > 0
                     else ''
                 )+
                 '\n'
                 'Faktura znajduje się w załącznikach.'
                 '\n'
                 '\n'
                 'Twoje zamówienie\n'
                 '\n'
                 'Numer zamówienia:\r' + str(invoice.invoice_number) + '\n'  # 12345566                 
                 'Data zamówienia:\r' + str(invoice.invoice_date) + '\n'  # 2016-08-31
                 'Całkowita kwota:\r' + f'{invoice.total_cost:,.2f} PLN\n'  
                 '\n'
                 '{$suggestContact}\n'
                 '\n'
                 '{$goodbye}')
    return replace_keywords(mail_text, user_id, database)
