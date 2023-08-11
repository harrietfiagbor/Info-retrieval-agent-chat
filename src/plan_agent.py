import os
import logging 
from dotenv import load_dotenv

from langchain import PromptTemplate
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.utilities import WikipediaAPIWrapper

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo', streaming=True)

search = DuckDuckGoSearchRun()
wikipedia = WikipediaAPIWrapper()

# Web search Tool
search_tool = Tool(
    name="Web Search",
    func=search.run,
    description="A useful tool for searching the Internet to find information on world events, issues, etc. Worth using for general topics. Use precise questions."
)

# Wikipedia Tool
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia.run,
    description="A useful tool for searching the Internet to find information on world events, issues, etc. Worth using for general topics. Use precise questions."
)

try:
    with open('./generate_template.txt') as file_1, open('./plan_prompt_template.txt') as file_2:
        generate_template = file_1.read()
        plan_template = file_2.read()
except OSError as error:
    logging.error('This Error Occurred: %s', error)

# with open('./src/generate_template.txt') as file_1:
#     generate_template = file1.read()

prompt = PromptTemplate(
    template=generate_template,
    input_variables=["input", "chat_history"]
)

plan_prompt = PromptTemplate(
    template=plan_template,
    input_variables=["input", "chat_history"]
)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True )

plan_chain = ConversationChain(
    llm=llm,
    memory=memory,
    input_key="input",
    prompt=plan_prompt,
    output_key="output"
)

agent = initialize_agent(
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    tools=[search_tool, wikipedia_tool],
    llm=llm,
    max_iterations=3,
    prompt=prompt,
    memory=memory
)


