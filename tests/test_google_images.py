from seleniumbase import BaseCase


class TestGoogleImages(BaseCase):

    def test_google_images(self):
        # Open Google
        self.open("https://www.google.com")

        # Take screenshot of initial page
        self.save_screenshot_to_logs("01_google_home")

        # Search for cat images
        self.type('textarea[name="q"]', "cat images")
        self.send_keys('textarea[name="q"]', "\n")

        # Wait for results page
        self.sleep(5)

        # Take screenshot of search results
        self.save_screenshot_to_logs("02_search_results")

        # Verify that search completed successfully
        self.assert_title_contains("cat images")

        print("PASS: Google search worked successfully")
