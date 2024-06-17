import streamlit as st
from dotenv import load_dotenv
# import chatbot_logic
import chatbot_logic
from chatbot_logic import get_response
import os
import random
import time
import pickle
from pathlib import Path

# Load the .env file
load_dotenv()
# Streamed response emulator
def response_generator(user_query):
    response = get_response(user_query)
    split_text = response.split('\n')
    final_split = []
    for sen in split_text:
        final_split.extend(sen.split())
        final_split.append('\n')
    # print(final_split)
    for word in final_split:
        yield word + " "
        time.sleep(0.05)

# Streamlit App

with st.expander(":exclamation: :red[Disclaimer]", True):
    st.write("""
    **Please Note:** This AI chatbot is designed to provide helpful information and support. However, it is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

    If you think you may have a medical emergency, call your doctor or emergency services immediately. Reliance on any information provided by this chatbot is solely at your own risk.
    """)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if len(st.session_state.messages) == 0:
    chatbot_logic.memory.clear()

# st.title("MediChat")

# st.session_state.current_chat = ""

def make_new_chat_button():
    initial_items = st.session_state.items_list
    item_ind = 0
    item = f'chat_{item_ind}'
    while item in initial_items:
        item_ind += 1
        item = f'chat_{item_ind}'
    initial_items = initial_items + [item]
    st.session_state.items_list = initial_items
    st.rerun()

def make_new_chat():
    st.session_state.messages = []
    # initial_items = st.session_state.items_list
    # item_ind = 0
    # item = f'chat_{item_ind}'
    # while item in initial_items:
    #     item_ind += 1
    #     item = f'chat_{item_ind}'
    # initial_items = initial_items + [item]
    # st.session_state.items_list = initial_items
    # st.rerun()

with st.sidebar:
    # Sample data
    # initial_items = []
    if 'items_list' not in st.session_state:
        initial_items = []
        st.session_state.items_list = initial_items

    # Initialize session state to hold the list of items
    # if 'items_list' not in st.session_state:
    #     st.session_state.items_list = initial_items
    
    # st.session_state.items_list = initial_items

    # Function to simulate an expensive computation (e.g., loading data)
    @st.cache_data
    def expensive_computation():
        import time
        time.sleep(5)  # Simulate a delay
        return "Expensive computation result"
    




    # Display the result of the expensive computation
    # result = expensive_computation()

    chat_init = {}

    def delete_item(item, index):
        message_file_path = Path(f'./data/chat_message_history/{item}_messages.pkl')
        if message_file_path.exists():
            message_file_path.unlink()

        summary_file_path = Path(f'./data/chat_summary_history/{item}_summary.pkl')
        if summary_file_path.exists():
            summary_file_path.unlink()

        st.session_state.items_list.pop(len(st.session_state.items_list)-index-1)
        st.session_state.messages = []
        del st.session_state[item]
        del st.session_state[f'delete_{item}']
    
    def save_chat_messages(item):
        # print("\n\n\nsaving to...........................", item, "\n\n\n")
        with open(f'./data/chat_message_history/{item}_messages.pkl', 'wb') as f:
            # print("messages: ", st.session_state.messages)
            pickle.dump(st.session_state.messages, f)
        with open(f'./data/chat_message_history/{item}_messages.txt', 'w') as f:
            f.write(str(st.session_state.messages))

    if "current_value" not in st.session_state:
        st.session_state.current_value = ""
        try:
            st.session_state.current_value = st.session_state.items_list[-1]
        except:
            pass

    if st.session_state.current_value == "":
        initial_items = st.session_state.items_list
        item_ind = 0
        item = f'chat_{item_ind}'
        while item in initial_items:
            item_ind += 1
            item = f'chat_{item_ind}'
        st.session_state.current_value = item
    print("CURRENT VALUE: ", st.session_state.current_value)

    def save_chat_summary(item):
        with open(f'./data/chat_summary_history/{item}_summary.pkl', 'wb') as f:
            pickle.dump(chatbot_logic.memory.load_memory_variables({})['history'], f)

    col1, col2 = st.columns([0.5, 0.5])
    with col2:
        if st.button('New Chat', type = "secondary", key = 'new_chat_button', help = 'Open new chat', use_container_width = True):
            initial_items = st.session_state.items_list
            item_ind = 0
            item = f'chat_{item_ind}'
            while item in initial_items:
                item_ind += 1
                item = f'chat_{item_ind}'
            # initial_items = initial_items + [item]
            # st.session_state.items_list = initial_items
            try:
                if st.session_state.messages != []:
                    save_chat_messages(st.session_state.current_value)
                    save_chat_summary(st.session_state.current_value)
                    st.session_state.current_value = item
            except:
                pass
            make_new_chat()
            # st.rerun()
            pass

    st.title("Chat History")

    # Display each item with a delete button
    for index, item in enumerate(reversed(st.session_state.items_list)):
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            item_val = "Chat " + str(int(item.split('_')[1])+1)
            if st.button(item_val, type = "secondary", key=item, help=f"{item}: chat history"):
                # chatbot_logic.memory.load_memory_variables({})['history'] = "You are a doctor"
                print(chatbot_logic.memory.load_memory_variables({}))
                save_chat_messages(st.session_state.current_value)
                save_chat_summary(st.session_state.current_value)
                messages_hist = []
                try:
                    with open(f'./data/chat_message_history/{item}_messages.pkl', 'rb') as file:
                        messages_hist = pickle.load(file)
                except:
                    messages_hist = []
                
                st.session_state.messages = messages_hist
                st.session_state.current_value = item
                # print("\n\n\ncurrent value...:", st.session_state.current_value, "\n\n\n")
        with col2:
            if st.button('x', type = "secondary", key=f'delete_{item}', help=f"{item}: Delete history", use_container_width = True):
                delete_item(item, index)
                st.rerun()
    # st.write(st.session_state)
    




# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Message Dr. Healthy Bot"):
    # Add user message to chat history
    # st.session_state.new_chat_button = True
    # if len(st.session_state.messages) == 0:
    #     make_new_chat()
    st.session_state.messages.append({"role": "user", "content": prompt})
    # with open(f'{this_chat}.pkl', 'wb') as f:
    #     pickle.dump(st.session_state.messages, f)
    # print("SESSION_STATE\n", st.session_state)
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    if len(st.session_state.messages) == 2:
        make_new_chat_button()
        pass
    # save_chat_messages()
# st.write(st.session_state)
