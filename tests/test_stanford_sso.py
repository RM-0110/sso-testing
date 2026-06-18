from seleniumbase import BaseCase
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from utils.gmail_helper import (
    get_latest_navya_otp,
)

class TestStanfordSSO(BaseCase):

    def test_stanford_sso_redirect(self):

        self.open(
            "https://stanford.dev.bestopinions.us/user/surveys/2625142"
        )

        self.sleep(5)

        print("\n===== INITIAL STATE =====")

        print(
            f"Current URL: {self.get_current_url()}"
        )

        print(
            f"Page Title: {self.get_page_title()}"
        )

        self.save_screenshot_to_logs(
            "01_login_page"
        )

        self.wait_for_text(
            "Continue with Stanford",
            timeout=30,
        )

        print("\nStanford button detected.")

        self.highlight("div.jss23")

        self.save_screenshot_to_logs(
            "02_before_click"
        )

        print("\nAttempting Stanford SSO...")

        self.js_click("div.jss23")

        self.sleep(10)

        print("\n===== AFTER CLICK =====")

        print(
            f"Current URL: {self.get_current_url()}"
        )

        print(
            f"Title: {self.get_page_title()}"
        )

        self.save_screenshot_to_logs(
            "03_microsoft_login"
        )

        self.assert_url_contains(
            "login.microsoftonline.com"
        )

        print(
            "[PASS] Microsoft login page detected."
        )

        self.wait_for_element(
            "#i0116",
            timeout=30,
        )

        self.type(
            "#i0116",
            "riddhimann@navya.care",
        )

        self.save_screenshot_to_logs(
            "04_username_entered"
        )

        self.click("#idSIButton9")

        print(
            "[PASS] Username entered."
        )

        self.sleep(10)

        print(
            "\n===== FETCHING OTP ====="
        )

        otp = get_latest_navya_otp()

        self.wait_for_element(
            "#idTxtBx_OTC_Password",
            timeout=60,
        )

        self.type(
            "#idTxtBx_OTC_Password",
            otp,
        )

        self.save_screenshot_to_logs(
            "05_otp_entered"
        )

        print("[PASS] OTP entered.")

        self.click("#idSIButton9")

        print("[PASS] Sign In clicked.")

        print(
            "\nWaiting for Stanford redirect..."
        )

        self.sleep(10)

        print(
            "\n===== AFTER LOGIN ====="
        )

        print(
            f"Current URL: {self.get_current_url()}"
        )

        print(
            f"Title: {self.get_page_title()}"
        )

        self.wait_for_element(
            "#page_title",
            timeout=60,
        )

        self.assert_text(
            "Summary ID",
            "#page_title",
        )

        self.save_screenshot_to_logs(
            "06_survey_loaded"
        )

        print(
            "[PASS] Survey page loaded."
        )

        print(
            "[PASS] Expert successfully authenticated."
        )

        print(
            "\n===== FINAL RESULT ====="
        )

        print(
            "[PASS] Stanford SSO completed."
        )

        print(
            "[PASS] OTP authentication successful."
        )

        print(
            "[PASS] Survey page accessible."
        )

        print(
            "[PASS] Expert login verified."
        )
