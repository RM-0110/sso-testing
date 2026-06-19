import json
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from utils.send_email import send_email


RESULT_DIR = "results"


def load_result(filename):

    path = os.path.join(
        RESULT_DIR,
        filename,
    )

    if not os.path.exists(path):
        return {
            "browser": filename.replace(
                ".json",
                "",
            ),
            "status": "NOT_RUN",
            "error": None,
        }

    with open(path, "r") as f:
        return json.load(f)


def build_summary():

    browsers = [
        "chrome",
        "firefox",
        "edge",
        "safari",
    ]

    results = []

    for browser in browsers:

        results.append(
            load_result(
                f"{browser}.json"
            )
        )

    overall_status = "PASS"

    body = []

    body.append(
        "Stanford SSO Automation Report"
    )

    body.append("")
    body.append("=" * 40)
    body.append("")

    for result in results:

        browser = result.get(
            "browser"
        )

        status = result.get(
            "status"
        )

        if status != "PASS":
            overall_status = "FAIL"

        body.append(
            f"{browser.upper()}: {status}"
        )

    body.append("")
    body.append("=" * 40)
    body.append("")

    body.append(
        "Failure Details"
    )

    body.append("")

    for result in results:

        if result.get(
            "status"
        ) == "FAIL":

            body.append(
                f"{result['browser'].upper()}:"
            )

            body.append(
                result.get(
                    "error",
                    "Unknown Error",
                )
            )

            body.append("")

    body.append(
        f"Overall Status: {overall_status}"
    )

    email_body = "\n".join(body)

    subject = (
        f"Stanford SSO Health Check - "
        f"{overall_status}"
    )

    print(email_body)

    send_email(
        subject=subject,
        body=email_body,
    )


if __name__ == "__main__":
    build_summary()
