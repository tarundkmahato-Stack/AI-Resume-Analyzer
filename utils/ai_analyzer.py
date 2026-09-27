import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def generate_ai_analysis(resume_text):

    prompt = f"""
You are an expert resume and career analyst.

Analyze the following resume:

{resume_text}

Provide the following:

1. A short professional resume summary.
2. Top 5 strengths.
3. Top 5 weaknesses or improvement areas.
4. 5 specific suggestions to improve the resume.
5. Important skills that should be highlighted.
6. Overall career improvement advice.

Keep the response clear, professional, and easy to understand.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text