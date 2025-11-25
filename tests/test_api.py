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

def test_generate():
    print("Testing /generate...")
    payload = {"message": "Hello from test"}
    try:
        response = requests.post(f"{BASE_URL}/generate", json=payload)
        print(f"Generate status: {response.status_code}")
        print(f"Generate response: {response.json()}")
    except Exception as e:
        print(f"Generate test failed: {e}")

def test_query():
    print("Testing /query...")
    payload = {"question": "Give me the recepie of the pie"}
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
    test_generate()
    test_query()
