from seleniumbase import BaseCase


class TestGoogleImages(BaseCase):

    def test_google_images(self):
        # Open Google
        self.open("https://www.google.com")

        # Search for cat images
        self.type('textarea[name="q"]', "cat images\n")

        # Verify that the Images tab appears
        self.wait_for_element('a[href*="tbm=isch"]', timeout=20)

        self.assert_element('a[href*="tbm=isch"]')

        print("PASS: Images tab found")