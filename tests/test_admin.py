import pytest

from jimmy import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    r = client.get('/admin/')
    assert r.status_code == 200
