import streamlit as st
import pandas as pd
import google.generativeai as genai
import json
import os
import numpy as np
from google.generativeai.types import FunctionDeclaration, Tool

# --- Page and App Setup ---
st.set_page_config(layout="wide", page_title="CSV Analysis Agent")

# --- Localization ---
def load_language(language):
    """Loads the language JSON file."""
    with open(f'locales/{language}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

if 'language' not in st.session_state:
    st.session_state.language = 'pt'
lang = load_language(st.session_state.language)

# --- UI Components ---
st.sidebar.title(lang['settings'])
st.sidebar.header(lang['language_selection'])
col1, col2, col3 = st.sidebar.columns(3)

if col1.button('🇧🇷'):
    st.session_state.language = 'pt'
    st.rerun()
if col2.button('🇬🇧'):
    st.session_state.language = 'en'
    st.rerun()
if col3.button('🇪🇸'):
    st.session_state.language = 'es'
    st.rerun()

api_key = st.sidebar.text_input(lang['api_key_label'], type='password')

model_options = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro']
if 'model' not in st.session_state:
    st.session_state.model = model_options[0]

st.session_state.model = st.sidebar.selectbox(
    lang['model_selection_label'],
    model_options,
    index=model_options.index(st.session_state.model)
)

uploaded_file = st.sidebar.file_uploader(lang['file_uploader_label'], type=['csv'])

st.title(lang['title'])
st.markdown(f"<p style='text-align: justify;'>{lang['description']}</p>", unsafe_allow_html=True)

# --- Main App Logic ---
if api_key:
    genai.configure(api_key=api_key)

if 'history' not in st.session_state:
    st.session_state.history = []

if uploaded_file is not None:
    if 'current_file' not in st.session_state or st.session_state.current_file != uploaded_file.name:
        st.session_state.current_file = uploaded_file.name
        try:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.session_state.history = []
            st.success(lang['file_upload_success'])
        except Exception as e:
            st.error(f"{lang['error_reading_file']}: {e}")
            if 'df' in st.session_state: del st.session_state.df

    if 'df' in st.session_state:
        df = st.session_state.df

        for role, content in st.session_state.history:
            with st.chat_message(role):
                st.markdown(content)

        if prompt := st.chat_input(lang['chat_input_placeholder']):
            st.session_state.history.append(("user", prompt))
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner(lang['thinking']):
                    try:
                        # --- Final, Comprehensive EDA Tool Definitions ---
                        def get_data_summary():
                            """Provides a statistical summary of the numerical columns."""
                            return df.describe().to_string()

                        def plot_histogram(column_name: str):
                            """Generates a histogram for a given column."""
                            import matplotlib.pyplot as plt
                            if column_name not in df.columns: return f"Error: Column '{column_name}' not found."
                            fig, ax = plt.subplots()
                            df[column_name].hist(ax=ax)
                            ax.set_title(f'Histogram of {column_name}')
                            st.pyplot(fig)
                            return f"Histogram for {column_name} displayed."

                        def plot_correlation_matrix():
                            """Calculates and visualizes the correlation matrix."""
                            import matplotlib.pyplot as plt
                            import seaborn as sns
                            numerical_df = df.select_dtypes(include=np.number)
                            if numerical_df.shape[1] < 2: return "Not enough numerical columns for a correlation matrix."
                            corr = numerical_df.corr()
                            fig, ax = plt.subplots()
                            sns.heatmap(corr, ax=ax, annot=True, cmap='coolwarm')
                            st.pyplot(fig)
                            return "Correlation matrix displayed."

                        def detect_outliers(column_name: str):
                            """Detects outliers in a numerical column using the IQR method."""
                            if column_name not in df.columns or df[column_name].dtype not in ['int64', 'float64']:
                                return f"Error: Column '{column_name}' is not a valid numerical column."
                            Q1 = df[column_name].quantile(0.25)
                            Q3 = df[column_name].quantile(0.75)
                            IQR = Q3 - Q1
                            outliers = df[(df[column_name] < (Q1 - 1.5 * IQR)) | (df[column_name] > (Q3 + 1.5 * IQR))]
                            if outliers.empty:
                                return f"No outliers detected in '{column_name}'."
                            return f"Outliers detected in '{column_name}':\n{outliers.to_string()}"

                        tool_functions = {
                            'get_data_summary': get_data_summary,
                            'plot_histogram': plot_histogram,
                            'plot_correlation_matrix': plot_correlation_matrix,
                            'detect_outliers': detect_outliers,
                        }

                        # --- Final, Correct Tool Declaration for the API ---
                        tools_declaration = Tool(
                            function_declarations=[
                                FunctionDeclaration(name='get_data_summary', description=get_data_summary.__doc__),
                                FunctionDeclaration(name='plot_histogram', description=plot_histogram.__doc__, parameters={'type': 'object', 'properties': {'column_name': {'type': 'string'}}}),
                                FunctionDeclaration(name='plot_correlation_matrix', description=plot_correlation_matrix.__doc__),
                                FunctionDeclaration(name='detect_outliers', description=detect_outliers.__doc__, parameters={'type': 'object', 'properties': {'column_name': {'type': 'string'}}}),
                            ]
                        )

                        model = genai.GenerativeModel(model_name=st.session_state.model, tools=[tools_declaration])

                        api_history = [{'role': 'user' if role == 'user' else 'model', 'parts': [content]} for role, content in st.session_state.history[:-1]]

                        chat = model.start_chat(history=api_history)

                        full_prompt = f"{lang['agent_prompt']}\nUser query: \"{prompt}\"\n\nData Columns: {list(df.columns)}"
                        response = chat.send_message(full_prompt)

                        while response.candidates[0].content.parts[0].function_call:
                            function_call = response.candidates[0].content.parts[0].function_call
                            function_name = function_call.name
                            if function_name not in tool_functions:
                                st.error(f"Function '{function_name}' not found.")
                                break
                            function_to_call = tool_functions[function_name]
                            args_dict = dict(function_call.args)
                            function_response = function_to_call(**args_dict)
                            response = chat.send_message(
                                [genai.protos.Part(function_response={'name': function_name, 'response': {'result': function_response}})]
                            )

                        final_response = response.text
                        st.markdown(final_response)
                        st.session_state.history.append(("assistant", final_response))

                    except Exception as e:
                        error_message = f"{lang['error_executing_code']}: {e}"
                        st.error(error_message)
                        st.session_state.history.append(("assistant", error_message))
else:
    st.info(lang['upload_file_to_start'])