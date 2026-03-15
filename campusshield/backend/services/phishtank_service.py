# backend/services/phishtank_service.py

import requests

PHISHTANK_URL = "https://checkurl.phishtank.com/checkurl/"

def check_phishtank(url: str) -> dict:
    """
    Checks a URL against the PhishTank phishing database.
    Returns score 100 if listed, 0 if clean, 0 if check fails.
    """
    try:
        response = requests.post(
            PHISHTANK_URL,
            data={"url": url, "format": "json"},
            headers={"User-Agent": "CampusShield/1.0"},
            timeout=5
        )

        data = response.json()
        results = data.get("results", {})

        in_database = results.get("in_database", False)
        is_valid    = results.get("valid", False)

        if in_database and is_valid:
            return {
                "score": 100,
                "detail": "URL is listed in PhishTank as a confirmed phishing site",
                "listed": True
            }
        else:
            return {
                "score": 0,
                "detail": "URL not found in PhishTank database",
                "listed": False
            }

    except requests.Timeout:
        return {
            "score": 0,
            "detail": "PhishTank check timed out — skipped",
            "listed": None
        }
    except Exception as e:
        return {
            "score": 0,
            "detail": f"PhishTank check failed: {str(e)}",
            "listed": None
        }