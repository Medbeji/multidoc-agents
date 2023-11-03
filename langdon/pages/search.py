import streamlit as st
import random
import time
import streamlit.components.v1 as components
from PIL import Image


st.set_page_config(layout="wide")

st.title("Ask Sales for Wiki")
col1, col2 = st.columns([1, 1])
prompt = st.chat_input("What is up?")

# Display website in the first column
website_url = ""  # Set this to an empty string to test the image placeholder
placeholder_image_url = "langdon/pages/assets/sales_wiki.png"  # URL of your placeholder image

with col1: 
    if website_url:
        iframe_code = f'<iframe src="{website_url}" width="100%" height="400" frameborder="0"></iframe>'
        components.html(iframe_code, height=400)
    else:
        image = Image.open(placeholder_image_url)

        st.image(image, caption="Website is not available", use_column_width=True)

with col2:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    else: 
        st.session_state.messages = st.session_state.messages[:-5]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            assistant_response = random.choice(
                [
                    "Hello there! How can I assist you today?",
                    "Hi, human! Is there anything I can help you with?",
                    "Do you need help?",
                ]
            )
            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
