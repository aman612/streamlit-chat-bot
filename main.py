import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize session state
def init_session_state() -> None:
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []

# Display chat messages
def display_messages() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Generate response from OpenAI and update session state
def generate_response(prompt: str, client: OpenAI) -> None:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error generating response: {e}")

# Main function to run the app
def main() -> None:
    # Set the title of the app
    st.title("Tom Parlante")

    # Initialize the OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_II"))

    init_session_state()
    display_messages()

    if prompt := st.chat_input("What is up?"):
        generate_response(prompt, client)

if __name__ == "__main__":
    main()
