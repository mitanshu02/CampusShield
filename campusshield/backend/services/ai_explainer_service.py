# backend/services/ai_explainer_service.py

import json
import google.generativeai as genai
from groq import Groq
from config import GEMINI_API_KEY, GROQ_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

SAFE_FALLBACK = {
    "explanation": "This URL appears to be legitimate. Our scan found no signs of phishing, typosquatting, or suspicious activity. You can visit this website safely.",
    "impersonation_statement": "No specific impersonation target identified.",
    "attack_type": "No threat detected"
}

THREAT_FALLBACK = {
    "explanation": "This URL shows signs of being a phishing attempt targeting college students. Attackers create fake versions of trusted websites to steal payment details or login credentials. If you had visited this page and entered your information, it would have gone directly to a scammer.",
    "impersonation_statement": "No specific impersonation target identified.",
    "attack_type": "Phishing Attempt"
}

UPI_FALLBACK = {
    "explanation": "This page is designed to steal your UPI payment credentials. It asks for your UPI PIN directly on a webpage — something no legitimate payment app ever does. If you had entered your PIN here, a scammer would have instant access to your bank account.",
    "impersonation_statement": "No specific impersonation target identified.",
    "attack_type": "UPI Collect Fraud"
}

def build_prompt(signals: dict, risk_score: int, url: str) -> str:
    if risk_score < 40:
        tone = "SAFE — confirm the URL is legitimate and explain what was checked"
    elif risk_score < 70:
        tone = "CAUTIOUS — explain mild concern without alarming"
    else:
        tone = "THREAT — explain the danger clearly and specifically"

    # extract payment signals if present
    payment_signals  = signals.get("payment_signals", [])
    payment_risk     = signals.get("payment_risk", 0)
    payment_context  = ""

    if payment_signals:
        signal_names    = [s.get("signal", "") for s in payment_signals]
        payment_context = f"""
Payment fraud signals found (payment risk: {payment_risk}/100):
{chr(10).join(f'- {s}' for s in signal_names)}

IMPORTANT: Since payment fraud signals exist, your explanation MUST:
- Mention that the page requests UPI PIN on a webpage
- Explain this is a classic UPI collect fraud technique
- Set attack_type to exactly: UPI Collect Fraud
"""

    return f"""You are a cybersecurity educator explaining URL scan results to college students.

URL scanned: {url}
Overall risk score: {risk_score} out of 100
Tone required: {tone}
URL signals detected: {json.dumps(signals.get("url_signals", signals))}
{payment_context}
CRITICAL RULES:
- If risk_score is below 40, attack_type MUST be exactly: No threat detected
- If risk_score is below 40, explanation must be reassuring not threatening
- Never say "threat" or "scam" when risk_score is below 40
- Keep explanation to exactly 3 sentences
- Be specific — mention the actual signals found

Generate a response in this exact JSON format with no extra text, no markdown, no code fences:
{{
  "explanation": "Three sentences matching the tone. Be specific about what was found.",
  "impersonation_statement": "One sentence naming which institution or brand is being impersonated if typosquatting was found. Otherwise write exactly: No specific impersonation target identified.",
  "attack_type": "3 words or less. Choose from: UPI Collect Fraud, Fee Portal Impersonation, Scholarship Scam, Domain Spoofing, Exam Result Phish, Phishing Attempt, No threat detected."
}}"""


def call_groq(signals: dict, risk_score: int, url: str) -> dict | None:
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "user",
                "content": build_prompt(signals, risk_score, url)
            }],
            max_tokens=400,
            temperature=0.2,
        )
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)

        if risk_score < 40:
            result["attack_type"] = "No threat detected"

        return result
    except Exception as e:
        print(f"Groq failed: {e}")
        return None


def call_gemini(signals: dict, risk_score: int, url: str) -> dict | None:
    try:
        model    = genai.GenerativeModel("gemini-2.0-flash-lite")
        response = model.generate_content(
            build_prompt(signals, risk_score, url)
        )
        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text)

        if risk_score < 40:
            result["attack_type"] = "No threat detected"

        return result
    except Exception as e:
        print(f"Gemini failed: {e}")
        return None


def generate_explanation(
    signals:    dict,
    risk_score: int = 0,
    url:        str = ""
) -> dict:
    result = call_groq(signals, risk_score, url)
    if result:
        return result

    result = call_gemini(signals, risk_score, url)
    if result:
        return result

    # smart fallback based on what signals exist
    if signals.get("payment_signals") and risk_score >= 40:
        return UPI_FALLBACK

    return SAFE_FALLBACK if risk_score < 40 else THREAT_FALLBACK

# # backend/services/ai_explainer_service.py

# import json
# import google.generativeai as genai
# from groq import Groq
# from config import GEMINI_API_KEY, GROQ_API_KEY

# genai.configure(api_key=GEMINI_API_KEY)
# groq_client = Groq(api_key=GROQ_API_KEY)

# SAFE_FALLBACK = {
#     "explanation": "This URL appears to be legitimate. Our scan found no signs of phishing, typosquatting, or suspicious activity. You can visit this website safely.",
#     "impersonation_statement": "No specific impersonation target identified.",
#     "attack_type": "No threat detected"
# }

# THREAT_FALLBACK = {
#     "explanation": "This URL shows signs of being a phishing attempt targeting college students. Attackers create fake versions of trusted websites to steal payment details or login credentials. If you had visited this page and entered your information, it would have gone directly to a scammer.",
#     "impersonation_statement": "No specific impersonation target identified.",
#     "attack_type": "Phishing Attempt"
# }

# def build_prompt(signals: dict, risk_score: int, url: str) -> str:
#     if risk_score < 40:
#         tone = "SAFE — confirm the URL is legitimate and explain what was checked"
#     elif risk_score < 70:
#         tone = "CAUTIOUS — explain mild concern without alarming"
#     else:
#         tone = "THREAT — explain the danger clearly"

#     return f"""You are a cybersecurity educator explaining URL scan results to college students.

# URL scanned: {url}
# Risk score: {risk_score} out of 100
# Tone required: {tone}
# Signals detected: {json.dumps(signals)}

# CRITICAL RULES:
# - If risk_score is below 40, attack_type MUST be exactly: No threat detected
# - If risk_score is below 40, explanation must be reassuring not threatening
# - Never say "threat" or "scam" when risk_score is below 40
# - Keep explanation to exactly 3 sentences

# Generate a response in this exact JSON format with no extra text, no markdown, no code fences:
# {{
#   "explanation": "Three sentences matching the tone above.",
#   "impersonation_statement": "One sentence naming the impersonation target if risk_score above 50 and typosquatting found. Otherwise write exactly: No specific impersonation target identified.",
#   "attack_type": "3 words or less. For safe URLs write exactly: No threat detected. For threats: Fee Portal Impersonation, UPI Collect Fraud, Scholarship Scam, Domain Spoofing, Exam Result Phish."
# }}"""


# def call_groq(signals: dict, risk_score: int, url: str) -> dict | None:
#     try:
#         response = groq_client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[{
#                 "role": "user",
#                 "content": build_prompt(signals, risk_score, url)
#             }],
#             max_tokens=400,
#             temperature=0.2,
#         )
#         text = response.choices[0].message.content.strip()
#         text = text.replace("```json", "").replace("```", "").strip()
#         result = json.loads(text)

#         # safety override — never show threat label for safe URLs
#         if risk_score < 40:
#             result["attack_type"] = "No threat detected"

#         return result
#     except Exception as e:
#         print(f"Groq failed: {e}")
#         return None


# def call_gemini(signals: dict, risk_score: int, url: str) -> dict | None:
#     try:
#         model    = genai.GenerativeModel("gemini-2.0-flash-lite")
#         response = model.generate_content(
#             build_prompt(signals, risk_score, url)
#         )
#         text = response.text.strip()
#         text = text.replace("```json", "").replace("```", "").strip()
#         result = json.loads(text)

#         # safety override
#         if risk_score < 40:
#             result["attack_type"] = "No threat detected"

#         return result
#     except Exception as e:
#         print(f"Gemini failed: {e}")
#         return None


# def generate_explanation(
#     signals: dict,
#     risk_score: int = 0,
#     url: str = ""
# ) -> dict:
#     result = call_groq(signals, risk_score, url)
#     if result:
#         return result

#     result = call_gemini(signals, risk_score, url)
#     if result:
#         return result

#     return SAFE_FALLBACK if risk_score < 40 else THREAT_FALLBACK
