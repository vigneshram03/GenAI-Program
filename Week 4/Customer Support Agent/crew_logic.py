import os
# pyrefly: ignore [missing-import]
from crewai import Agent, Task, Crew, Process
# pyrefly: ignore [missing-import]
from crewai.tools import tool
# pyrefly: ignore [missing-import]
from crewai_tools import SerperDevTool

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Initialize FAISS Vector Database from local text file
def initialize_faiss_rag():
    txt_path = "knowledge_base.txt"
    if not os.path.exists(txt_path):
        return None

    loader = TextLoader(txt_path, encoding='utf-8')
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(docs, embeddings)
    
    return vector_store.as_retriever(search_kwargs={"k": 2})

# Setup retriever globally for the custom tool instance
retriever = initialize_faiss_rag()

@tool("Company Knowledge Base RAG Tool")
def custom_rag_tool(query: str) -> str:
    """Useful to search internal company documents, policies, FAQs, and procedures 
    for specific details like password resets, payroll cut-offs, or HR policies.
    """
    if not retriever:
        return "Error: Local knowledge base text file not found."
    
    relevant_docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    return context

def run_support_crew(user_query: str):
    """Orchestrates the multi-agent sequential pipeline execution."""
    
    # 1. Agent Definitions
    knowledge_assistant = Agent(
        role="Internal FAQ Assistant",
        goal="Provide accurate answers to customer queries exclusively using the provided company documentation.",
        backstory="You are a highly efficient internal support agent. Your job is to look up company policies, FAQs, and procedures in the provided knowledge base.",
        tools=[custom_rag_tool],
        verbose=True
    )

    web_assistant = Agent(
        role="Web Search Assistant",
        goal="Search the web for up-to-date details regarding the customer's query and provide a well-rounded answer.",
        backstory="You are an expert internet researcher. When a customer query comes in, you scour the live web to find accurate public information.",
        tools=[SerperDevTool()],
        verbose=True
    )

    entry_agent = Agent(
        role="Entry Agent",
        goal="Compile the results from the previous agents, save them to a file, and format the output.",
        backstory="You are a meticulous data administrator who securely logs information into a text file.",
        tools=[],
        verbose=True
    )

    # 2. Task Definitions
    task_rag = Task(
        description=f"Search the internal company FAQ document for the answer to this query: '{user_query}'. Rely strictly on the custom RAG tool details.",
        expected_output="A concise response answering the query based solely on the internal vector store data.",
        agent=knowledge_assistant
    )

    task_web = Task(
        description=f"Search the internet to find information related to this query: '{user_query}'. Look for recent updates or standard external practices.",
        expected_output="A comprehensive summary of the web search results answering the query.",
        agent=web_assistant
    )

    task_compile = Task(
        description=(
            f"1. Take the original query: '{user_query}'\n"
            f"2. Take the final text output from the Internal FAQ Assistant.\n"
            f"3. Take the final text output from the Web Search Assistant.\n"
            f"4. Format them cleanly and write everything into a file named 'answers.txt'."
        ),
        expected_output="A final layout containing both full answers clearly separated.",
        agent=entry_agent,
        output_file="answers.txt"
    )

    # 3. Crew Setup and Execution
    support_crew = Crew(
        agents=[knowledge_assistant, web_assistant, entry_agent],
        tasks=[task_rag, task_web, task_compile],
        process=Process.sequential,
        verbose=True
    )

    support_crew.kickoff()
    
    # Return both raw outputs to be displayed in the UI
    ans1 = task_rag.output.raw if task_rag.output else "No internal data found."
    ans2 = task_web.output.raw if task_web.output else "No external search data found."
    
    return ans1, ans2