"""
Python file for Retrieval Augmented Generation, for the course Generative AI in Cybersecurity at UCN.

Author: Henning Thomsen
"""
# Load environment variables from .env file
# Be sure to have valid API keys in this file

from dotenv import load_dotenv

load_dotenv()

# Loading the PDF file. Try also with other files.

from langchain_community.document_loaders import PyPDFLoader

file_path = (
    "A-Survey-of-Large-Language-Models.pdf"
)

loader = PyPDFLoader(file_path)

pages = loader.load()

# Splitting the loaded document into chunks. Try various splits and see if there is a difference.

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)

all_splits = text_splitter.split_documents(pages)

# Ingest the document chunks into the vectorstore

from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

retrieved_docs = retriever.invoke("What are neural language models?")

print(retrieved_docs[0])

print(len(retrieved_docs))

"""
Now, we will look at a simple RAG application. It ingests the same 
"""

from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

template = """Answer the question based only on the following context: {context}
Question: {question}"""

prompt = PromptTemplate.from_template(template)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

retriever = vectorstore.as_retriever()

chain = (
{"context": retriever, "question": RunnablePassthrough()}
| prompt
| llm
| StrOutputParser()
)

result = chain.invoke("What are neural language models?")

print(result)