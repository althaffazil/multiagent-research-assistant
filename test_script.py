import os
from dotenv import load_dotenv

load_dotenv()
print(f"Key found: {os.getenv('GOOGLE_API_KEY')[:10]}...") # Prints first 10 chars