from fastapi.testclient import TestClient
from web.tag import app

client = TestClient(app)

def test_create_tag():
    response = client.post("/", json={"tag": "mytesttag"})
    assert response.status_code == 200
    assert response.json() == {"tag": "mytesttag"}

def test_get_tag():
    # First, create a tag to ensure it exists for retrieval
    client.post("/", json={"tag": "another_tag"})

    response = client.get("/another_tag")
    assert response.status_code == 200

    assert response.json()['tag'] == "another_tag"
    assert 'created' in response.json()

    # datetime object are serialised to strings in JSON
    assert isinstance(response.json()["created"], str)

def test_get_tag_not_found():
    response = client.get("/notexist")
    assert response.status_code == 404
