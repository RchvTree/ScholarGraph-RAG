# check_models
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("--- Available Models List ---")
# List all models available to your API key
for model in client.models.list():
    print(f"Model Name: {model.name}")