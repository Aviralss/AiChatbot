import streamlit as st
from dotenv import load_dotenv
from google import genai
import os


load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY not found in .env")
    st.stop()


client = genai.Client(api_key=api_key)


st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

st.title("🤖 Gemini AI Chatbot")


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("Ask anything...")

if prompt:


    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        answer = response.text

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

    except Exception as e:
        st.error(e)