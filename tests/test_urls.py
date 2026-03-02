from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_short_url():
    response = client.post("/shorten", json={
        "original_url": "https://google.com",
    
        "short_code": "test999"
    })
    assert response.status_code == 400 #duplicate short code

def test_create_short_url1():
    response = client.post("/shorten", json={
        "original_url": "https://youtube.com",
        "expiry_date": "2024-01-01T00:00:00",
        
    })
    assert response.status_code == 201

def test_create_short_url_2():
    response = client.post(
        "/shorten", json = {
            "original_url" : "https://github.com",
            "expiry_date": "2024-03-01T08:15:00",
            "short_code" : "gits"
        }
    )

def test_expired_redirect():
    # 1. Create the short URL
    response = client.post("/shorten", json={
        "original_url": "https://youtube.com",
        "expiry_date": "2020-01-01T00:00:00",  # past date to simulate expired link
    })
    assert response.status_code == 201

    short_code = response.json()["short_code"]

    # 2. Try to access the short URL
    redirect_response = client.get(f"/{short_code}")
    assert redirect_response.status_code == 410  
