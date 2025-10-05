# CSV Analysis Agent with Google Gemini

This project is a web-based application built with Streamlit that allows users to upload a CSV file and interact with it through a conversational agent powered by Google's Gemini API. The agent can analyze the data, answer questions, and generate visualizations to provide insights.

## Features

-   **Interactive Data Analysis:** Upload your CSV files and ask questions in natural language.
-   **Dynamic Visualizations:** The agent can generate and display charts (e.g., bar charts, line graphs) based on your queries.
-   **Multi-Language Support:** The user interface is available in English, Spanish, and Portuguese.
-   **Selectable AI Models:** Choose from a list of available Google Gemini models to tailor the agent's capabilities to your needs.
-   **Secure API Key Handling:** Your Google Gemini API key is managed securely and is not stored or exposed.

## How to Set Up and Run the Application

Follow these steps to get the application running on your local machine.

### Prerequisites

-   Python 3.8+
-   A Google Gemini API Key. You can get one from [Google AI Studio](https://aistudio.google.com/apikey).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Execute the Streamlit command:**
    ```bash
    streamlit run app.py
    ```

2.  **Open the application in your browser:**
    -   Streamlit will provide a local URL (usually `http://localhost:8501`) that you can open in your web browser.

3.  **Using the App:**
    -   Enter your Google Gemini API key in the sidebar.
    -   Select the Gemini model you wish to use.
    -   Upload your CSV file.
    -   Start asking questions about your data in the chat input box.