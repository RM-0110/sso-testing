from seleniumbase import BaseCase


class TestStanfordSSO(BaseCase):

    def test_stanford_sso_redirect(self):
        # Step 1: Open Stanford survey URL
        self.open(
            "https://stanford.dev.bestopinions.us/user/surveys/2625142"
        )

        # Capture initial state
        self.save_screenshot_to_logs("01_survey_page")

        # Step 2: Wait for Stanford SSO button
        self.wait_for_text("Continue with Stanford", timeout=30)

        print("\n===== BEFORE CLICK =====")
        print("Current URL:")
        print(self.get_current_url())

        print("\nWindow Handles:")
        print(self.driver.window_handles)

        # Step 3: Click Stanford button
        self.click('*:contains("Continue with Stanford")')

        # Allow redirect/popup to occur
        self.sleep(10)

        print("\n===== AFTER CLICK =====")
        print("Window Handles:")
        print(self.driver.window_handles)

        # Step 4: Switch to newest window if one exists
        if len(self.driver.window_handles) > 1:
            print("\nSwitching to newest window...")
            self.switch_to_newest_window()

        # Allow page to stabilize
        self.sleep(5)

        # Step 5: Capture evidence
        self.save_screenshot_to_logs("02_after_redirect")

        print("\nCurrent URL:")
        print(self.get_current_url())

        print("\nPage Title:")
        print(self.get_page_title())

        print("\nPage Body (first 1000 characters):")
        body_text = self.get_text("body")
        print(body_text[:1000])

        print("\n===== TEST COMPLETED =====")

        # Intentional pass while debugging
        self.assert_true(True)
