import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key not found. Check your .env file.")

else:
    try:
        client = genai.Client(api_key=api_key)

        response = client.interactions.create(
            model="gemini-3.8-flash",
            input="Reply exactly: Gemini connection successful!"
        )

        print("Gemini API Connection Successful!")
        print("Gemini Response:", response.output_text)

    except Exception as e:
        print("Gemini connection failed.")
        print("Error:", e)
        
        
# python src/test_gemini.py