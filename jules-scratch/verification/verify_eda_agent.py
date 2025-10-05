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

            # Enter a prompt that should trigger the plot_histogram function
            page.get_by_placeholder("Faça uma pergunta sobre o arquivo...").fill("gere um histograma para a coluna 'score'")
            page.keyboard.press("Enter")

            # Wait for the final assistant's response, which should mention the histogram
            assistant_response = page.locator("div[data-testid='stChatMessage']").last
            expect(assistant_response).to_contain_text("histograma", timeout=60000)

            # Check if a plot was generated
            expect(page.locator("img.st-emotion-cache-1632s4l.e1f1d6gn0")).to_be_visible()

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