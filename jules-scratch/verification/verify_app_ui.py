from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Navigate to the Streamlit app
            page.goto("http://localhost:8501", timeout=60000) # Increased timeout

            # Wait for the main title to be visible
            expect(page.locator("h1").first).to_be_visible(timeout=30000)

            # Take a screenshot
            page.screenshot(path="jules-scratch/verification/verification.png")

            print("Screenshot taken successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            # Try to capture the page content on error for debugging
            page.screenshot(path="jules-scratch/verification/error.png")
            print("Error screenshot taken.")

        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()