import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.chat import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os  # or any model you're using

API_KEY = os.environ["GOOGLE_API_KEY"]
model = ChatGoogleGenerativeAI(api_key=API_KEY, model="gemini-2.5-pro")

# Prompt templates
bug_identification = PromptTemplate(template="""
You are an experienced Python developer with deep expertise in identifying bugs in code.
Given the following code snippet, identify any bugs or errors present.

Your response must be clearly structured as follows:
BUG IDENTIFICATION
<Your explanation here>

Code:
{question}
""",
                                    input_variables=["question"])

error_expalin = PromptTemplate(template="""
You are a skilled Python instructor known for simplifying complex errors.
Explain the bug mentioned below in a way that's easy to understand for learners.

Structure your response as follows:
ERROR EXPLANATION
<Your explanation here>

Bug:
{bug}
""",
                               input_variables=["bug"])

fix_error = PromptTemplate(template="""
You are a Python expert who specializes in debugging and fixing code issues.
Provide a clear and correct solution to fix the error explained below.

Structure your response as follows:
ERROR FIXING
<Your fix here>

Explanation:
{error}
""",
                           input_variables=["error"])

# Streamlit UI
st.set_page_config(page_title="Python Bug Fixer", page_icon="🐞")
st.title("🐍 Python Bug Identifier and Fixer")

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Input field
user_input = st.text_area(
    "Paste your buggy Python code and press Ctrl+Enter or click 'Submit'",
    height=200)

if st.button("Submit") and user_input.strip():
    with st.spinner("Analyzing..."):
        try:
            # Step 1: Bug Identification
            bug_chain = bug_identification | model
            bug_output = bug_chain.invoke({"question": user_input})
            bug_text = bug_output.content

            # Step 2: Error Explanation
            explain_chain = error_expalin | model
            error_output = explain_chain.invoke({"bug": bug_text})
            error_text = error_output.content

            # Step 3: Fixing the Error
            fix_chain = fix_error | model
            fix_output = fix_chain.invoke({"error": error_text})
            fix_text = fix_output.content

            # Save in chat history
            st.session_state.chat.append({
                "user": user_input,
                "bug": bug_text,
                "explanation": error_text,
                "fix": fix_text
            })

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Display chat messages
for chat in reversed(st.session_state.chat):
    with st.chat_message("user"):
        st.code(chat["user"], language="python")
    with st.chat_message("assistant"):
        st.markdown(f"**{chat['bug']}**")
        st.markdown(f"**{chat['explanation']}**")
        st.markdown(f"**{chat['fix']}**")
