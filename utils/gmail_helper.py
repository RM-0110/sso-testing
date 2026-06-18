import os
import json
import base64
import re
import datetime

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
"https://www.googleapis.com/auth/gmail.readonly"
]

OTP_SUBJECT = (
"Your Navya Network account verification code"
)

def authenticate_gmail():
"""
Authenticates Gmail using GitHub secrets.

```
Uses:
GMAIL_TOKEN_JSON
GMAIL_CREDENTIALS_JSON

Fails hard if token is invalid,
expired, or revoked.
"""

token_json = os.environ.get(
    "GMAIL_TOKEN_JSON"
)

credentials_json = os.environ.get(
    "GMAIL_CREDENTIALS_JSON"
)

if not token_json:
    raise Exception(
        "FATAL ERROR: "
        "GMAIL_TOKEN_JSON secret not found."
    )

if not credentials_json:
    raise Exception(
        "FATAL ERROR: "
        "GMAIL_CREDENTIALS_JSON secret not found."
    )

creds = Credentials.from_authorized_user_info(
    json.loads(token_json),
    SCOPES,
)

try:
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

except Exception as e:
    raise Exception(
        "FATAL ERROR: "
        "Refresh token expired or revoked. "
        "Regenerate token.json and update "
        "GMAIL_TOKEN_JSON secret."
    ) from e

gmail = build(
    "gmail",
    "v1",
    credentials=creds,
)

profile = gmail.users().getProfile(
    userId="me"
).execute()

email = profile.get(
    "emailAddress",
    "unknown"
)

print(
    f"[PASS] Gmail authenticated successfully: "
    f"{email}"
)

return gmail
```

def get_message_body(
gmail,
message_id,
):
message = gmail.users().messages().get(
userId="me",
id=message_id,
format="full",
).execute()

```
payload = message.get(
    "payload",
    {}
)

data = None

if payload.get(
    "body",
    {}
).get(
    "data"
):
    data = payload["body"]["data"]

else:
    parts = payload.get(
        "parts",
        []
    )

    for part in parts:
        body = part.get(
            "body",
            {}
        )

        if body.get(
            "data"
        ):
            data = body["data"]
            break

if not data:
    return ""

decoded = base64.urlsafe_b64decode(
    data
).decode(
    "utf-8",
    errors="ignore",
)

return decoded
```

def get_latest_navya_otp():
"""
Finds newest OTP email.

```
Subject:
Your Navya Network account verification code

Returns:
8 digit OTP
"""

gmail = authenticate_gmail()

query = (
    'subject:"'
    + OTP_SUBJECT
    + '" newer_than:1d'
)

response = gmail.users().messages().list(
    userId="me",
    q=query,
    maxResults=20,
).execute()

messages = response.get(
    "messages",
    []
)

if not messages:
    raise Exception(
        "FATAL ERROR: "
        "No OTP emails found."
    )

now = datetime.datetime.utcnow()

for message in messages:

    msg = gmail.users().messages().get(
        userId="me",
        id=message["id"],
        format="metadata",
    ).execute()

    internal_date = int(
        msg["internalDate"]
    )

    email_time = (
        datetime.datetime.utcfromtimestamp(
            internal_date / 1000
        )
    )

    age_minutes = (
        now - email_time
    ).total_seconds() / 60

    if age_minutes > 10:
        continue

    body = get_message_body(
        gmail,
        message["id"],
    )

    match = re.search(
        r"\b(\d{8})\b",
        body,
    )

    if match:
        otp = match.group(1)

        print(
            "[PASS] OTP email found."
        )

        return otp

raise Exception(
    "FATAL ERROR: "
    "No valid OTP found in recent emails."
)
```
