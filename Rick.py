import streamlit as st

import sys
sys.path.insert(0, r"dev_env\Lib\site-packages")
import ollama

#Page config
st.set_page_config(page_title="Rick")
st.title("Rick! Your personal coding assistant")
st.markdown("Ask me anything for your interview preparation")

#Storing the conversation in the session
if "messages" not in st.session_state:
    context = "You are Rick, the interview preparation assistant. Respond to the user requests in single line responses, unless explicitly stated otherwise. If asked for a code example, provide a sample output with the program as well."
    message = [{'role':'system','content':context}]
    st.session_state.messages = message

#Printing the entire message history
for message in st.session_state.messages[1:]:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

#Taking user input
prompt = st.chat_input("What's up?")

#If a prompt is given
if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)

    st.session_state.messages.append({'role':'user','content':prompt})

    #Giving output
    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            try:
                response = ollama.chat(
                    model = "deepseek-coder",
                    messages = st.session_state.messages
                )
                st.markdown(response['message']['content'])

                st.session_state.messages.append({"role":"assistant","content":response['message']['content']})
            except Exception as e:
                st.markdown(f"Error: {e}")