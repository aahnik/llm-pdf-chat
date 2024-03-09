from InstructorEmbedding import INSTRUCTOR
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatAnthropic
from langchain.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    AIMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import DuckDuckGoSearchRun
from langchain.vectorstores import Chroma
from PyPDF2 import PdfReader

CHROMA_PERSIST_DB_DIR = "db"


def load_pdfs(look_dir):
    loader = DirectoryLoader(look_dir, glob="./*.txt", loader_cls=TextLoader)

    documents = loader.load()
    len(documents)


def process_pdfs(documents):
    # splitting the text into
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    instructor_embeddings = HuggingFaceInstructEmbeddings(
        model_name="hkunlp/instructor-xl", model_kwargs={"device": "cuda"}
    )


def setup_vectordb(embedding):

    vectordb = Chroma.from_documents(
        documents=texts, embedding=embedding, persist_directory=CHROMA_PERSIST_DB_DIR
    )

    # making out retriever
    retriever = vectordb.as_retriever(search_kwargs={"k": 7})


def create_chain():
    # create the chain to answer questions
    llm = ChatAnthropic(model="claude-2", temperature=0.0)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
    )

    return qa_chain
