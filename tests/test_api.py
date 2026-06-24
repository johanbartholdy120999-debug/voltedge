from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

<<<<<<< HEAD
def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"
    
=======
def test_root():
    response = client.get("/")
    assert response.status_code == 200
>>>>>>> 31fc2640b81234a7acd0e181677c44420260ea4a
