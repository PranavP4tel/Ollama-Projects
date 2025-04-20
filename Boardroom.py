import streamlit as st

#Importing ollama from the environment
import sys
sys.path.insert(0, r"dev_env\Lib\site-packages")
import ollama

# Page config
st.set_page_config(page_title="The Boardroom")
st.title("The Boardroom")
st.markdown("This app allows you to pitch your idea or problem to two AI experts (Deepseek-coder and Gemma) and get their expertise in building your solution!")

#  Initialize Chat Histories 
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent1" not in st.session_state:
    st.session_state.agent1 = [
        {"role": "system", "content": "You are DeepCoder, an expert in software engineering, system design, and product development"}
    ]

if "agent2" not in st.session_state:
    st.session_state.agent2 = [
        {"role": "system", "content": "You are GemmaMind,  an expert in software engineering, research, AI and data science"}
    ]

#Printing the entire message history
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# User Input 
user_input = st.chat_input("What's on the your mind?")

if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Add to both agents' chat history
    st.session_state.agent1.append({"role": "user", "content": user_input})
    st.session_state.agent2.append({"role": "user", "content": user_input})

    #  Get response from Agent 1 (deepseek-coder) 
    with st.chat_message("DeepCoder"):
        with st.spinner("DeepCoder is thinking..."):
            try:
                response1 = ollama.chat(
                    model="deepseek-coder",
                    messages=st.session_state.agent1
                )

                reply1 = response1["message"]["content"]
                st.markdown(reply1)
                st.session_state.agent1.append({"role": "assistant", "content": reply1})
                st.session_state.messages.append({"role": "agent1", "content": reply1})
            except Exception as e:
                st.error(f"DeepCoder failed: {e}")

    #  Get response from Agent 2 (Gemma) 
    with st.chat_message("GemmaMind"):
        with st.spinner("GemmaMind is reflecting..."):
            try:
                response2 = ollama.chat(
                    model="gemma3:1b",
                    messages=st.session_state.agent2
                )
                reply2 = response2["message"]["content"]
                st.markdown(reply2)
                st.session_state.agent2.append({"role": "assistant", "content": reply2})
                st.session_state.messages.append({"role": "agent2", "content": reply2})
            except Exception as e:
                st.error(f"GemmaMind failed: {e}")
