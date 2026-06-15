from seleniumbase import BaseCase


class TestGoogle(BaseCase):

    def test_google(self):
        self.open("https://www.google.com")

        self.type('textarea[name="q"]', "cat images\n")

        self.wait_for_ready_state_complete()

        self.sleep(5)

        self.save_screenshot_to_logs("google_results")

        print(self.get_current_url())

        self.assert_url_contains("q=cat+images")

        print("PASS")
