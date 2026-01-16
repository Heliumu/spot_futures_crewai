import os
from .aitrados_data import AitradosDataProvider
from .mock_data import MockDataProvider
from dotenv import load_dotenv

load_dotenv()

def get_data_provider():
    use_real = os.getenv("USE_REAL_DATA", "false").lower() == "true"
    if use_real:
        secret_key = os.getenv("AITRADOS_SECRET_KEY")
        if not secret_key:
            raise EnvironmentError("USE_REAL_DATA=true but AITRADOS_SECRET_KEY not set in .env")
        return AitradosDataProvider(secret_key)
    else:
        return MockDataProvider()
