from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain_community.document_loaders import AsyncChromiumLoader
#from langchain_community.document_transformers import BeautifulSoupTransformer

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# load documents from urls
loader_web = RecursiveUrlLoader(url="https://wiki.hyperledger.org/display/fabric/")

# Load HTML
loader_html = AsyncChromiumLoader(["https://hyperledger-fabric.readthedocs.io/en/release-2.5/index.html"])

# merge all the document sources
loader= MergedDataLoader(loaders=[loader_web, loader_html])

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
vectorstore.persist()

template_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
    "\n\n"
    "Now, using this guidance and adhering to the context, process the text below and give yer best answer:"
    "text: {question}"
    )

PROMPT = PromptTemplate(template=template_prompt, input_variables=["context", "question"])

chain_type_kwargs = {"prompt": PROMPT}
llm = ChatOpenAI()

vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = vectordb.as_retriever()

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs=chain_type_kwargs,
)

class Query(BaseModel):
    text: str = ""

app = FastAPI()

@app.post("/query")
async def query(query: Query):
    try:
        result = qa.run(query=query.text)
        return {"response": result}
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=500)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
