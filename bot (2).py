
import streamlit as st
import os # Import os to access environment variables
from langchain_groq import ChatGroq

st.set_page_config(page_title = "My AI Chat", layout = 'centered')

st.title("The Groq Chatbot")
st.write("A fully integrated, memory enable AI Assistant")

# Retrieve API key from environment variable (set in the Colab launch cell)
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# Initialize LLM globally, so it's ready when the app starts
# Only initialize if the API key is available
llm = None
if GROQ_API_KEY:
    llm = ChatGroq(
        temperature=0.7,
        model_name="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY
    )
else:
    st.error("GROQ_API_KEY not found in environment variables. Please set it in Colab secrets and re-run the setup cell.")

# 1. Side Bar
with st.sidebar:
  st.header("Configuration")
  # Displaying the API key status, no longer asking for input here
  if GROQ_API_KEY:
      st.success("Groq API Key detected in environment variables.")
  else:
      st.warning("Groq API Key is missing. Please check your Colab secrets and environment setup.")

# 2. Memory Vault
if "messages" not in st.session_state:
  st.session_state.messages = []

# 3. Display History
for msg in st.session_state.messages:
  with st.chat_message(msg['role']):
    st.markdown(msg['content'])

# 4. The input box (pinned to the bottom)
if user_query := st.chat_input("Message the AI...."):

  if not llm: # Check if LLM was successfully initialized
    st.error("Cannot process query: LLM not initialized due to missing API key.")

  else:
    with st.chat_message('user'):
      st.markdown(user_query)

    st.session_state.messages.append({"role":"user", "content": user_query})

    with st.spinner("AI is thinking...."):
      # Pass only the current messages for LLM invocation
      response = llm.invoke(st.session_state.messages)
      bot_answer = response.content

    with st.chat_message("assistant"):
      st.markdown(bot_answer)

    st.session_state.messages.append({"role":"assistant", "content": bot_answer})


    from pyngrok import ngrok

# Replace 'YOUR_NGROK_AUTH_TOKEN' with your actual authtoken
ngrok.set_auth_token('3FZgBiwXa0DqKF67meNUTRmh5Hh_6x5rHVJwvKEzPqTfzCb5H')
print("ngrok authtoken set.")



import os
import signal
import time
import subprocess
import sys # Import sys module to get the Python executable path
from pyngrok import ngrok

# Terminate any previous ngrok tunnels
ngrok.kill()

# Find and kill any process running on port 8501
try:
    # Use fuser to find the PID of the process using port 8501 and kill it
    # -k kills the process, -n specifies network, tcp specifies TCP protocol
    os.system('fuser -k -n tcp 8501')
    print("Killed any process previously using port 8501.")
except Exception as e:
    print(f"Could not kill process on port 8501: {e}")

# Start Streamlit app (bot.py) in the background using subprocess.Popen
# Use sys.executable to explicitly run streamlit as a module
print("Starting Streamlit bot.py app...")
streamlit_process = subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'bot.py'])

# Give Streamlit a moment to start up
time.sleep(7) # Increased delay to ensure the bot app starts fully

# Start ngrok tunnel for Streamlit on port 8501
public_url = ngrok.connect(addr='8501', proto='http')
print(f'Streamlit App URL: {public_url}')

# The streamlit_process will now run in the background.




import os
import signal
import time
import subprocess
import sys
from pyngrok import ngrok
from google.colab import userdata

# Terminate any previous ngrok tunnels
ngrok.kill()

# Find and kill any process running on port 8501
try:
    os.system('fuser -k -n tcp 8501')
    print("Killed any process previously using port 8501.")
except Exception as e:
    print(f"Could not kill process on port 8501: {e}")

# Retrieve API key from Colab secrets and set as environment variable
GROQ_API_KEY = userdata.get('groq_api')
os.environ['GROQ_API_KEY'] = GROQ_API_KEY

# Ensure Streamlit is installed in the current environment
# This helps prevent 'No module named streamlit' errors when using subprocess.Popen
print("Ensuring Streamlit is installed...")
get_ipython().system('pip install streamlit -q --force-reinstall')

print("Attempting to start Streamlit bot.py and capture output...")
# Start Streamlit app (bot.py) in the background, capturing stdout and stderr
# We'll use a temporary file for stderr to ensure it's captured even if the process exits quickly

# Create a temporary file for stderr
import tempfile
stderr_file = tempfile.TemporaryFile(mode='w+', encoding='utf-8')

streamlit_process = subprocess.Popen(
    [sys.executable, '-m', 'streamlit', 'run', 'bot.py'],
    stdout=subprocess.PIPE,
    stderr=stderr_file,
    text=True, # Decode stdout/stderr as text
    bufsize=1, # Line-buffered output
    universal_newlines=True # Ensure consistent newline handling
)

# Give Streamlit a moment to start up
time.sleep(7)

# Check if the process is still running
if streamlit_process.poll() is None:
    print("Streamlit process is still running. Retrieving public URL...")
    # Start ngrok tunnel for Streamlit on port 8501
    public_url = ngrok.connect(addr='8501', proto='http')
    print(f'Streamlit App URL: {public_url}')

    print("You can now access the Streamlit app using the URL above.")
    print("To view its logs, please run the next cell (which will be generated below).")

else:
    print(f"Streamlit process terminated with exit code: {streamlit_process.returncode}")
    print("Streamlit process did not stay alive. Checking logs...")

    # Read stdout and stderr
    stdout_output = streamlit_process.stdout.read()
    stderr_file.seek(0) # Rewind to the beginning of the file
    stderr_output = stderr_file.read()

    print("\n--- Streamlit STDOUT ---\n")
    print(stdout_output)
    print("\n--- Streamlit STDERR ---\n")
    print(stderr_output)
    print("\n--- End of Streamlit Logs ---\n")
    print("Please examine the logs above for error messages.")

# Close the temporary file
stderr_file.close()
