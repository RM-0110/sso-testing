from seleniumbase import BaseCase


class TestStanfordSSO(BaseCase):

    def test_stanford_sso_redirect(self):
        # Step 1: Open survey URL
        self.open(
            "https://stanford.dev.bestopinions.us/user/surveys/2625142"
        )

        # Allow the automatic redirect to /login
        self.sleep(5)

        print("\n===== INITIAL STATE =====")
        print("Current URL:")
        print(self.get_current_url())

        print("\nPage Title:")
        print(self.get_page_title())

        self.save_screenshot_to_logs("01_login_page")

        # Step 2: Wait for Stanford button text
        self.wait_for_text("Continue with Stanford", timeout=30)

        print("\nStanford button detected.")

        # Highlight the element we're about to click
        self.highlight("div.jss23")

        self.save_screenshot_to_logs("02_before_click")

        print("\nURL before click:")
        print(self.get_current_url())

        print("\nWindow handles before click:")
        print(self.driver.window_handles)

        # Step 3: Force click
        print("\nAttempting JavaScript click on div.jss23...")
        self.js_click("div.jss23")

        # Give redirect time to happen
        self.sleep(10)

        print("\n===== AFTER CLICK =====")

        print("\nURL immediately after click:")
        print(self.get_current_url())

        print("\nWindow handles after click:")
        print(self.driver.window_handles)

        self.save_screenshot_to_logs("03_after_click")

        found_microsoft = False

        # Step 4: Check all open windows/tabs
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

        print("\n===== FINAL RESULT =====")

        if found_microsoft:
            print("PASS: Microsoft login page detected.")
        else:
            print("FAIL: Microsoft login page not found.")

        self.assert_true(
            found_microsoft,
            "Microsoft login page was not found "
            "in any open tab/window."
        )
