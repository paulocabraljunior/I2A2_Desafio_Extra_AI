from playwright.sync_api import sync_playwright, expect
import os

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Go to the Streamlit app
            page.goto("http://localhost:8501", timeout=60000)

            # Wait for the sidebar to be visible
            sidebar = page.locator("section[data-testid='stSidebar']")
            expect(sidebar).to_be_visible(timeout=30000)

            # Upload the CSV file
            file_path = os.path.abspath("jules-scratch/verification/sample_data.csv")
            page.set_input_files("input[type='file']", file_path)

            # Wait for the file to be uploaded and processed
            expect(page.get_by_text("Arquivo carregado com sucesso!")).to_be_visible(timeout=20000)

            # Enter a prompt that should trigger the get_data_head function
            page.get_by_placeholder("Faça uma pergunta sobre o arquivo...").fill("mostre as primeiras linhas dos dados")
            page.keyboard.press("Enter")

            # Wait for the assistant's response and check for the function output
            # We check for the content of the text_area that displays the function output
            output_area = page.locator("textarea[aria-label='Function Output']")
            expect(output_area).to_be_visible(timeout=30000)
            expect(output_area).to_contain_text("alpha")
            expect(output_area).to_contain_text("beta")
            expect(output_area).to_contain_text("gamma")

            # Take a screenshot for visual confirmation
            page.screenshot(path="jules-scratch/verification/verification.png")

            print("Verification successful, screenshot saved.")

        except Exception as e:
            print(f"An error occurred during verification: {e}")
            page.screenshot(path="jules-scratch/verification/error.png")

        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()