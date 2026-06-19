from seleniumbase import BaseCase

from utils.gmail_helper import (
get_latest_navya_otp,
)

class TestStanfordSSO(BaseCase):

    def test_stanford_sso_redirect(self):

        # ---------------------------------
        # Open Stanford Survey
        # ---------------------------------
        
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
        
        # ---------------------------------
        # Click Stanford SSO
        # ---------------------------------
        
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
        
        print(
            "\n===== AFTER CLICK ====="
        )
        
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
        
        # ---------------------------------
        # Enter Email
        # ---------------------------------
        
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
        
        self.click(
            "#idSIButton9"
        )
        
        print(
            "[PASS] Username entered."
        )
        
        # ---------------------------------
        # Fetch OTP
        # ---------------------------------
        
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
        
        print(
            "[PASS] OTP entered."
        )
        
        self.click(
            "#idSIButton9"
        )
        
        print(
            "[PASS] Sign In clicked."
        )
        
        # ---------------------------------
        # Wait for Stanford Redirect
        # ---------------------------------
        
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
        
        # ---------------------------------
        # Authorization Validation
        # ---------------------------------
        
        print(
            "\nChecking authorization status..."
        )
        
        unauthorized_elements = self.find_elements(
            ".alert-message"
        )
        
        for element in unauthorized_elements:
        
            text = element.text.strip()
        
            print(
                f"Alert detected: {text}"
            )
        
            if (
                "Not authorised for the case"
                in text
            ):
                self.save_screenshot_to_logs(
                    "07_authorization_failure"
                )
        
                raise Exception(
                    "FAIL: User authenticated successfully "
                    "but is not authorized to access "
                    "the survey."
                )
        
        print(
            "[PASS] Survey authorization validated."
        )
        
        # ---------------------------------
        # Validate Survey Page
        # ---------------------------------
        
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
