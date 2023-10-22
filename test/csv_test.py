import pytest
from src.csvDatabase import CSVDatabase


def test_create_db_with_wrong_columns():
    columns_without_id = ["name", "surname", "subscription"]

    with pytest.raises(KeyError):
        CSVDatabase("dbtest.csv", columns_without_id)


def test_add_client_with_wrong_columns():
    columns = ["id", "subscription"]
    client = {"id": "01", "name": "John", "subscription": "gold"}

    db = CSVDatabase("dbtest.csv", columns)

    with pytest.raises(ValueError):
        db.add_client(client)

    db.drop_database()


def test_get_nonexistent_client():
    columns = ["id", "subscription"]
    db = CSVDatabase("dbtest.csv", columns)

    assert db.get_client("01") is None

    db.drop_database()


def test_add_and_get_client():
    columns = ["id", "subscription"]
    client1 = {"id": "01", "subscription": "bronze"}
    client2 = {"id": "02", "subscription": "gold"}
    db = CSVDatabase("dbtest.csv", columns)

    db.add_client(client1)
    db.add_client(client2)

    assert db.get_client("01") == client1
    assert db.get_client("02") == client2

    db.drop_database()


def test_add_duplicated_client():
    columns = ["id", "subscription"]
    client = {"id": "01", "subscription": "bronze"}
    db = CSVDatabase("dbtest.csv", columns)

    db.add_client(client)

    with pytest.raises(KeyError):
        db.add_client(client)

    db.drop_database()


def test_update_nonexistent_client():
    columns = ["id", "subscription"]
    client = {"id": "01", "subscription": "bronze"}
    db = CSVDatabase("dbtest.csv", columns)

    with pytest.raises(KeyError):
        db.update_client(client)

    db.drop_database()


def test_update_client():
    columns = ["id", "subscription"]
    client = {"id": "01", "subscription": "bronze"}
    db = CSVDatabase("dbtest.csv", columns)

    db.add_client(client)

    updated_client = db.get_client("01")
    updated_client["subscription"] = "gold"
    db.update_client(updated_client)

    assert db.get_client("01") == updated_client

    db.drop_database()


def test_remove_nonexistent_client():
    columns = ["id", "subscription"]
    db = CSVDatabase("dbtest.csv", columns)

    with pytest.raises(KeyError):
        db.remove_client("01")

    db.drop_database()


def test_remove_client():
    columns = ["id", "subscription"]
    client1 = {"id": "01", "subscription": "bronze"}
    client2 = {"id": "02", "subscription": "gold"}
    client3 = {"id": "03", "subscription": "platinum"}
    db = CSVDatabase("dbtest.csv", columns)

    db.add_client(client1)
    db.add_client(client2)
    db.add_client(client3)

    db.remove_client("02")

    assert db.get_client("01") == client1
    assert db.get_client("02") is None
    assert db.get_client("03") == client3

    db.drop_database()


def test_get_all_clients():
    columns = ["id", "subscription"]
    client1 = {"id": "01", "subscription": "bronze"}
    client2 = {"id": "02", "subscription": "gold"}
    client3 = {"id": "03", "subscription": "platinum"}
    db = CSVDatabase("dbtest.csv", columns)

    db.add_client(client1)
    db.add_client(client2)
    db.add_client(client3)

    clients = db.get_clients()

    assert len(clients) == 3
    assert client1 in clients
    assert client2 in clients
    assert client3 in clients

    db.drop_database()


def test_get_clients_with_predicate():
    columns = ["id", "subscription"]
    client1 = {"id": "01", "subscription": "bronze"}
    client2 = {"id": "02", "subscription": "gold"}
    client3 = {"id": "03", "subscription": "platinum"}
    db = CSVDatabase("dbtest.csv", columns)

    db.add_client(client1)
    db.add_client(client2)
    db.add_client(client3)

    clients = db.get_clients(
        lambda client: client["subscription"] in ("bronze", "platinum")
    )

    assert len(clients) == 2
    assert client1 in clients
    assert client3 in clients

    db.drop_database()
