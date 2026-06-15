from seleniumbase import BaseCase


class TestStanfordSSO(BaseCase):

    def test_stanford_sso_redirect(self):
        # Step 1: Open the application
        self.open("https://stanford.dev.bestopinions.us/login")

        # Capture initial state
        self.save_screenshot_to_logs("01_login_page")

        # Step 2: Click the Stanford SSO button
        self.wait_for_text("Continue with Stanford", timeout=30)
        self.click('*:contains("Continue with Stanford")')

        # Step 3: Wait for Microsoft login page to load
        self.wait_for_element('img.logo[alt="Microsoft"]', timeout=60)

        # Capture redirected page
        self.save_screenshot_to_logs("02_microsoft_login")

        # Step 4: Assert Microsoft logo exists
        self.assert_element('img.logo[alt="Microsoft"]')

        print("PASS: Successfully redirected to Microsoft login page")
