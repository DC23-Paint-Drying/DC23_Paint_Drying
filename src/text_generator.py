def replace_keywords(text: str, userID: int, database) -> str:
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
    :param userID: id of user, to whom the mail is sent
    :param database: the database object - at the moment mock object
    :return:
    """

    if '{$greeting}' in text:
        if database.get_user_sex(userID) == 'M':
            text = text.replace('{$greeting}',
                                'Dear Mr ' + database.get_user_surname(userID))
        if database.get_user_sex(userID) == 'F':
            text = text.replace('{$greeting}',
                                'Dear Mrs ' + database.get_user_surname(userID))

    if '{$proposeNewService}' in text:
        subscribed_services = database.get_subscribed_services()
        not_subscribed_services = database.get_not_subscribed_services()

        if len(not_subscribed_services) > 0:
            if len(subscribed_services) > 0:
                if len(not_subscribed_services) > 3:
                    services = ", ".join(not_subscribed_services[0:3])
                else:
                    services = ", ".join(not_subscribed_services)
                text = text.replace('{$proposeNewService}',
                                    'It seems, you are very interested in service ' + subscribed_services
                                    [0] + '. You should also check these services: ' + services + '!')
            else:
                if len(not_subscribed_services) >= 3:
                    text = text.replace('{$proposeNewService}',
                                        'Looking for new action? Check our best services: ' + ', '.join(
                                            not_subscribed_services[0:3]) + '!')
                else:
                    text = text.replace('{$proposeNewService}',
                                        'Looking for new action? Check our best services: ' +
                                        ', '.join(not_subscribed_services) + '!')
        else:
            text = text.replace('{$proposeNewService}',
                                'It seems, you are one of our best customers! You\'ve bought all of our services! '
                                'Stay tuned for more!')

    if '{$proposeLengtheningSubscription}' in text:
        subscribed_services = database.get_subscribed_services()
        if len(subscribed_services) > 0:
            text = text.replace('{$proposeLengtheningSubscription}',
                                'The subscription for ' + subscribed_services[0] + 'will soon expire! Quick! Renew the '
                                                                                   'subscription!')
        else:
            # delete mark, because there is nothing to propose
            text = text.replace('{$proposeLengtheningSubscription}',
                                '')

    if '{$suggestContact}' in text:
        text = text.replace('{$suggestContact}',
                            'We are glad, you are interested in our services. For more information, we suggest '
                            'visiting our website to check new products we offer!')

    if '{$goodbye}' in text:
        text = text.replace('{$goodbye}',
                            'Enjoy our services \nDC Drying Paint Services')

    if '{$subscribedServices}' in text:
        text = text.replace('{$subscribedServices}',
                            ', '.join(database.get_subscribed_services()))

    if '{$notSubscribedServices}' in text:
        text = text.replace('{$notSubscribedServices}', ', '.join(database.get_not_subscribed_services()))

    return text


def get_propose_mail_text(userID: int, database) -> str:
    """
    function for creating mail text procedurally
    :param userID:
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
    return replace_keywords(mail_text, userID, database)


def get_invoice_mail_text(userID: int, invoice, database) -> str:
    """
    function for creating mail text (for sending invoices) procedurally
    :param userID:
    :param invoice: the invoice object - at the moment mock object
    :param database: the database object - at the moment mock object
    :return:
    """
    products = ''
    for product in invoice.products:
        products += "-" + product + "\n"

    mail_text = ('{$greeting}\n'
                 '\n'
                 'Thank you for your order for the following products:\n'
                 + products +
                 '\n'
                 'Please find your invoice attached to this email.'
                 '\n'
                 '\n'
                 'Your order\n'
                 '\n'
                 'Reference no.:\r' + str(invoice.number) + '\n'  # 12345566
                 'Payment method:\r' + invoice.payment + '\n'  # VISA/Mastercard - 1234
                 'Order date:\r' + invoice.date + '\n'  # 2016-08-31
                 'Grand total:\r' + f'{invoice.price:,.2f} USD\n'  # 1,315.00 USD
                 '\n'
                 '{$suggestContact}\n'
                 '\n'
                 '{$goodbye}')
    return replace_keywords(mail_text, userID, database)
