"""
Python script for prompt template example, for the course Generative AI in Cybersecurity at UCN.

Author: Henning Thomsen
"""

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file
# Be sure to have valid API keys in this file
load_dotenv()

# Define the prompt with variables in the system message
system_template = (
    "You are a cybersecurity assistant specializing in {specialty}. "
    "Analyze the following input for threats related to {threat_type}, and provide detailed recommendations."
)

# Define prompt template (contains system message and user message)
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", "{log_data}")
])

# Instantiate the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# Format the prompt
formatted_prompt = prompt_template.format_messages(
    specialty="cloud infrastructure security",
    threat_type="unauthorized access and privilege escalation",
    log_data=(
        "Log Entry:\n"
        "User 'root' executed 'sudo su' from IP address 192.0.2.42 at 03:17 UTC.\n"
        "Followed by a 'wget' command downloading a shell script from http://malicious.example.com/install.sh"
    )
)

# Invoke the LLM
response = llm.invoke(formatted_prompt)

# Print the result (note: only content variable from response object)
print(response.content)
