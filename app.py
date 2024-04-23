from openai import OpenAI
import streamlit as st
import configparser

# Read the API key from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
openai_api_key = config['openai']['api_key']

# Initialize OpenAI client
openai = OpenAI(api_key=openai_api_key)

# Define function to interact with OpenAI
def get_code_review(prompt: str) -> str:
    # Define the conversation prompt
    conversation_prompt = [
        "You are a helpful AI Assistant.",
        "Given a Python code snippet, you will review it for potential bugs and suggest fixes.",
        f"Python Code:\n{prompt}\n\nAI Review:"
    ]

    # Generate completion
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful AI Assistant. Given a Python code snippet, you will review it for potential bugs and suggest fixes."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract corrected code from completion
    corrected_code = response.choices[0].text.strip()

    return corrected_code

# Streamlit UI
st.markdown("<h1 style='color:green;'>GenAI App - AI Code Reviewer</h1>", unsafe_allow_html=True)
st.subheader("Python Code Reviewer and Bug Fixer")

# User input for code snippet
prompt = st.text_area("Enter your Python code", height=200)

# If button is clicked, generate code review
if st.button("Get Review"):
    st.markdown("<h2 style='color:black;'>Review:</h2>", unsafe_allow_html=True)

    # Original code display
    st.markdown("<h3 style='color:green;font-size:20px;'>Original Code:</h3>", unsafe_allow_html=True)
    st.code(prompt, language='python')

    # Generate and display corrected code
    corrected_code = get_code_review(prompt)
    st.markdown("<h3 style='color:green;font-size:20px;'>Corrected Code and Review:</h3>", unsafe_allow_html=True)
    st.code(corrected_code, language='python')
