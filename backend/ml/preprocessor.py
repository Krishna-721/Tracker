import re
import html

def clean_email(text: str) -> str:
    text = html.unescape(text)

    # Strip CSS blocks
    text = re.sub(r'@[a-zA-Z-]+\s*\{[^}]*\}', '', text)
    # Strip Unicode zero-width/invisible characters
    text = re.sub(r'[\u200b-\u200f\u202a-\u202e\ufeff\u00ad]', '', text)
    # Strip URLs
    text = re.sub(r'http\S+', '', text)

    text = re.sub(r'<[^>]+>', ' ', text)

    boilerplate_patterns = [
        r'unsubscribe.*',
        r'copyright.*',
        r'privacy policy.*',
        r'all rights reserved.*',
        r'you are receiving this.*',
        r'to stop receiving.*',
    ]
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # 4. Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text