import streamlit as st
import requests

# Rasa API URL (replace with your Rasa server URL)
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

# Function to send message to Rasa and get response
def get_bot_response(user_message):
    response = requests.post(RASA_URL, json={"sender": "user", "message": user_message})
    if response.status_code == 200:
        return response.json()
    else:
        return [{"text": "Sorry, I'm having trouble. Please try again later."}]

# Streamlit UI Setup
st.set_page_config(page_title="Educational Chatbot", page_icon=":robot:", layout="wide")

# Title of the app
st.title("Educational Chatbot")

# Sidebar for additional information or settings (optional)
st.sidebar.title("Chatbot Settings")
st.sidebar.markdown("""
- This is an educational chatbot powered by Rasa.
- Ask anything related to your course or studies!
""")

# Displaying a search bar
st.markdown("### Search for your topic:")
search_query = st.text_input("Enter a topic to search for:")

# Display chat history area
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Display previous messages in the chat
for message in st.session_state['messages']:
    if message['sender'] == 'user':
        st.markdown(f"**You:** {message['text']}")
    else:
        st.markdown(f"**Bot:** {message['text']}")

# If user types something, process the message
if search_query:
    # Add user message to chat history
    st.session_state['messages'].append({'sender': 'user', 'text': search_query})

    # Get response from the Rasa bot
    bot_responses = get_bot_response(search_query)

    # Display bot's response
    for bot_response in bot_responses:
        st.session_state['messages'].append({'sender': 'bot', 'text': bot_response['text']})

# Input box for user to ask questions
user_input = st.text_input("Ask your question:")

# Handle user input
if user_input:
    # Add user message to chat history
    st.session_state['messages'].append({'sender': 'user', 'text': user_input})

    # Get response from Rasa bot
    bot_responses = get_bot_response(user_input)

    # Display bot's response
    for bot_response in bot_responses:
        st.session_state['messages'].append({'sender': 'bot', 'text': bot_response['text']})

# Optional: Add a reset button to clear chat history
if st.button("Reset Conversation"):
    st.session_state['messages'] = []

