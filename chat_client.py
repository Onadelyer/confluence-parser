import requests
import sys
import time

BASE_URL = "http://localhost:8000"

def chat_loop():
    print("\n" + "="*50)
    print("🤖 Confluence RAG Chat CLI")
    print("Type 'exit', 'quit', or 'q' to stop.")
    print("="*50 + "\n")

    # Check if server is running
    try:
        requests.get(f"{BASE_URL}/health")
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: Could not connect to server at {BASE_URL}")
        print("Please make sure the API server is running (uvicorn main:app ...)")
        return

    while True:
        try:
            question = input("\nYou: ").strip()
            if not question:
                continue
            
            if question.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye! 👋")
                break

            print("Thinking...", end="", flush=True)
            
            start_time = time.time()
            try:
                response = requests.post(f"{BASE_URL}/query", json={"question": question})
                response.raise_for_status()
                data = response.json()
                
                # Clear "Thinking..." line
                print("\r" + " "*20 + "\r", end="", flush=True)
                
                answer = data.get("answer", "No answer provided.")
                sources = data.get("sources", [])
                
                print(f"AI: {answer}")
                
                if sources:
                    print(f"\n📚 Sources: {', '.join(sources)}")
                    
            except requests.exceptions.RequestException as e:
                print(f"\n❌ API Error: {e}")
                
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break

if __name__ == "__main__":
    chat_loop()
