from src.csvDatabase import CSVDatabase
from src.database import Database


def test_get_user_sex():
    columns = ["id", "gender"]
    client1 = {"id": '1', "gender": "male"}
    client2 = {"id": '2', "gender": "female"}
    csvdb = CSVDatabase("dbtest.csv", columns)

    csvdb.add_client(client1)
    csvdb.add_client(client2)

    db = Database(csvdb)
    assert db.get_user_sex('1') == 'M'
    assert db.get_user_sex('2') == 'F'

    csvdb.drop_database()

def test_get_subscribed_packets():
    packets = ['monthly','family']
    columns = ["id", "packets"]
    client1 = {"id": '1', "packets": packets}
    csvdb = CSVDatabase("dbtest.csv", columns)

    csvdb.add_client(client1)

    db = Database(csvdb)
    assert db.get_subscribed_packets('1') == ['Miesięczny','Rodzinny']

    csvdb.drop_database()
def test_get_not_subscribed_packets():
    columns = ["id", "packets"]
    client1 = {"id": '1', "packets": ['monthly']}
    csvdb = CSVDatabase("dbtest.csv", columns)

    csvdb.add_client(client1)

    db = Database(csvdb)
    assert db.get_not_subscribed_packets('1') == ['Rodzinny']

    csvdb.drop_database()
def test_get_subscription():
    columns = ["id", "subscription"]
    client1 = {"id": '1', "subscription": 'basic'}
    csvdb = CSVDatabase("dbtest.csv", columns)

    csvdb.add_client(client1)

    db = Database(csvdb)
    assert db.get_subscription('1') == 'Podstawowy'

    csvdb.drop_database()
def test_get_user_surname():
    surname = 'Kaczka'
    columns = ["id", "surname"]
    client1 = {"id": '1', "surname": surname}
    csvdb = CSVDatabase("dbtest.csv", columns)

    csvdb.add_client(client1)

    db = Database(csvdb)
    assert db.get_user_surname('1') == surname

    csvdb.drop_database()