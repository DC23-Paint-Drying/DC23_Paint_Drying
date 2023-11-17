"""
Module used to collect data for report.
"""

from datetime import datetime

import pandas as pd

from src.database_context import DatabaseContext
import src.manifest as manifest


def get_report_data(db: DatabaseContext) -> dict:
    """
    Collects all required data for report and transforms it to dictionary.

    Args:
        db: Database to get data from.

    Returns:
        Dictionary containing data for report.
    """

    users_df = pd.read_csv(db.basic_db._filename)
    users_df['timestamp'] = pd.to_datetime(users_df['timestamp'])
    users_df['subscription_timestamp'] = pd.to_datetime(users_df['subscription_timestamp'])

    packets_df = pd.read_csv(db.bundle_db._filename)
    packets_df['date_from'] = pd.to_datetime(packets_df['date_from'])
    packets_df['date_to'] = pd.to_datetime(packets_df['date_to'])

    date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d'),
        'date': date.strftime('%Y-%m'),
        'users': {
            'subscriptions': {},
            'gender': {
                'Mężczyźni': len(users_df[users_df['gender'] == 'male']),
                'Kobiety': len(users_df[users_df['gender'] == 'female']),
                'Inne': len(users_df[users_df['gender'] == 'other']),
            },
            'age': {
                '<18': len(users_df[users_df['age'] < 18]),
                '18-25': len(users_df[(users_df['age'] >= 18) & (users_df['age'] <= 25)]),
                '26-35': len(users_df[(users_df['age'] > 25) & (users_df['age'] <= 35)]),
                '36-50': len(users_df[(users_df['age'] > 35) & (users_df['age'] <= 50)]),
                '>50': len(users_df[users_df['age'] > 50]),
            },
        },
        'sales': {},
        'recent': {
            'users': len(users_df[users_df['timestamp'] > date]),
            'subscribed': {},
            'packets': {}
        }
    }

    for subscription in manifest.SUBSCRIPTIONS:
        name = manifest.SUBSCRIPTIONS[subscription]['name']
        price = manifest.SUBSCRIPTIONS[subscription]['price']
        data['users']['subscriptions'][name] = len(users_df[users_df['subscription_level'] == subscription])
        data['sales'][name] = {}
        data['sales'][name]['users'] = data['users']['subscriptions'][name]
        data['sales'][name]['profit'] = data['users']['subscriptions'][name] * price
        data['recent']['subscribed'][name] = len(users_df[(users_df['subscription_level'] == subscription) &
                                                          (users_df['subscription_timestamp'] > date)])

    for packet in manifest.PACKETS:
        name = manifest.PACKETS[packet]['name']
        data['recent']['packets'][name] = len(packets_df[(packets_df['name'] == packet) &
                                                         (packets_df['date_from'] > date)])

    return data
