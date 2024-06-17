from langchain.prompts import ChatPromptTemplate

def get_prompt_template():
    # Define your prompt template here
    # system="You are Dr. Chintu Lal great qualified professional doctor. Your response should be small and human like."
    # , you can also use some emojies (0-3 per response)
    system = """
    You are Dr. Healthy Bot great qualified professional doctor who only do online consulting. Your response should be small and human like. You don't hallucinate.

    {history}
    """
    human="{input}"
    doctor = ""
    template=ChatPromptTemplate.from_messages([
        ("system",system),
        ("human",human),
        ("ai", doctor)
    ]
    )
    return template
