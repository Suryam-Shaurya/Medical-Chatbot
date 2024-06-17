import streamlit as st
import random
import time

# Create a fixed position collapsible section

# Using "with" notation
with st.sidebar:
    # Sample data
    initial_items = ["Loose Motions and Symptoms", "Doctor-Patient Role Play", 
                    "Unexpected Input Variables", "Memory-enhanced Conversation", 
                    "Library for Conversational Agents", "Create collapsible disclaimer section"]

    # Initialize session state to hold the list of items
    if 'items_list' not in st.session_state:
        st.session_state.items_list = initial_items

    # Function to simulate an expensive computation (e.g., loading data)
    @st.cache_data
    def expensive_computation():
        import time
        time.sleep(5)  # Simulate a delay
        return "Expensive computation result"

    def delete_item(index):
        st.session_state.items_list.pop(index)


    st.title("Custom List with Delete Option")

    # Display the result of the expensive computation
    result = expensive_computation()

    # Display each item with a delete button
    for index, item in enumerate(st.session_state.items_list):
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.button(item, type = "secondary", key=f'chat_{index}', help=f"{item}: chat history")
        with col2:
            if st.button('x', type = "primary", key=f'delete_{index}', help=f"Delete history"):
                delete_item(index)
                st.experimental_rerun()


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})