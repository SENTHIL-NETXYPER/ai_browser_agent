import re
from playwright.sync_api import sync_playwright
from playwright_stealth.stealth import Stealth


def google_search(query: str):
    print(f"🔎 Searching Google for: {query}")

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        Stealth().apply_stealth_sync(page)

        try:
            page.goto("https://www.google.com", wait_until="domcontentloaded")

            # Handle Google consent popup (if it appears)
            try:
                consent_button = page.get_by_role(
                    "button",
                    name=re.compile(r"(I agree|Accept all|Accept|Agree|Alles akzeptieren)", re.I)
                )
                if consent_button.first.is_visible():
                    consent_button.first.click(timeout=10000)
            except Exception:
                pass

            # Wait for search box
            page.wait_for_selector("textarea[name='q'], input[name='q']", timeout=8000)

            # Prefer textarea (modern Google UI)
            search_box = page.locator("textarea[name='q']").first

            if not search_box.is_visible():
                search_box = page.locator("input[name='q']").first

            # Type query and search
            search_box.fill(query)
            page.wait_for_timeout(5000)
            search_box.press("Enter")

            print("✅ Search submitted")

            # Wait for results
            page.wait_for_selector("h3", timeout=10000)

            # Extract top results
            results = page.locator("h3").all_text_contents()

            print("\n📊 Top Results:")
            for r in results[:5]:
                print("-", r)

            page.wait_for_timeout(5000)

        finally:
            browser.close()


def open_website(url: str):
    print(f"🌐 Opening website: {url}")

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)

        finally:
            browser.close()