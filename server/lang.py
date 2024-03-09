from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatAnthropic
from langchain_community.embeddings import HuggingFaceInstructEmbeddings


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from config import CONFIG
from crud import get_llm_config

CHROMA_PERSIST_DB_DIR = "chroma-db"


def load_pdfs(look_dir):
    loader = PyPDFDirectoryLoader(look_dir)
    documents = loader.load()
    return documents


def process_pdfs(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    instructor_embeddings = HuggingFaceInstructEmbeddings(
        model_name="hkunlp/instructor-xl", model_kwargs={"device": "cuda"}
    )
    return texts, instructor_embeddings


def setup_vectordb(texts, embedding):
    vectordb = Chroma.from_documents(
        documents=texts, embedding=embedding, persist_directory=CHROMA_PERSIST_DB_DIR
    )
    return vectordb.as_retriever(search_kwargs={"k": 7})


def create_chain(retreiver, model="claude-2", temp=0.0):

    llm = ChatAnthropic(model=model, temperature=temp)
    return RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retreiver, return_source_documents=True
    )


docs = None
texts, embeddings = None, None
retreiver = None
chain = None


async def load_chain():
    global chain
    model, temp = await get_llm_config()
    chain = create_chain(retreiver, model, temp)


async def process_docs():
    global docs, texts, embeddings, retreiver
    docs = load_pdfs(CONFIG.files_dir)
    texts, embeddings = process_pdfs(docs)
    retreiver = setup_vectordb(texts, embeddings)
