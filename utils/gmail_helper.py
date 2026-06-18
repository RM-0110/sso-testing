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

OTP_SUBJECT = "Your Navya Network account verification code"


def authenticate_gmail():
    token_json = os.environ.get("GMAIL_TOKEN_JSON")
    credentials_json = os.environ.get("GMAIL_CREDENTIALS_JSON")

    if not token_json:
        raise Exception(
            "FATAL ERROR: GMAIL_TOKEN_JSON secret not found."
        )

    if not credentials_json:
        raise Exception(
            "FATAL ERROR: GMAIL_CREDENTIALS_JSON secret not found."
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
            "FATAL ERROR: Refresh token expired or revoked. "
            "Regenerate token.json and update GMAIL_TOKEN_JSON secret."
        ) from e

    gmail = build(
        "gmail",
        "v1",
        credentials=creds,
    )

    profile = gmail.users().getProfile(
        userId="me"
    ).execute()

    print(
        f"[PASS] Gmail authenticated successfully: "
        f"{profile.get('emailAddress', 'unknown')}"
    )

    return gmail


def get_message_body(gmail, message_id):
    message = gmail.users().messages().get(
        userId="me",
        id=message_id,
        format="full",
    ).execute()

    payload = message.get("payload", {})

    data = None

    if payload.get("body", {}).get("data"):
        data = payload["body"]["data"]
    else:
        for part in payload.get("parts", []):
            if part.get("body", {}).get("data"):
                data = part["body"]["data"]
                break

    if not data:
        return ""

    return base64.urlsafe_b64decode(
        data
    ).decode(
        "utf-8",
        errors="ignore",
    )


def get_latest_navya_otp():
    gmail = authenticate_gmail()

    query = (
        f'subject:"{OTP_SUBJECT}" newer_than:1d'
    )

    response = gmail.users().messages().list(
        userId="me",
        q=query,
        maxResults=20,
    ).execute()

    messages = response.get("messages", [])

    if not messages:
        raise Exception(
            "FATAL ERROR: No OTP emails found."
        )

    now = datetime.datetime.utcnow()

    for message in messages:

        msg = gmail.users().messages().get(
            userId="me",
            id=message["id"],
            format="metadata",
        ).execute()

        email_time = (
            datetime.datetime.utcfromtimestamp(
                int(msg["internalDate"]) / 1000
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
            print("[PASS] OTP email found.")
            return match.group(1)

    raise Exception(
        "FATAL ERROR: No valid OTP found in recent emails."
    )
