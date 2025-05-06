"""
Python script for exercise 1 in module 1, for the course Generative AI in Cybersecurity at UCN.

Author: Henning Thomsen
"""

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from .env file
# Be sure to have valid API keys in this file
load_dotenv()

# Define your prompt here, as per exercise text
prompt = """
Explain in max three sentences why one should study Generative AI in Cybersecurity.
"""

# Run OpenAI model
llm = ChatOpenAI(model="gpt-4o", temperature=0.1, verbose=True)
response = llm.invoke(prompt)
print(response)

"""
# Run model via Groq
llm = ChatGroq(model="llama3-8b-8192", temperature=0)
response = llm.invoke(prompt)
print(response.content)
"""