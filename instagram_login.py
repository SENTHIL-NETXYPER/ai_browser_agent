from playwright.sync_api import sync_playwright
import time


def signup_instagram(email, password, fullname, month, day, year):

    months = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    month_name = months[int(month) - 1]

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.instagram.com/accounts/emailsignup/")

        page.get_by_role("textbox", name="Mobile number or email").wait_for()

        # Fill fields
        page.get_by_role("textbox", name="Mobile number or email").type(email, delay=100)
        page.get_by_role("textbox", name="Password").type(password, delay=100)
        page.get_by_role("textbox", name="Full name").type(fullname, delay=100)

        print("Basic fields filled")

        # -------- Month --------
        page.get_by_role("combobox", name="Month").click()
        page.get_by_text(month_name, exact=True).click()

        # -------- Day --------
        page.get_by_role("combobox", name="Day").click()
        page.get_by_text(day, exact=True).click()

        # -------- Year --------
        page.get_by_role("combobox", name="Year").click()
        page.get_by_text(year, exact=True).click()

        print("Birthday selected")

        # Submit
        page.get_by_role("button", name="Submit").click()
        veriable=input("Enter Verification Code: ")
        page.get_by_role("textbox", name="Code").type(veriable, delay=100)
        page.get_by_role("button", name="Continue").click()

       
        print("Form submitted")

        time.sleep(10)
        browser.close()


# ---- User Inputs ----
email = input("Enter Email: ")
password = input("Enter Password: ")
fullname = input("Enter Full Name: ")
month = input("Enter Month Number (1-12): ")
day = input("Enter Day (1-31): ")
year = input("Enter Year (Example 2000): ")

signup_instagram(email, password, fullname, month, day, year)
