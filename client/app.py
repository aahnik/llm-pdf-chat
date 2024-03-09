import streamlit as st
import requests
import time
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

_unset = "!@unset"
STORAGE_DIR = Path(os.environ["FILES_STORAGE_DIR"], _unset)
assert STORAGE_DIR != _unset

os.makedirs(STORAGE_DIR, exist_ok=True)

BACKEND_API_CON = "http://localhost:8000/messages/"


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

        files = st.file_uploader(
            "Upload PDFs", accept_multiple_files=True, type=["pdf"]
        )

        save = st.button("Save")
        if save:
            if files:
                for file in files:
                    save_path = STORAGE_DIR / file.name
                    with open(save_path, mode="wb") as wf:
                        wf.write(file.getvalue())


def run_chat_loop():
    con = BACKEND_API_CON
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
