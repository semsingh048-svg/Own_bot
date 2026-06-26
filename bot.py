
import streamlit as st
from langchain_groq import ChatGroq

st.set_page_config(page_title = "My AI Chat", layout = 'centered')

st.title("The Groq Chatbot")
st.write("A fully integrated, memory enable AI Assistant")

# 1. Side Bar
with st.sidebar:
  st.header("Configuration")
  user_api_key = st.text_input("Enter your Groq API Key:", type = 'password')
  st.info("Your key is required to weke up the AI brain.")

# 2. Memory Vault
if "messages" not in st.session_state:
  st.session_state.messages = []

# 3. Display History
# Redraw all past messages every time the page returns
for msg in st.session_state.messages:
  with st.chat_message(msg['role']):  # This display human and ai messages differently
    st.markdown(msg['content'])

# 4. The input box (pinned to the bottom)
if user_qrery := st.chat_input("Massage the AI...."):

  if not user_api_key:
    st.error("Please enter API Key in the sidebar first")

  else:
      
    # Display the user message instantly
    with st.chat_message('user'):
      st.markdown(user_query)

      # Save the user massage to the vault
      st.session_state.messages.append({"role":"user", "content": user_query})

      llm = ChatGroq(
          temperature= 0.7,
          model_name = "llama-3.3-70b-verrsatile",
          api_key = user_api_key
      )

      # Call the Actual AI

      with st.spinner("AI is thinking...."):
        response = llm.invoke(st.session_state.messages)
        bot_answer = response.content

      # Display the bot message instantly
      with st.chat_message("assistant"):
        st.markdown(bot_response)

      # Save the user message to the vault
      st.session_state.message.append({"role":"assistant", "content":bot_response})
