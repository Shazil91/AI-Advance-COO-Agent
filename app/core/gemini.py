from google import genai
from app.core.config import GEMINI_API_KEY

client=genai.Client(api_key=GEMINI_API_KEY)


def ask_gemini(prompt:str)->str:
    if not prompt or prompt.strip() == "" :
        return "Empty response return to gemini"
    
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt]
    )
    return response.text