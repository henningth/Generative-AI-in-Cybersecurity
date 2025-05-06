"""
Starter file for exercise 4 in module 2, for the course Generative AI in Cybersecurity at UCN.

Author: Henning Thomsen
"""

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file
# Be sure to have valid API keys in this file
load_dotenv()

# Define LLM (test with both OpenAI and Groq models)
llm = ChatGroq(model="llama3-8b-8192", temperature=0.1)

# Define prompt template
prompt_template = """
Classify the given email message as either spam or legitimate.

Examples are given below:

Message: "Hi Alex, just confirming our meeting tomorrow at 10 AM—let me know if anything changes."
Classification: Legitimate

Message: "Your account has been compromised—click here immediately to verify your identity and avoid suspension!"
Classification: Spam

Message: {message}
Classification: 
"""

# Make a prompt template using the above prompt.
spam_classification_prompt_template = PromptTemplate(
    input_variables = ["message"],
    template = prompt_template
)

# Format the prompt
spam_classification_prompt = spam_classification_prompt_template.format(message="Hey. Nice to see you! Best regards, Rick.")

# Invoke LLM
result = llm.invoke(spam_classification_prompt)

# Print result
print(result.content)