import streamlit as st
import websocket


def on_open(ws):
    with st.chat_message("system"):
        st.markdown("Connected!")


def on_message(ws, message):
    print(message)
    with st.chat_message("someuser"):
        st.markdown(message)


def on_error(ws, error):
    with st.chat_message("system"):
        st.markdown(f"Error: {error}")
    st.session_state.connected = False


def on_close(ws, close_status_code, close_msg):
    with st.chat_message("system"):
        st.markdown(f"Closed connection! {close_status_code} {close_msg}")
    st.session_state.connected = False


@st.cache_resource
def get_ws(username):
    print("trying first connection")
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        f"ws://localhost:8000/ws/{username}",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    return ws


def handle_username_change():
    st.toast(f"Username set to {st.session_state.username}")


st.title("Streamlit + FastAPI WebSocket Chat!")


if "username" not in st.session_state:
    st.session_state.username = ""

if "connected" not in st.session_state:
    st.session_state.connected = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.connected:
    st.write(f"Connected as {st.session_state.username}")

if not st.session_state.connected:
    with st.sidebar:
        uname = st.text_input(
            "Enter your username:",
            key="username_input_box",
            on_change=handle_username_change,
        )
        hit_connect = st.button("Connect")
        if hit_connect:

            st.session_state.username = uname
            st.session_state.connected = True
            ws = get_ws(st.session_state.username)
            try:
                ws.run_forever()
            except Exception as err:
                st.write(err)
                ws.close()
            finally:
                st.rerun()


print("session state username: " + st.session_state.username)

if st.session_state.connected:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Start chatting"):
        st.session_state.messages.append(
            {"role": st.session_state.username, "content": prompt}
        )
        ws = get_ws(st.session_state.username)
        ws.send(prompt)

        # with st.chat_message("user"):
        #     st.markdown(prompt)

    print(st.session_state.connected)
    print(st.session_state.username)
