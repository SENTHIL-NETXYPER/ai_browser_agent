from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
from playwright.sync_api import expect
import random

def human_delay(min_ms=600, max_ms=1200):
    time.sleep(random.randint(min_ms, max_ms) / 1000)

def type_like_human(field, text):
    """Click field, clear it, and type character by character with delays."""
    field.wait_for(state="visible", timeout=30000)
    field.scroll_into_view_if_needed()
    field.click()
    # Always clear to prevent previous data from bleeding in
    field.fill("")
    time.sleep(0.3)
    for ch in text:
        field.type(ch, delay=random.randint(70, 130))


def dismiss_cookies(page):
    """Dismiss common Facebook cookie consent buttons."""
    for label in [
        "Allow all cookies", "Accept all", "Allow essential and optional cookies", "OK"
    ]:
        btn = page.get_by_role("button", name=label)
        if btn.count() > 0 and btn.first.is_visible():
            btn.first.click()
            print(f"[INFO] 🍪 Cookie popup dismissed: '{label}'")
            page.wait_for_timeout(1500)
            return
    print("[INFO] No cookie popup detected")

def signup_facebook():
    print("\n--- Facebook Signup Information ---")
    firstname = input("Enter First Name: ").strip()
    lastname  = input("Enter Surname: ").strip()
    email     = input("Enter Email/Mobile: ").strip()
    password  = input("Enter Password: ").strip()
    
    month_num = input("Enter Birth Month (1-12): ").strip()
    months = {
        "1": "January", "2": "February", "3": "March", "4": "April",
        "5": "May", "6": "June", "7": "July", "8": "August",
        "9": "September", "10": "October", "11": "November", "12": "December"
    }
    month = months.get(month_num, "January")
    
    day    = input("Enter Birth Day (e.g. 1): ").strip()
    year   = input("Enter Birth Year (e.g. 1995): ").strip()
    gender = input("Enter Gender (male/female): ").strip().lower()

    print(f"\n[INFO] Starting process for: {firstname} {lastname} ({gender})")


    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )

        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        )
        context.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        )

        page = context.new_page()

        try:
            print("[INFO] Navigating to Facebook registration (English forced)...")
            reg_url = "https://www.facebook.com/reg/?locale=en_US&entry_point=aymh&next=https%3A%2F%2Fwww.facebook.com%2F"
            page.goto(reg_url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(4000)


            # 1. Handle Cookie Popup
            dismiss_cookies(page)
            
            # 2. Click "Create new account" to open the signup modal
            print("[INFO] Looking for 'Create new account' button...")
            create_btn = page.get_by_role("link", name="Create new account")
            if create_btn.count() == 0:
                create_btn = page.locator("a[data-testid='open-registration-form-button']")
            if create_btn.count() > 0 and create_btn.first.is_visible():
                print("[INFO] Clicking 'Create new account' link to open the form...")
                create_btn.first.click()
                page.wait_for_timeout(3000)
            else:
                print("[WARN] 'Create new account' button not found. Assuming we are already on the form.")

            print("[INFO] ---------------------------------------------")

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

            type_like_human(last_box, lastname)

            print("[INFO] Surname entered")
            human_delay()

            # --- EMAIL / MOBILE ---
            print("[INFO] Entering Email/Mobile...")
            # '6ad' is the consistent pattern for the Email field
            em_selector = "input[id*='6ad']:visible, input[name='reg_email__']:visible"
            em_field = page.locator(em_selector).first
            
            if em_field.count() > 0:
                type_like_human(em_field, email)
                print(f"[INFO] ✅ Email: {email}")
            else:
                # Fallback to broad label search
                em_field = page.get_by_label("Mobile number or email address", exact=False).first
                if em_field.count() > 0:
                    type_like_human(em_field, email)
                    print(f"[INFO] ✅ Email (Label fallback): {email}")
                else:
                    print("[WARN] Email/Mobile field not found.")
            human_delay()
            
            # Confirm email optionally
            print("[INFO] Checking for email confirmation field...")
            em_confirm = page.locator("input[name='reg_email_confirmation__']:visible")
            if em_confirm.count() > 0:
                type_like_human(em_confirm.first, email)
                print("[INFO] ✅ Email confirmed")
                human_delay()

            # --- PASSWORD ---
            print("[INFO] Entering Password...")
            # 'cla' is the pattern for Password
            pw_selector = "input[id*='cla']:visible, input[name='reg_passwd__']:visible"
            pw_field = page.locator(pw_selector).first

            if pw_field.count() > 0:
                type_like_human(pw_field, password)
                print("[INFO] ✅ Password entered")
            else:
                pw_field = page.get_by_label("New password").first
                if pw_field.count() > 0:
                    type_like_human(pw_field, password)
                    print("[INFO] ✅ Password entered (Label fallback)")
                else:
                    print("[WARN] Password field not found.")
            human_delay()


            # --- BIRTHDAY ---
            print("[INFO] Selecting Birthday...")
            
            # Month
            m_sel = page.locator("select[name='birthday_month']")
            if m_sel.count() > 0:
                m_sel.select_option(label=month[:3]) # e.g. "Jan"
            else:
                cb = page.get_by_role("combobox", name="month")
                if cb.count() > 0:
                    cb.first.click(); page.wait_for_timeout(500)
                    page.get_by_role("option", name=month).click()
            print(f"[INFO] ✅ Month: {month}")
            human_delay(300, 600)

            # Day
            d_sel = page.locator("select[name='birthday_day']")
            if d_sel.count() > 0:
                d_sel.select_option(label=day)
            else:
                cb = page.get_by_role("combobox", name="day")
                if cb.count() > 0:
                    cb.first.click(); page.wait_for_timeout(500)
                    page.get_by_role("option", name=day, exact=True).click()
            print(f"[INFO] ✅ Day: {day}")
            human_delay(300, 600)

            # Year
            y_sel = page.locator("select[name='birthday_year']")
            if y_sel.count() > 0:
                y_sel.select_option(label=year)
            else:
                cb = page.get_by_role("combobox", name="year")
                if cb.count() > 0:
                    cb.first.click(); page.wait_for_timeout(500)
                    page.get_by_role("option", name=year, exact=True).click()
            print(f"[INFO] ✅ Year: {year}")
            human_delay(400, 800)

            # --- GENDER ---
            print(f"[INFO] Selecting Gender: {gender}...")
            # 1 = Female, 2 = Male
            g_val = "2" if gender == "male" else "1"
            g_label = "Male" if gender == "male" else "Female"

            # Try native radio buttons first
            radio = page.locator(f"input[type='radio'][value='{g_val}']")
            if radio.count() > 0:
                radio.check()
                print(f"[INFO] ✅ Gender selected ({g_label})")
            else:
                # Target the custom combobox often used in the modal
                print("[INFO] Looking for Gender combobox...")
                cb = page.locator("div[role='combobox']:has-text('Select your gender')")
                if cb.count() ==0: cb = page.locator("div[role='combobox']:has-text('Gender')")
                if cb.count() == 0: cb = page.get_by_text("Select your gender", exact=False)
                    
                if cb.count() > 0:
                    try:
                        cb.first.click(timeout=8000)
                        page.wait_for_timeout(1500)
                        
                        g_opt = page.locator(f"div[role='option']:has-text('{g_label}')")
                        if g_opt.count() == 0:
                            g_opt = page.get_by_role("option", name=g_label, exact=True)
                        if g_opt.count() == 0:
                            g_opt = page.get_by_text(g_label, exact=True)
                            
                        if g_opt.count() > 0:
                            g_opt.first.click(timeout=5000)
                            print(f"[INFO] ✅ Gender selected ({g_label} Dropdown)")
                        else:
                            print(f"[WARN] '{g_label}' option not found in dropdown.")
                    except PlaywrightTimeoutError:
                        print("[WARN] Failed to open Gender dropdown.")

                else:
                    print("[WARN] Could not find any Gender dropdown or radio buttons.")
                    
            # --- SUBMIT ---
            print("[INFO] Clicking Sign Up...")
            sub = page.locator("button[name='websubmit']")
            if sub.count() == 0:
                sub = page.get_by_role("button", name="Sign Up")
            if sub.count() == 0:
                sub = page.get_by_role("button", name="Submit")
                
            if sub.count() > 0:
                sub.first.click()
                print("[INFO] 🚀 Submitted form! Waiting for response...")
            else:
                print("[WARN] Submit button not found")

            human_delay(5000, 7000)

            # -------- OTP --------
            try:
                code = input("Enter Facebook verification code (or press Enter to skip): ")
                if code:
                    print("[INFO] Waiting for OTP field...")
                    otp_box = page.locator("input[name='code']")
                    if otp_box.count() == 0:
                        otp_box = page.get_by_role("textbox").first
                    otp_box.wait_for(state="visible", timeout=60000)
                    type_like_human(otp_box.first, code)
                    human_delay(600, 1200)

                    page.get_by_role("button", name="Continue").click()
                    print("[INFO] Verification submitted")
                    human_delay(5000, 7000)
                    print("[INFO] ✅ Signup complete!")
            except Exception as e:
                print(f"[WARN] Verification skipped or error: {e}")

            print("[INFO] Holding browser open for 15s to view result...")
            page.wait_for_timeout(15000)

        except PlaywrightTimeoutError as e:
            print(f"\n[ERROR] ⏱ Timed out: {e}")
            input("Press ENTER to close browser...")

        except Exception as e:
            print(f"\n[ERROR] ❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            input("Press ENTER to close browser...")

        finally:
            context.close()
            browser.close()
            print("[INFO] Browser closed.")

if __name__ == "__main__":
    signup_facebook()