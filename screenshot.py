
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

# Website address
URL = "http://localhost:8501"

# Folder where screenshots will be saved
OUTPUT_DIR = Path("website_screenshots")
OUTPUT_DIR.mkdir(exist_ok=True)

# Dashboard page names
PAGES = [
    "Overview",
    "Demographics",
    "Gaming behaviour",
    "Preferences",
    "Research analysis",
    "Data explorer"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page(
        viewport={"width": 1440, "height": 1000},
        device_scale_factor=1
    )

    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(3000)

    for index, page_name in enumerate(PAGES, start=1):

        print(f"Capturing {page_name}...")

        # Find the Streamlit navigation item
        navigation_item = page.get_by_text(
            page_name,
            exact=True
        ).first

        navigation_item.click()

        # Wait for dashboard to finish rendering
        page.wait_for_timeout(2500)

        # Save full-page screenshot
        filename = OUTPUT_DIR / f"{index}_{page_name.lower().replace(' ', '_')}.png"

        page.screenshot(
            path=str(filename),
            full_page=True,
            animations="disabled"
        )

        print(f"Saved: {filename}")

    browser.close()

print("\nAll screenshots have been saved!")
