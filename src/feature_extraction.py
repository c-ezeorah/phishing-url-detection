import re
from urllib.parse import urlparse

URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly",
    "buff.ly", "is.gd", "cutt.ly", "rb.gy"
}

IPV4_RE = re.compile(
    r"^(?:\d{1,3}\.){3}\d{1,3}$"
)

def normalize_url(url: str) -> str:
    """Add a scheme when needed so urllib can parse the hostname."""
    url = url.strip()
    if "://" not in url:
        url = "http://" + url
    return url

def extract_lexical_features(url: str) -> dict:
    """
    Extract lightweight lexical URL features for phishing detection.

    This is an initial Progress Report 1 prototype. It focuses on features
    that can be computed directly from the URL string without network calls.
    """
    normalized = normalize_url(url)
    parsed = urlparse(normalized)
    host = (parsed.hostname or "").lower()
    raw = url.strip()

    special_chars = "-_@?=&%./:#"

    return {
        "url": raw,
        "url_length": len(raw),
        "hostname_length": len(host),
        "num_dots": raw.count("."),
        "num_hyphens": raw.count("-"),
        "num_at_symbols": raw.count("@"),
        "num_question_marks": raw.count("?"),
        "num_equal_signs": raw.count("="),
        "num_digits": sum(ch.isdigit() for ch in raw),
        "num_special_chars": sum(ch in special_chars for ch in raw),
        "uses_https": int(raw.lower().startswith("https://")),
        "contains_ip_address": int(bool(IPV4_RE.match(host))),
        "uses_known_shortener": int(host in URL_SHORTENERS),
    }

if __name__ == "__main__":
    demo_urls = [
        "https://example.com",
        "https://accounts.example.com/login",
        "http://192.0.2.10/verify-account",
        "https://tinyurl.com/demo-link",
        "http://secure-login-example.com/account?user=12345"
    ]

    for url in demo_urls:
        print(extract_lexical_features(url))
