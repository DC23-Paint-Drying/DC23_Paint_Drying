import uuid
from datetime import datetime

import pytest

import src.report.report_data as report_data
import src.manifest as company
from src.database_context import DatabaseContext
from src.bundle_info import BundleInfo
from src.client_info import ClientInfo
from src.user_dto import UserDto
from src.subscription_info import SubscriptionInfo


@pytest.fixture(autouse=True)
def database_context_handling():
    db = DatabaseContext('db')
    now = datetime(2023, 11, 11, 0, 0, 0)
    later = datetime(2023, 12, 11, 0, 0, 0)
    db.serialize(ClientInfo(
        UserDto('test1', 'test1', 'test1', 17, 'test1@test.com', 'male', now.strftime('%Y-%m-%d %H:%M:%S')),
        SubscriptionInfo(list(company.SUBSCRIPTIONS.keys())[0], now.strftime('%Y-%m-%d %H:%M:%S')),
        [BundleInfo('test1@test.com', list(company.PACKETS.keys())[0],
                    now.strftime('%Y-%m-%d'), later.strftime('%Y-%m-%d'), str(uuid.uuid4()))]
    ))
    db.serialize(ClientInfo(
        UserDto('test2', 'test2', 'test2', 22, 'test2@test.com', 'female', now.strftime('%Y-%m-%d %H:%M:%S')),
        SubscriptionInfo(list(company.SUBSCRIPTIONS.keys())[1], now.strftime('%Y-%m-%d %H:%M:%S')),
        [BundleInfo('test2@test.com', list(company.PACKETS.keys())[1],
                    now.strftime('%Y-%m-%d'), later.strftime('%Y-%m-%d'), str(uuid.uuid4()))]
    ))
    yield
    db.destroy()


def test_get_report_data():
    data = report_data.get_report_data()

    assert data['users']['subscriptions'][list(company.SUBSCRIPTIONS.values())[0]['name']] == 1
    assert data['users']['subscriptions'][list(company.SUBSCRIPTIONS.values())[1]['name']] == 1
    assert data['users']['subscriptions'][list(company.SUBSCRIPTIONS.values())[2]['name']] == 0

    assert data['users']['gender']['Mężczyźni'] == 1
    assert data['users']['gender']['Kobiety'] == 1
    assert data['users']['gender']['Inne'] == 0

    assert data['users']['age']['<18'] == 1
    assert data['users']['age']['18-25'] == 1
    assert data['users']['age']['26-35'] == 0
    assert data['users']['age']['36-50'] == 0
    assert data['users']['age']['>50'] == 0

    assert data['sales'][list(company.SUBSCRIPTIONS.values())[0]['name']]['users'] == 1
    assert data['sales'][list(company.SUBSCRIPTIONS.values())[0]['name']]['profit'] == \
           1 * list(company.SUBSCRIPTIONS.values())[0]['price']
    assert data['sales'][list(company.SUBSCRIPTIONS.values())[1]['name']]['users'] == 1
    assert data['sales'][list(company.SUBSCRIPTIONS.values())[1]['name']]['profit'] == \
           1 * list(company.SUBSCRIPTIONS.values())[1]['price']
    assert data['sales'][list(company.SUBSCRIPTIONS.values())[2]['name']]['users'] == 0
    assert data['sales'][list(company.SUBSCRIPTIONS.values())[2]['name']]['profit'] == \
           0 * list(company.SUBSCRIPTIONS.values())[2]['price']
