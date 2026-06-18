import json
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


def authenticate_gmail():
    """
    Authenticates to Gmail using:
    - GMAIL_TOKEN_JSON
    - GMAIL_CREDENTIALS_JSON

    Returns:
        gmail service object

    Raises:
        RuntimeError with actionable message
    """

    token_secret = os.getenv("GMAIL_TOKEN_JSON")

    if not token_secret:
        raise RuntimeError(
            """
 FATAL ERROR: GMAIL_TOKEN_JSON secret not found.

Action required:
Add the complete contents of token.json to the
GMAIL_TOKEN_JSON GitHub Secret.

Workflow terminated because OTP retrieval
is a mandatory prerequisite for SSO validation.
"""
        )

    with open("token.json", "w") as f:
        f.write(token_secret)

    credentials_secret = os.getenv("GMAIL_CREDENTIALS_JSON")

    if credentials_secret:
        with open("credentials.json", "w") as f:
            f.write(credentials_secret)

    try:
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES,
        )

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        gmail = build(
            "gmail",
            "v1",
            credentials=creds,
        )

        profile = (
            gmail.users()
            .getProfile(userId="me")
            .execute()
        )

        print(
            f"Gmail authenticated successfully: "
            f"{profile.get('emailAddress')}"
        )

        return gmail

    except Exception as e:

        error_text = str(e)

        if (
            "invalid_grant" in error_text
            or "Token has been expired or revoked" in error_text
        ):
            raise RuntimeError(
                """
 FATAL ERROR: Gmail authentication failed.

Reason:
Google rejected the refresh token (invalid_grant).

Most likely causes:
- Refresh token expired
- Refresh token revoked
- New token.json invalidated the old token

Action required:
1. Regenerate token.json locally.
2. Update GMAIL_TOKEN_JSON secret.
3. Re-run workflow.

Workflow terminated because OTP retrieval
is a mandatory prerequisite for SSO validation.
"""
            )

        raise RuntimeError(
            f"""
FATAL ERROR: Gmail authentication failed.

Underlying error:
{error_text}

Workflow terminated.
"""
        )
