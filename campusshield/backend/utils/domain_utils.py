# backend/utils/domain_utils.py

import re

def extract_domain(url: str) -> str:
    """
    Extracts the bare domain from any URL format.
    
    Examples:
      https://fees-nitbhopal-edu.in/pay  →  fees-nitbhopal-edu.in
      http://phonepe-refund.xyz/claim    →  phonepe-refund.xyz
      nitbhopal.ac.in                    →  nitbhopal.ac.in  (already bare)
    """
    # Remove http:// or https://
    url = re.sub(r"https?://", "", url.strip())
    
    # Remove www. prefix if present
    url = re.sub(r"^www\.", "", url)
    
    # Take everything before the first / or ?
    domain = url.split("/")[0].split("?")[0]
    
    return domain.lower()


def extract_domain_base(domain: str) -> str:
    """
    Extracts just the name part before the TLD, for Levenshtein comparison.
    
    Examples:
      fees-nitbhopal-edu.in   →  fees-nitbhopal-edu
      nitbhopal.ac.in         →  nitbhopal       (strips .ac.in)
      phonepe.com             →  phonepe
    """
    # Split on dots and take the first meaningful part
    parts = domain.split(".")
    return parts[0].lower()