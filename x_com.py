from playwright.sync_api import sync_playwright
import time
import random
import os


def human_delay(min_ms=800, max_ms=2000):
    """Random human-like pause between actions."""
    delay = random.randint(min_ms, max_ms)
    time.sleep(delay / 1000)


def signup_x(name, email, month, day, year):

    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    month_name = months[int(month) - 1]
    day_label   = str(int(day))    # e.g. "17"  (no leading zero)
    year_label  = str(int(year))   # e.g. "2005"

    print(f"[INFO] Signing up: Name={name}, Email={email}, DOB={month_name} {day_label} {year_label}")

    with sync_playwright() as p:

        # Persistent profile directory — reusing it makes the browser
        # look like a real returning user (helps bypass human verification)
        user_data_dir = os.path.join(os.path.expanduser("~"), ".x_signup_profile")
        os.makedirs(user_data_dir, exist_ok=True)

        context = p.chromium.launch_persistent_context(
            user_data_dir,           # <-- required positional argument
            headless=False,
            slow_mo=150,
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
        )

        page = context.new_page()

        # ---- Open signup page ----
        page.goto("https://twitter.com/i/flow/signup", wait_until="domcontentloaded")
        human_delay(2000, 4000)

        # ---- Click "Create account" ----
        create_btn = page.locator("button:has-text('Create account')")
        create_btn.wait_for(timeout=30000)
        human_delay(500, 1500)
        create_btn.click()

        # ---- Wait for signup form ----
        page.get_by_role("textbox", name="Name").wait_for(timeout=30000)
        human_delay(800, 1500)

        # ---- Fill Name (character by character) ----
        name_field = page.get_by_role("textbox", name="Name")
        name_field.click()
        human_delay(300, 700)
        name_field.type(name, delay=random.randint(80, 150))
        print("[INFO] Name filled")
        human_delay(700, 1500)

        # ---- Fill Email ----
        email_field = page.locator("input[type='email']")
        email_field.click()
        human_delay(300, 700)
        email_field.type(email, delay=random.randint(80, 150))
        print("[INFO] Email filled")
        human_delay(800, 1800)

        # ---- Wait for birthday dropdowns ----
        page.locator("select").first.wait_for(timeout=30000)
        human_delay(600, 1200)

        # ---- Month (use input value) ----
        page.locator("select").nth(0).select_option(label=month_name)
        print(f"[INFO] Month set to: {month_name}")
        human_delay(600, 1200)

        # ---- Day (use input value) ----
        page.locator("select").nth(1).select_option(label=day_label)
        print(f"[INFO] Day set to: {day_label}")
        human_delay(600, 1200)

        # ---- Year (use input value) ----
        page.locator("select").nth(2).select_option(label=year_label)
        print(f"[INFO] Year set to: {year_label}")
        human_delay(800, 1600)

        print("[INFO] Birthday selected successfully")

        # ---- Next (page 1 → 2) ----
        page.get_by_role("button", name="Next").click()
        human_delay(2000, 3500)

        # ---- Next (page 2 → 3) ----
        page.get_by_role("button", name="Next").click()
        human_delay(2000, 3500)

        # ---- Sign up ----
        page.get_by_role("button", name="Sign up").click()
        print("[INFO] Signup submitted — waiting for verification...")
        human_delay(3000, 5000)

        # ---- OTP / Email verification ----
        code = input("Enter Verification Code: ")
        human_delay(500, 1000)

        page.locator("input").last.click()
        human_delay(300, 600)
        page.locator("input").last.type(code, delay=random.randint(100, 200))
        human_delay(700, 1500)

        page.get_by_role("button", name="Next").click()
        print("[INFO] Verification code submitted")

        human_delay(4000, 6000)
        context.close()   # close persistent context (no separate browser object)
        print("[INFO] Done — browser closed.")


# -------- Inputs --------

name  = input("Enter Name: ")
email = input("Enter Email: ")
month = input("Enter Month Number (1-12): ")
day   = input("Enter Day (1-31): ")
year  = input("Enter Year (example 2000): ")

signup_x(name, email, month, day, year)