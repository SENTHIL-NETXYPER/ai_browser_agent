from playwright.sync_api import sync_playwright
import time
import random


def human_delay(min_ms=500, max_ms=1200):
    time.sleep(random.randint(min_ms, max_ms) / 1000)


def type_like_human(field, text):
    field.scroll_into_view_if_needed()
    field.click()
    field.fill("")  # clear any text
    human_delay()

    for ch in text:
        field.type(ch)
        time.sleep(random.uniform(0.05, 0.12))


def run_test():

    firstname = "senthilmonerereri"
    surname = "kumar"

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("[INFO] Opening Facebook signup page...")

        page.goto(
            "https://www.facebook.com/reg/",
            wait_until="networkidle"
        )

        page.wait_for_timeout(3000)

        # ---- First Name ----
        print("[INFO] Typing first name...")

        first_box = page.get_by_role("textbox").nth(0)
        first_box.wait_for(state="visible")

        type_like_human(first_box, firstname)

        print("[INFO] First name entered")

        human_delay()

        # ---- Surname ----
        print("[INFO] Typing surname...")

        last_box = page.get_by_role("textbox").nth(1)
        last_box.wait_for(state="visible")

        type_like_human(last_box, surname)

        print("[INFO] Surname entered")

        page.wait_for_timeout(10000)

        browser.close()


if __name__ == "__main__":
    run_test()
