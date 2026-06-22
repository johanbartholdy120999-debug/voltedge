<<<<<<< HEAD
git add .
git commit -m "Add API tests"
git push
=======
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/")
    assert response.status_code == 200
>>>>>>> 418a559 (Fix API test)
