from seleniumbase import BaseCase


class TestStanfordSSO(BaseCase):

    def test_stanford_sso_redirect(self):
        # Step 1: Open Stanford survey URL
        self.open(
            "https://stanford.dev.bestopinions.us/user/surveys/2625142"
        )

        self.save_screenshot_to_logs("01_survey_page")

        # Step 2: Wait for Stanford button
        self.wait_for_text("Continue with Stanford", timeout=30)

        print("\nURL before click:")
        print(self.get_current_url())

        print("\nWindows before click:")
        print(self.driver.window_handles)

        # Step 3: Force click using JavaScript
        self.js_click('*:contains("Continue with Stanford")')

        # Allow redirects/popups to happen
        self.sleep(10)

        print("\nWindows after click:")
        print(self.driver.window_handles)

        found_microsoft = False

        # Step 4: Check every open tab/window
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)

            self.sleep(2)

            current_url = self.get_current_url()
            current_title = self.get_page_title()

            print("\n==============================")
            print("Window Handle:", handle)
            print("URL:", current_url)
            print("Title:", current_title)
            print("==============================")

            self.save_screenshot_to_logs(
                f"window_{handle[-5:]}"
            )

            if (
                "microsoft" in current_url.lower()
                or "login.microsoftonline" in current_url.lower()
                or "live.com" in current_url.lower()
            ):
                found_microsoft = True
                print("\nMicrosoft authentication page found!")
                break

        self.assert_true(
            found_microsoft,
            "Microsoft login page was not found "
            "in any open tab/window."
        )

        print("\nPASS: Microsoft login page detected.")
