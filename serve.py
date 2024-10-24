import os
from  fastapi import FastAPI
from langserve import add_routes
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="llama3-8b-8192",groq_api_key=groq_api_key)

system_template="""
Translate the following into {language}
"""
prompt_template=ChatPromptTemplate.from_messages([
    "system",system_template,
    "user",'{input}'
])

parser=StrOutputParser()
chain=prompt_template|model|parser
app=FastAPI(title="langchain_server",version="1.0",description="Simple api server using langchain runnable interface")

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)


