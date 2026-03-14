import re
import html

def clean_email(text: str) -> str:
    text = html.unescape(text)

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