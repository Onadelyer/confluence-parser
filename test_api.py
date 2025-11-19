import requests
import time

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing /health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        print("Health check passed!")
    except Exception as e:
        print(f"Health check failed: {e}")

def test_ingest():
    print("Testing /ingest (Mocked)...")
    # Note: This will fail if credentials are not set in .env
    # We are just checking if the endpoint is reachable and handles auth error or success
    try:
        response = requests.post(f"{BASE_URL}/ingest")
        print(f"Ingest status: {response.status_code}")
        print(f"Ingest response: {response.json()}")
    except Exception as e:
        print(f"Ingest test failed: {e}")

def test_query():
    print("Testing /query...")
    payload = {"question": "What is this documentation about?"}
    try:
        response = requests.post(f"{BASE_URL}/query", json=payload)
        print(f"Query status: {response.status_code}")
        print(f"Query response: {response.json()}")
    except Exception as e:
        print(f"Query test failed: {e}")

if __name__ == "__main__":
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(5)
    test_health()
    test_ingest()
    test_query()
