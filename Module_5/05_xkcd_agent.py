"""
XKCD agent example, used in module 5, 
for the course Generative AI in Cybersecurity at UCN.

Author: Henning Thomsen
"""

import yaml
import requests
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain_community.utilities import RequestsWrapper
from langchain_community.agent_toolkits.openapi import planner

from dotenv import load_dotenv

# Load environment variables from .env file
# Be sure to have valid API keys in this file
load_dotenv()

# Fetch XKCD OpenAPI spec
openapi_spec = requests.get("https://raw.githubusercontent.com/APIs-guru/unofficial_openapi_specs/master/xkcd.com/1.0.0/openapi.yaml").text

# Parse the YAML string into a dictionary
xkcd_openapi_spec = yaml.load(openapi_spec, Loader=yaml.Loader)
xkcd_openapi_spec_reduced = reduce_openapi_spec(xkcd_openapi_spec)

# Create a requests wrapper for making HTTP requests
requests_wrapper = RequestsWrapper()

# Create an LLM to power the agent
OPENAI_MODEL = "gpt-4o-mini"
llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0)

ALLOW_DANGEROUS_REQUESTS = True

xkcd_agent = planner.create_openapi_agent(
    xkcd_openapi_spec_reduced,
    requests_wrapper,
    llm,
    allow_dangerous_requests=ALLOW_DANGEROUS_REQUESTS,
)

# Example queries to test the agent
print("XKCD API Agent Demo\n")

# Example 1: Get the current comic
print("Example 1: Getting the current comic...")
response = xkcd_agent.invoke({"input": "What is the current XKCD comic? Show me the title and image URL."})
print("Agent Response:", response["output"])
print("\n" + "-"*50 + "\n")

# Example 2: Get a specific comic by ID
print("Example 2: Getting comic #614...")
response = xkcd_agent.invoke({"input": "Get information about XKCD comic number 614. What's its title and joke?"})
print("Agent Response:", response["output"])
print("\n" + "-"*50 + "\n")

# Example 3: Find a comic with a specific feature
print("Example 3: Finding a comic from 2020...")
response = xkcd_agent.invoke({"input": "Find an XKCD comic from the year 2020. Any one will do."})
print("Agent Response:", response["output"])