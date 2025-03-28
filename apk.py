import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API keys
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="Code Analysis AI Agent",
    page_icon="💻",
    layout="wide"
)

st.title("Code Analysis AI Agent 💻")
st.header("Powered by Gemini 2.0 Flash Exp")

@st.cache_resource
def initialize_agent():
    return Agent(
        name="Code Analysis Agent",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )

# Initialize the agent
code_analysis_agent = initialize_agent()

# Code snippet input
code_snippet = st.text_area(
    "Enter your code snippet (C, C++, Java, or Python)",
    height=200,
    placeholder="Paste your code snippet here",
    help="Enter the code snippet you want to analyze."
)

# User query input
user_query = st.text_area(
    "What insights are you seeking from the code?",
    placeholder="Ask anything about the code snippet. The AI agent will analyze and gather additional context if needed.",
    help="Provide specific questions or insights you want from the code."
)

if st.button("🔍 Analyze Code", key="analyze_code_button"):
    if not code_snippet:
        st.warning("Please enter a code snippet to analyze.")
    elif not user_query:
        st.warning("Please enter a question or insight to analyze the code.")
    else:
        try:
            with st.spinner("Processing code and gathering insights..."):
                # Prompt generation for analysis
                analysis_prompt = (
                    f"""
                    Analyze the following code snippet for content and context:
                    {code_snippet}

                    Respond to the following query using code insights and supplementary web research:
                    {user_query}

                    Provide a detailed, user-friendly, and actionable response.
                    """
                )

                # AI agent processing
                response = code_analysis_agent.run(analysis_prompt)

            # Display the result
            st.subheader("Analysis Result")
            st.markdown(response.content)

        except Exception as error:
            st.error(f"An error occurred during analysis: {error}")
else:
    st.info("Enter a code snippet and a question to begin analysis.")

# Customize text area height
st.markdown(
    """
    <style>
    .stTextArea textarea {
        height: 100px;
    }
    </style>
    """,
    unsafe_allow_html=True
)