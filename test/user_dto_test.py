from src.user_dto import UserDto


def test_user_creation():
    username = 'username'
    name = 'name'
    surname = 'surname'
    age = 18
    email = 'mail'
    gender = 'male'
    timestamp = '2023-01-01 00:00:00'

    user = UserDto(username=username,
                   name=name,
                   surname=surname,
                   age=age,
                   email=email,
                   gender=gender,
                   timestamp=timestamp)

    assert user.username == username
    assert user.name == name
    assert user.surname == surname
    assert user.email == email
    assert user.gender == gender


def test_json_serialization_deserialization():
    user = UserDto(username='username',
                   name='name',
                   surname='surname',
                   age=18,
                   email='mail@example.com',
                   gender='male',
                   timestamp='2023-01-01 00:00:00')

    json_data = user.to_json()
    user_from_json = UserDto.from_json(json_data)

    assert user == user_from_json


def test_xml_serialization_deserialization():
    user = UserDto(username='username',
                   name='name',
                   surname='surname',
                   age=18,
                   email='mail@example.com',
                   gender='male',
                   timestamp='2023-01-01 00:00:00',
                   packets=['a', 'b'])

    xml_data = user.to_xml()
    user_from_xml = UserDto.from_xml(xml_data)

    assert user == user_from_xml


def test_csv_serialization_deserialization():
    user = UserDto(username='username',
                   name='name',
                   surname='surname',
                   age=18,
                   email='mail@example.com',
                   gender='male',
                   timestamp='2023-01-01 00:00:00',
                   packets=['a', 'b'])

    csv_data = user.to_csv()
    user_from_csv = UserDto.from_csv(csv_data)

    assert user == user_from_csv


def test_xml_serialization_deserialization_empty_packets():
    user = UserDto(username='username',
                   name='name',
                   surname='surname',
                   age=18,
                   email='mail@example.com',
                   gender='male',
                   timestamp='2023-01-01 00:00:00',
                   packets=[])

    xml_data = user.to_xml()
    user_from_xml = UserDto.from_xml(xml_data)

    assert user == user_from_xml


def test_csv_serialization_deserialization_empty_packets():
    user = UserDto(username='username',
                   name='name',
                   surname='surname',
                   age=18,
                   email='mail@example.com',
                   gender='male',
                   timestamp='2023-01-01 00:00:00',
                   packets=[])

    csv_data = user.to_csv()
    user_from_csv = UserDto.from_csv(csv_data)

    assert user == user_from_csv