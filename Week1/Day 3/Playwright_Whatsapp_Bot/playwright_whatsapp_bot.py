from playwright.sync_api import sync_playwright
import pandas as pd
import os
import time

EXCEL_FILE = "contacts.xlsx"
USER_DATA_DIR = "whatsapp_profile"


# =========================
# Wait for WhatsApp to be fully logged in
# =========================
def wait_for_whatsapp_ready(page):
    # This is the best indicator that login is successful
    page.wait_for_selector("div[aria-label='Chat list']", timeout=120000)


# =========================
# Send message to contact
# =========================
def send_message(page, name, phone, template):

    message = template.replace("{name}", name)

    phone_number = phone

    url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message}"

    print(f"\n→ Sending message to: {name} ({phone})")

    page.goto(url)

    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    message_box = page.locator('div[contenteditable="true"]').last
    message_box.wait_for(timeout=30000)

    message_box.press("Enter")

    page.wait_for_timeout(3000)

    os.makedirs("screenshots", exist_ok=True)

    screenshot_path = f"screenshots/{name}_{int(time.time())}.png"

    page.screenshot(
        path=screenshot_path,
        full_page=True
    )

    print(f"✓ Sent successfully to {name}")
    print(f"✓ Screenshot saved: {screenshot_path}")


# =========================
# Main execution flow
# =========================
with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        USER_DATA_DIR,
        headless=False
    )

    page = context.pages[0] if context.pages else context.new_page()
    page.goto("https://web.whatsapp.com")

    print("\n====================================")
    print(" Checking login session...")
    print("====================================\n")

    try:
        wait_for_whatsapp_ready(page)
        print("✓ Already logged in (session found)")
    except:
        print("⚠ First-time login required (scan QR once)")
        wait_for_whatsapp_ready(page)

    # =========================
    # Read Excel file
    # =========================
    df = pd.read_excel(EXCEL_FILE, header=None)

    print(f"\n✓ Loaded {len(df)} contacts from Excel")

    # =========================
    # Loop through contacts
    # =========================
    for index, row in df.iterrows():

        try:
            name = str(row[0]).strip()
            phone = str(row[1]).strip()

            if len(row) > 2 and pd.notna(row[2]):
                message = str(row[2]).strip()
            else:
                message = "Hello {name}"

            send_message(page, name, phone, message)

            page.wait_for_timeout(2000)

        except Exception as e:
            print(f"✗ Error at row {index + 1}: {e}")

    # =========================
    # Finish execution
    # =========================
    print("\n✅ ALL MESSAGES COMPLETED")

    context.close()