import aiohttp


async def consumer(ws_con: str, st):

    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.ws_connect(ws_con) as websocket:
            st.subheader(f"Connected to: {ws_con}")

            # for message in st.session_state.messages:
            #     with st.chat_message(message["role"]):
            #         st.markdown(message["content"])

            if prompt := st.chat_input("Start chatting"):
                print(prompt)
                # st.session_state.messages.append(
                #     {"role": st.session_state.username, "content": prompt}
                # )
                await websocket.send_str(prompt)
                print("sent to websocket")
            async for message in websocket:
                data = message.json()

                st.write(data)
