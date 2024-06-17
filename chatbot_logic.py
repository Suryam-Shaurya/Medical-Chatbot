import os
from dotenv import load_dotenv
import langchain
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from prompts import get_prompt_template
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.prompts.prompt import PromptTemplate
import time
import datetime

# Access the API key
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')

# Initialize the language model
llm = ChatGroq(model="llama3-8b-8192", api_key=api_key)

def comm_2():
    # # Get the prompt template
    # prompt = get_prompt_template()

    # # Create the chain
    # chain = prompt | llm


    # def get_response(user_query):
    #     response_chunks = chain.stream({"text": user_query})
    #     response = "".join(chunk.content for chunk in response_chunks)
    #     return response






    # template = """The following is a conversation between a human and an AI doctor.
    # If the AI does not know the answer to a question, it truthfully says it does not know. The AI ONLY uses information contained in the "Relevant Information" section (which is having summary of conversation happend yet) and does not hallucinate.
    # AI name is Dr. Healthy Bot, a great qualified professional doctor. It's response should be small and human like.

    # Relevant Information: 
    # {history}

    # Conversation:
    # Human: {input}
    # AI:"""

    # prompt = PromptTemplate(input_variables=["history", "input"], template=template)
    # conversation_with_kg = ConversationChain(
    #     llm=llm, verbose=True, prompt=prompt, memory=ConversationSummaryBufferMemory(llm=llm, max_token_limit=30)
    # )
    pass

prompt = get_prompt_template()

def comm():
    # prompt = PromptTemplate(input_variables={'summary', 'new_lines'}, template=template)
    # memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=10)
    # memory.save_context({"input": "hi"}, {"output": "whats up"})
    # print("jgfhjgh.................", memory.load_memory_variables({}))
    # messages = memory.chat_memory.messages
    # print(messages)
    # print()
    # previous_summary = ""
    # moving_sum = memory.predict_new_summary(messages, previous_summary)
    # print("PURANAAAAA.....", moving_sum)
    # memory.save_context({"input": "not much you"}, {"output": "not much"})
    # print("jgfhjgh.................", memory.load_memory_variables({}))
    # messages = memory.chat_memory.messages
    # print(messages)
    # print()
    # previous_summary = ""
    # print("NAAYAYAYAYA.....", memory.predict_new_summary(messages, moving_sum))
    pass

memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=150)
verbose_output = []
conversation_with_summary = ConversationChain(
    llm=llm,
    prompt = prompt,
    # We set a very low max_token_limit for the purposes of testing.
    memory=memory,
    verbose=False
)


# while True:
#     user_input = input("User:")
#     print(conversation_with_summary.predict(input=user_input))

def save_summary(summary):
    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date and time into a string that can be used as a file name
    timestamp = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')

    chat_topic = "dupli_summ"

    # Specify the file name with the timestamp
    file_name = f"./data/chat_summary_history/{chat_topic}.txt"

    # Write the content to the file
    with open(file_name, 'w', encoding='utf-8') as file:
        summary = f"{timestamp}\n" + summary
        file.write(summary)

def get_response(user_query):
    # print(conversation_with_summary)
    response = conversation_with_summary.predict(input=user_query)
    summary = memory.load_memory_variables({})['history']
    # print(summary)
    save_summary(summary)
    return response
















