"""
Starter code for exercise 2, module 4, 
for the course Generative AI in Cybersecurity at UCN.

Author: Henning Thomsen
"""

from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain.agents import Tool

import requests

from dotenv import load_dotenv
load_dotenv()

# Set up the LLM
OPENAI_MODEL = "gpt-4o-mini"
llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.1)

# Define the tool that the LLM agent has at its disposal
def ip_lookup(ip_address: str) -> str:
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        print(data)
        if data['status'] == 'success':
            return (
                f"IP: {data['query']}\n"
                f"Country: {data['country']}\n"
                f"Region: {data['regionName']}\n"
                f"City: {data['city']}\n"
                f"ISP: {data['isp']}\n"
                f"Org: {data['org']}\n"
                f"AS: {data['as']}"
            )
        else:
            return f"IP lookup failed: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Error during IP lookup: {str(e)}"
    
# Register tool
tools = [
    Tool(
        name="IPLookup",
        func=ip_lookup,
        description="Use this tool to get geolocation and ownership details of an IP address. Input should be an IP like '8.8.8.8'."
    )
]

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Example chained run
result = agent.invoke("Where is the IP address 66.240.205.34 located?")
print("ReAct agent result:\n")
print(result["output"])