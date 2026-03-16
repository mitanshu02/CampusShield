# backend/utils/domain_utils.py

import re

def extract_domain(url: str) -> str:
    """Extracts bare domain from any URL format."""
    url = re.sub(r"https?://", "", url.strip())
    url = re.sub(r"^www\.", "", url)
    domain = url.split("/")[0].split("?")[0]
    return domain.lower()


def extract_domain_base(domain: str) -> str:
    """Extracts just the name part before the TLD."""
    parts = domain.split(".")
    return parts[0].lower()


def extract_tld(domain: str) -> str:
    """
    Extracts the TLD/extension from a domain.
    
    Examples:
      nitbhopal.ac.in  →  ac.in
      phonepe.com      →  com
      amity.edu        →  edu
    """
    parts = domain.split(".")
    if len(parts) >= 3:
        return ".".join(parts[-2:])  # e.g. ac.in, co.in
    elif len(parts) == 2:
        return parts[-1]             # e.g. com, edu
    return ""


def get_shared_keywords(domain1: str, domain2: str) -> list:
    """
    Finds common keywords of 4+ characters between two domain bases.
    
    Example:
      fees-nitbhopal-edu  vs  nitbhopal  →  ['nitbhopal']
      skitm               vs  amity      →  []
    """
    # Split on hyphens and dots to get individual words
    words1 = set(re.split(r"[-.]", domain1.lower()))
    words2 = set(re.split(r"[-.]", domain2.lower()))

    # Only count words with 4+ characters
    shared = [w for w in words1 & words2 if len(w) >= 4]
    return shared


def is_valid_typosquat_match(
    suspicious_domain: str,
    legitimate_domain: str,
    distance: int
) -> bool:
    """
    Returns True only if ALL three conditions are met:
    1. Levenshtein distance is 2 or less
    2. Domains share at least one common keyword of 4+ characters
    3. TLD/extension is similar
    """
    # Condition 1 — distance must be 2 or less
    if distance > 2:
        return False

    # Condition 2 — must share at least one keyword of 4+ characters
    sus_base = extract_domain_base(suspicious_domain)
    leg_base = extract_domain_base(legitimate_domain)
    shared   = get_shared_keywords(sus_base, leg_base)
    if not shared:
        return False

    # Condition 3 — TLD must be similar
    sus_tld = extract_tld(suspicious_domain)
    leg_tld = extract_tld(legitimate_domain)

    # Both Indian domains, or both same TLD
    indian_tlds = {"ac.in", "co.in", "in", "edu.in", "org.in"}
    both_indian = sus_tld in indian_tlds and leg_tld in indian_tlds
    same_tld    = sus_tld == leg_tld

    if not (both_indian or same_tld):
        return False

    return True