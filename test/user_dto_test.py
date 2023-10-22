from src.user_dto import UserDto, Gender


def test_user_creation():
    username = 'username'
    name = 'name'
    surname = 'surname'
    email = 'mail'
    gender = 'male'

    user = UserDto(username=username,
                   name=name,
                   surname=surname,
                   email=email,
                   gender=Gender(gender))

    assert user.username == username
    assert user.name == name
    assert user.surname == surname
    assert user.email == email
    assert user.gender == gender


def test_json_serialization_deserialization():
    user = UserDto(username='username',
                   name='name',
                   surname='surname',
                   email='mail@example.com',
                   gender=Gender.MALE)

    json_data = user.to_json()
    user_from_json = UserDto.from_json(json_data)

    assert user == user_from_json


def test_xml_serialization_deserialization():
    user = UserDto(username='username',
                   name='name',
                   surname='surname',
                   email='mail@example.com',
                   gender=Gender.MALE)

    xml_data = user.to_xml()
    user_from_xml = UserDto.from_xml(xml_data)

    assert user == user_from_xml


def test_csv_serialization_deserialization():
    user = UserDto(username='username',
                   name='name',
                   surname='surname',
                   email='mail@example.com',
                   gender=Gender.MALE)

    csv_data = user.to_csv()
    user_from_csv = UserDto.from_csv(csv_data)

    assert user == user_from_csv