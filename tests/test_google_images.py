from seleniumbase import BaseCase


class TestGoogleImages(BaseCase):

    def test_google_images(self):
        self.open("https://www.google.com")

        # Save screenshot immediately
        self.save_screenshot_to_logs("01_google_home")

        # Search
        self.type('textarea[name="q"]', "cat images")
        self.send_keys('textarea[name="q"]', "\n")

        # Wait a little
        self.sleep(5)

        # Save search results screenshot
        self.save_screenshot_to_logs("02_search_results")

        # Check page title instead
        self.assert_title_contains("cat images")

        print("PASS!")
