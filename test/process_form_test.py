import sys
sys.path.append('src')
from process_form import process_form


def test_process_register_form():
    username = 'user123'
    name = 'User'
    surname = '123'
    email = 'user123@example.com'
    gender = 'male'

    register_data = process_form(username=username,
                                 name=name,
                                 surname=surname,
                                 email=email,
                                 gender=gender)

    assert register_data['username'] == username
    assert register_data['name'] == name
    assert register_data['surname'] == surname
    assert register_data['email'] == email
    assert register_data['gender'] == gender


def test_process_subscription_form():
    email = 'user123@example.com'
    subscription_level = 'bronze'

    subscription_data = process_form(email=email,
                                     subscription_level=subscription_level)

    assert subscription_data['email'] == email
    assert subscription_data['subscription_level'] == subscription_level
