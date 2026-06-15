from seleniumbase import BaseCase


class TestStanfordSSO(BaseCase):

    def test_stanford_sso_redirect(self):
        # Step 1: Open Stanford survey URL
        self.open("https://stanford.dev.bestopinions.us/user/surveys/2625142")

        self.save_screenshot_to_logs("01_survey_page")

        # Step 2: Click Stanford SSO button
        self.wait_for_text("Continue with Stanford", timeout=30)

        self.click('*:contains("Continue with Stanford")')

        # Give redirect time to happen
        self.sleep(10)

        # Capture what we actually got
        self.save_screenshot_to_logs("02_after_redirect")

        print("\nCURRENT URL:")
        print(self.get_current_url())

        print("\nPAGE TITLE:")
        print(self.get_page_title())

        print("\nBODY TEXT:")
        print(self.get_text("body"))

        # Assert that we reached Microsoft
        self.assert_url_contains("login.microsoftonline.com")

        print("PASS: Successfully redirected to Microsoft")
