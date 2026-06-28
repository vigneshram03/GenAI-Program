import os
import time
from hashlib import md5

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


SYSTEM_PROMPT = """
You are Dutch Agri Assistant.

Answer ONLY from the retrieved Government of the Netherlands Agriculture context.

Instructions:
- Use only the retrieved context.
- Combine multiple chunks when necessary.
- If the answer is incomplete, clearly state what is available.
- If the answer is not explicitly available, provide relevant information from the retrieved context and suggest related agriculture topics instead of simply saying you don't know.
- Format answers using short paragraphs and bullet points whenever appropriate.

Context:
{context}
"""


class RAGEngine:

    def __init__(self):

        self.documents = []
        self.chunks = []

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            streaming=True,
            tags=["DutchAgriAssistant", "RAG"],
            metadata={
                "application": "DutchAgriAssistant",
                "embedding_model": "text-embedding-3-small",
                "llm": "gpt-4o-mini"
            }
        )

        self.vector_store = None
        self.retriever = None
        self.chain = None

        self.cache_root = "faiss_index"
        os.makedirs(self.cache_root, exist_ok=True)

    def create_documents(self, pages):
        self.documents = [
            Document(
                page_content=p["text"],
                metadata={"title": p["title"], "url": p["url"]}
            )
            for p in pages
        ]

    def split_documents(self):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150
        )
        self.chunks = splitter.split_documents(self.documents)

    def _cache_path(self, url):
        return os.path.join(self.cache_root, md5(url.encode()).hexdigest())

    def build_vector_store(self, url):
        folder = self._cache_path(url)

        if os.path.exists(folder):
            self.vector_store = FAISS.load_local(
                folder,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            return

        self.vector_store = FAISS.from_documents(
            self.chunks,
            self.embeddings
        )
        self.vector_store.save_local(folder)

    def create_retriever(self):
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )

    @staticmethod
    def format_documents(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def build_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "{question}")
        ])

        self.chain = (
            {
                "context": self.retriever | self.format_documents,
                "question": RunnablePassthrough(),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        ).with_config(
            {
                "run_name": "DutchAgriAssistant-RAG",
                "tags": ["production", "government", "agriculture"],
                "metadata": {
                    "application": "DutchAgriAssistant"
                }
            }
        )

    def index_pages(self, pages, website_url):
        self.create_documents(pages)
        self.split_documents()
        self.build_vector_store(website_url)
        self.create_retriever()
        self.build_chain()

    def retrieve(self, question):
        return self.retriever.invoke(question)

    def get_sources(self, question):
        docs = self.retrieve(question)

        seen = set()
        sources = []

        for doc in docs:
            url = doc.metadata["url"]
            if url in seen:
                continue
            seen.add(url)
            sources.append({
                "title": doc.metadata["title"],
                "url": url,
                "snippet": doc.page_content[:250] + "..."
            })
        return sources

    def ask(self, question):
        start = time.perf_counter()
        answer = self.chain.invoke(
            question,
            config={
                "run_name": "QuestionAnswer",
                "metadata": {
                    "question": question
                }
            }
        )
        latency = time.perf_counter() - start

        return {
            "answer": answer,
            "sources": self.get_sources(question),
            "latency": latency
        }

    def stream_answer(self, question):
        for token in self.chain.stream(
            question,
            config={
                "run_name": "StreamingAnswer",
                "metadata": {
                    "question": question
                }
            }
        ):
            yield token

    def generate_summary(self):
        return self.ask(
            "Summarize this website in five concise bullet points."
        )["answer"]
