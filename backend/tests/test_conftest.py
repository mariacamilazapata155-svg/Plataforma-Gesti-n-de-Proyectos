def test_database_connection(db_session):
    assert db_session is not None


def test_client_creation(client):
    assert client is not None


def test_users_fixture(users):
    assert users["owner"].username == "owner"
    assert users["member"].username == "member"


def test_authorization_data(authorization_data):
    assert authorization_data["project"].title == "Proyecto compartido"
    assert authorization_data["board"].title == "Tablero compartido"
    assert authorization_data["task"].title == "Tarea compartida"


def test_owner_headers(owner_headers):
    assert "Authorization" in owner_headers