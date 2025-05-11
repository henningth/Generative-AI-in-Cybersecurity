"""
Starter code for exercise 4, module 4, 
for the course Generative AI in Cybersecurity at UCN.

Author: Henning Thomsen
"""

from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, AgentType
from langchain.agents import Tool

import requests
import os

from dotenv import load_dotenv
load_dotenv()

# Set up the LLM
OPENAI_MODEL = "gpt-4o-mini"
llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.1)

# Define the two tools that the LLM agent has at its disposal
# Tool 1: IP Lookup
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
    
# Tool 2: Real Threat Intelligence using AbuseIPDB
def check_ip_reputation(ip: str) -> str:
    url = f"https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": os.getenv("ABUSEIPDB_API_KEY"),
        "Accept": "application/json"
    }
    params = {"ipAddress": ip}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if data['data']['abuseConfidenceScore'] > 0:
            return (f"{ip} is flagged as malicious. "
                    f"Abuse Confidence Score: {data['data']['abuseConfidenceScore']}%. "
                    f"Reported incidents: {data['data']['totalReports']}.")
        else:
            return f"{ip} is not flagged in AbuseIPDB's database."
    except Exception as e:
        return f"Error during threat check: {str(e)}"
    
# Register tools
tools = [
    Tool(
        name="IPLookup",
        func=ip_lookup,
        description="Use this tool to get geolocation and ownership details of an IP address. Input should be an IP like 8.8.8.8."
    ),
    Tool(
        name="ThreatIntel",
        func=check_ip_reputation,
        description="Use this tool to check if an IP address has been flagged for malicious activity using AbuseIPDB. Input should be an IP address."
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
result = agent.invoke("Check the IP 185.199.110.153 and give me a threat report that includes location, ASN, ISP, and whether it's in any abuse databases.")

print("ReAct agent result:\n")
print(result["output"])