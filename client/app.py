import streamlit as st
import requests
import time


def handle_username_change():
    st.toast(f"Username set to {st.session_state.username}")


st.title("Streamlit + FastAPI + Langchain Chat!")

if "username" not in st.session_state:
    st.session_state.username = ""

with st.sidebar:
    uname = st.text_input(
        "Enter your username:",
        key="username_input_box",
        on_change=handle_username_change,
        value=st.session_state.username,
    )
    save = st.button("Save")
    if save:
        st.session_state.username = uname


if "connected" not in st.session_state:
    st.session_state.connected = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "offset" not in st.session_state:
    st.session_state.offset = -1

if st.session_state.connected:
    st.write(f"Connected as {st.session_state.username}")


print("session state username: " + st.session_state.username)


def main():

    connect = st.checkbox("connect with backend")

    if connect:
        assert st.session_state.username != ""
        con = "http://localhost:8000/messages/"
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
            requests.post(
                con, json={"username": st.session_state.username, "message": prompt}
            )
            st.rerun()
        else:
            time.sleep(0.5)
            st.rerun()


if __name__ == "__main__":
    main()
