import base64
import html
import re

def extract_email_body(payload: dict) -> str:
    def decode(data):
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    def strip_html(text):
        text = html.unescape(text)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    # Case 1: Simple email with direct body
    if "body" in payload and payload["body"].get("data"):
        raw = decode(payload["body"]["data"])
        return raw if payload.get("mimeType") == "text/plain" else strip_html(raw)

    # Case 2: Multipart — prefer text/plain, fallback to text/html
    html_body = ""
    for part in payload.get("parts", []):
        mime = part.get("mimeType", "")
        if mime == "text/plain" and part["body"].get("data"):
            return decode(part["body"]["data"])
        if mime == "text/html" and part["body"].get("data"):
            html_body = strip_html(decode(part["body"]["data"]))

    # Case 3: Nested multipart
    for part in payload.get("parts", []):
        if "parts" in part:
            for subpart in part["parts"]:
                mime = subpart.get("mimeType", "")
                if mime == "text/plain" and subpart["body"].get("data"):
                    return decode(subpart["body"]["data"])
                if mime == "text/html" and subpart["body"].get("data"):
                    html_body = strip_html(decode(subpart["body"]["data"]))

    return html_body