"""
Starter code for exercise 1, module 4, 
for the course Generative AI in Cybersecurity at UCN.

Author: Henning Thomsen
"""

from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.agents import Tool

# Load environment variables from .env file
# Be sure to have valid API keys in this file

from dotenv import load_dotenv
load_dotenv()

# Define the Python function that you want the agent to execute
def my_function(input: str) -> str:
    # Add your Python code here
    output = input
    return output

# Map the function to a tool (be sure to modify the name, func and description).
tools = [
    Tool(
        name="MyFunction",
        func=my_function,
        description="Use this tool to parse an input string, and return parsed string."
    )
]

# Define LLMs
# OpenAI model
OPENAI_MODEL = "gpt-4o-mini"
openai_llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.1)

# Open source model via Groq
GROQ_MODEL = "llama3-8b-8192"
groq_llm = ChatGroq(model=GROQ_MODEL, temperature=0.1)

agent = initialize_agent(
    tools=tools,
    llm=openai_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

QUERY = "Pass this string to the tool."

response = agent.invoke(QUERY)
print("Agent Response:", response["output"])