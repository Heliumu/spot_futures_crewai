from dotenv import load_dotenv
import os

load_dotenv()

def test_environment_variable():
    api_key = os.getenv("ZHIPU_API_KEY")
    print(f"ZHIPU_API_KEY: {api_key}")

if __name__ == "__main__":
    test_environment_variable()