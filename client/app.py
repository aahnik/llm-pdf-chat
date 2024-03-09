import streamlit as st
import requests
import time
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

_unset = "!@unset"
STORAGE_DIR = Path(os.environ.get("FILES_STORAGE_DIR", _unset))
assert STORAGE_DIR != _unset
print(STORAGE_DIR)
os.makedirs(STORAGE_DIR, exist_ok=True)

API_BASE_URL = "http://localhost:8000/"


def init_session_state():
    if "connected" not in st.session_state:
        st.session_state.connected = False

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "offset" not in st.session_state:
        st.session_state.offset = -1

    if st.session_state.connected:
        st.write(f"Connected as {st.session_state.username}")


def create_sidebar():
    with st.sidebar:
        with st.expander("Files"):
            files = st.file_uploader(
                "Upload PDFs", accept_multiple_files=True, type=["pdf"]
            )

            save_files = st.button("Save", key="save_files")
            if save_files:
                if files:
                    for file in files:
                        save_path = STORAGE_DIR / file.name
                        with open(save_path, mode="wb") as wf:
                            wf.write(file.getvalue())
            st.divider()
            st.markdown("**Saved Files**")
            for file in os.listdir(STORAGE_DIR):
                print(file)
                st.write(file)
        with st.expander("Configure LLM"):
            temperature = st.slider(
                "Temperature", min_value=0.0, max_value=1.0, step=0.1
            )
            model = st.selectbox("Model", options=["claude-2", "claude-3"])
            save_llm = st.button("Save", key="save_llm")
            if save_llm:
                con = API_BASE_URL + "set_llm/"
                response = requests.post(
                    con, params={"temperature": temperature, "model": model}
                )
                st.toast(response.json())


def run_chat_loop():
    con = API_BASE_URL + "messages/"
    response = requests.get(con + str(st.session_state.offset))
    msgs_json = response.json()

    for msg in msgs_json:
        st.session_state.messages.append(
            {"username": msg["username"], "message": msg["message"]}
        )
    if len(msgs_json) >= 1:
        st.session_state.offset = msgs_json[-1]["seqno"]

    for message in st.session_state.messages:
        with st.chat_message(message["username"]):
            st.markdown(message["message"])

    if prompt := st.chat_input("Start chatting"):
        requests.post(con, json={"username": "user", "message": prompt})
        st.rerun()
    else:
        time.sleep(0.5)
        st.rerun()


def main():
    st.title("Streamlit + FastAPI + Langchain Chat!")
    init_session_state()
    create_sidebar()

    connect = st.checkbox("connect with backend")

    if connect:
        run_chat_loop()


if __name__ == "__main__":
    main()
