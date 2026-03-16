# backend/services/ai_explainer_service.py

import json
import google.generativeai as genai
from groq import Groq
from config import GEMINI_API_KEY, GROQ_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

FALLBACK_RESPONSE = {
    "explanation": "This URL shows multiple signs of being a phishing attempt targeting college students. Attackers create fake versions of trusted websites to steal payment details or login credentials. If you had visited this page and entered your information, it would have gone directly to a scammer.",
    "impersonation_statement": "No specific impersonation target identified.",
    "attack_type": "Phishing Attempt"
}

def build_prompt(signals: dict) -> str:
    return f"""You are a cybersecurity educator explaining threats to college students.
A URL scan has returned these signals: {json.dumps(signals)}

Generate a response in this exact JSON format with no extra text, no markdown, no code fences:
{{
  "explanation": "Three sentences in plain English for a non-technical college student. Sentence 1: what this threat is. Sentence 2: how it works. Sentence 3: what would have happened if they visited it.",
  "impersonation_statement": "One sentence specifically naming which institution or brand this URL is impersonating and how. If no clear impersonation target, write: No specific impersonation target identified.",
  "attack_type": "Attack pattern in 3 words or less. Examples: Fee Portal Impersonation, UPI Collect Fraud, Scholarship Scam, Domain Spoofing, Timing Based Phish."
}}"""


# def call_gemini(signals: dict) -> dict | None:
#     """Primary explainer — Gemini 1.5 Flash."""
#     try:
#         model    = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content(build_prompt(signals))
#         text     = response.text.strip()

#         # Strip markdown code fences if Gemini adds them
#         text = text.replace("```json", "").replace("```", "").strip()
#         return json.loads(text)
#     except Exception as e:
#         print(f"Gemini failed: {e}")
#         return None


# def call_groq(signals: dict) -> dict | None:
#     """Fallback explainer — Groq Llama 3.1 70B."""
#     try:
#         response = groq_client.chat.completions.create(
#             model="llama-3.1-70b-versatile",
#             messages=[{"role": "user", "content": build_prompt(signals)}],
#             max_tokens=400,
#             temperature=0.3,
#         )
#         text = response.choices[0].message.content.strip()
#         text = text.replace("```json", "").replace("```", "").strip()
#         return json.loads(text)
#     except Exception as e:
#         print(f"Groq failed: {e}")
#         return None
def call_gemini(signals: dict) -> dict | None:
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-lite")       
        response = model.generate_content(build_prompt(signals))
        text     = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Gemini failed: {e}")  # already there
        return None


def call_groq(signals: dict) -> dict | None:
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": build_prompt(signals)}],
            max_tokens=400,
            temperature=0.3,
        )
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Groq failed: {e}")  # already there
        return None
def generate_explanation(signals: dict) -> dict:
    """
    Tries Groq first (faster, higher limits), falls back to Gemini, 
    then static fallback. Never crashes.
    """
    result = call_groq(signals)
    if result:
        return result

    result = call_gemini(signals)
    if result:
        return result

    return FALLBACK_RESPONSE

def list_gemini_models():
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(m.name)