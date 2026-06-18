import os
import sys

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(0, ROOT_DIR)

from seleniumbase import BaseCase
from utils.gmail_helper import authenticate_gmail


class TestStanfordSSO(BaseCase):

    def test_stanford_sso_redirect(self):

        # ----------------------------
        # Stanford Survey URL
        # ----------------------------

        self.open(
            "https://stanford.dev.bestopinions.us/user/surveys/2625142"
        )

        self.sleep(5)

        print("\n===== INITIAL STATE =====")

        print(
            f"Current URL: "
            f"{self.get_current_url()}"
        )

        print(
            f"Page Title: "
            f"{self.get_page_title()}"
        )

        self.save_screenshot_to_logs(
            "01_login_page"
        )

        # ----------------------------
        # Stanford Button
        # ----------------------------

        self.wait_for_text(
            "Continue with Stanford",
            timeout=30,
        )

        print(
            "\nStanford button detected."
        )

        self.highlight(
            "div.jss23"
        )

        self.save_screenshot_to_logs(
            "02_before_click"
        )

        print(
            "\nAttempting Stanford SSO..."
        )

        self.js_click(
            "div.jss23"
        )

        self.sleep(10)

        # ----------------------------
        # Validate Microsoft Redirect
        # ----------------------------

        current_url = (
            self.get_current_url()
        )

        print(
            "\n===== AFTER CLICK ====="
        )

        print(
            f"Current URL: "
            f"{current_url}"
        )

        print(
            f"Title: "
            f"{self.get_page_title()}"
        )

        self.save_screenshot_to_logs(
            "03_microsoft_login"
        )

        self.assert_url_contains(
            "login.microsoftonline.com"
        )

        print(
            "\n Microsoft login page detected."
        )

        # ----------------------------
        # Gmail Validation
        # ----------------------------

        print(
            "\n===== GMAIL AUTH CHECK ====="
        )

        gmail = authenticate_gmail()

        self.assert_true(
            gmail is not None
        )

        print(
            "\n Gmail authentication validated."
        )

        print(
            "\n===== TEST PASSED ====="
        )
