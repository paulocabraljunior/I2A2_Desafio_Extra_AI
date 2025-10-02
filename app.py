import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
import os

st.set_page_config(layout="wide", page_title="CSV Analysis Agent")

# Function to load language strings from a JSON file
def load_language(language):
    with open(f'locales/{language}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Set default language
if 'language' not in st.session_state:
    st.session_state.language = 'pt'

# Load the selected language
lang = load_language(st.session_state.language)

# --- UI Setup ---
# Sidebar for controls
st.sidebar.title(lang['settings'])

# Language selection with flags
st.sidebar.header(lang['language_selection'])
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    if st.button('🇧🇷'):
        st.session_state.language = 'pt'
        st.experimental_rerun()
with col2:
    if st.button('🇬🇧'):
        st.session_state.language = 'en'
        st.experimental_rerun()
with col3:
    if st.button('🇪🇸'):
        st.session_state.language = 'es'
        st.experimental_rerun()

# API Key Input
api_key = st.sidebar.text_input(lang['api_key_label'], type='password')

# Model selection
model_options = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-2.5-pro']
if 'model' not in st.session_state:
    st.session_state.model = model_options[0]

st.session_state.model = st.sidebar.selectbox(
    lang['model_selection_label'],
    model_options,
    index=model_options.index(st.session_state.model)
)

# File Uploader
uploaded_file = st.sidebar.file_uploader(lang['file_uploader_label'], type=['csv'])


# Main panel
st.title(lang['title'])
st.markdown(f"<p style='text-align: justify;'>{lang['description']}</p>", unsafe_allow_html=True)

if api_key:
    genai.configure(api_key=api_key)

if 'history' not in st.session_state:
    st.session_state.history = []

if uploaded_file is not None:
    # Check if a new file has been uploaded
    if 'current_file' not in st.session_state or st.session_state.current_file != uploaded_file.name:
        st.session_state.current_file = uploaded_file.name
        try:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.session_state.history = [] # Reset history for new file
            st.success(lang['file_upload_success'])
        except Exception as e:
            st.error(f"{lang['error_reading_file']}: {e}")
            # Reset session state if file reading fails
            for key in ['current_file', 'df', 'history']:
                if key in st.session_state:
                    del st.session_state[key]

    if 'df' in st.session_state:
        df = st.session_state.df
        # Display chat history
        for entry in st.session_state.history:
            with st.chat_message(entry['role']):
                st.markdown(entry['content'])

        # User input
        prompt = st.chat_input(lang['chat_input_placeholder'])

        if prompt:
            st.session_state.history.append({'role': 'user', 'content': prompt})
            with st.chat_message('user'):
                st.markdown(prompt)

            with st.chat_message('assistant'):
                with st.spinner(lang['thinking']):
                    try:
                        model = genai.GenerativeModel(st.session_state.model)
                        # Build conversation history for the model
                        model_history = []
                        for entry in st.session_state.history:
                            # Simple conversion, might need adjustment based on actual roles
                            role = 'user' if entry['role'] == 'user' else 'model'
                            model_history.append({'role': role, 'parts': [entry['content']]})

                        # Let's make sure the last message is from the user
                        if model_history[-1]['role'] != 'user':
                             # This case should ideally not happen if we follow the flow
                             st.warning("Warning: Last message in history is not from the user.")

                        # Start a chat session with the model
                        chat = model.start_chat(history=model_history)

                        # Constructing a more detailed prompt for the model
                        full_prompt = f"""
                        {lang['agent_prompt']}

                        User query: "{prompt}"

                        Dataset columns: {list(df.columns)}
                        Dataset head:
                        {df.head().to_string()}
                        """

                        response = chat.send_message(full_prompt)

                        # Check if the response contains code to be executed
                        if "```python" in response.text:
                            code = response.text.split("```python")[1].split("```")[0]

                            # Prepare the execution environment
                            local_vars = {'df': df, 'st': st, 'pd': pd, 'fig': None, 'plt': None}

                            # Import matplotlib dynamically
                            exec("import matplotlib.pyplot as plt", local_vars)

                            # Execute the code
                            exec(code, {}, local_vars)

                            # The executed code is expected to handle the output
                            # Check if a plot was generated
                            if local_vars.get('fig'):
                                st.pyplot(local_vars['fig'])

                            # Add the full response to history for context
                            st.session_state.history.append({'role': 'assistant', 'content': response.text})
                            # Also display the textual part of the response
                            st.markdown(response.text)

                        else:
                             st.markdown(response.text)
                             st.session_state.history.append({'role': 'assistant', 'content': response.text})

                    except Exception as e:
                        error_message = f"{lang['error_executing_code']}: {e}"
                        st.error(error_message)
                        st.session_state.history.append({'role': 'assistant', 'content': error_message})

else:
    st.info(lang['upload_file_to_start'])