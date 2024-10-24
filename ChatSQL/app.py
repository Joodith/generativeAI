import os
import streamlit as st
import sqlite3
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain.agents import AgentType
from sqlalchemy import create_engine
from langchain_community.agent_toolkits import SQLDatabaseToolkit,create_sql_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler



st.set_page_config(page_title="ChatSQL",page_icon="🦜",layout="wide")
st.title("🦜 Langchain: Chat with SQL DB")

LOCALDB="USE_LOCAL_DB"
POSTGRES_DB="USE_POSTGRES_DB"

radio=st.sidebar.radio("Select Database",options=[LOCALDB,POSTGRES_DB])
if radio==POSTGRES_DB:
    db_uri=POSTGRES_DB
    pg_host=st.sidebar.text_input("Postgres Host")
    pg_username=st.sidebar.text_input("Postgres Username")
    pg_password=st.sidebar.text_input("Postgres Password",type="password")
    pg_dbname=st.sidebar.text_input("Postgres DB Name")
   
else:
    db_uri=LOCALDB        

st.sidebar.title("Enter GROQ API Key")
api_key=st.sidebar.text_input("GROQ API Key",type="password")

if  not db_uri:
    st.info("Please select a database")
    
if not api_key:
    st.info("Please enter a GROQ API Key")

llm= ChatGroq(model="llama3-8b-8192",api_key=api_key)

@st.cache_resource
def configure_db(db_uri,pg_host=None,pg_username=None,pg_password=None,pg_dbname=None):
    if db_uri==LOCALDB:
        db_path=os.path.join(os.getcwd(),"student.db")
        creator=lambda: sqlite3.connect(f"file:{db_path}?mode=ro",uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=creator))
    else:
        if (not pg_host) or (not pg_username) or (not pg_password) or (not pg_dbname):
            st.error("Please enter Postgres credentials")
            st.stop()
        return SQLDatabase(create_engine(f"postgresql://{pg_username}:{pg_password}@{pg_host}/{pg_dbname}"))

if db_uri==POSTGRES_DB:
    db=configure_db(db_uri,pg_host,pg_username,pg_password,pg_dbname)
else:
    db=configure_db(db_uri)


toolkit=SQLDatabaseToolkit(db=db,llm=llm)


if "messages" not in st.session_state or st.sidebar.button("Clear chat history"):
    st.session_state["messages"]=[
        {"role":"assistant","content":"Hello! I am a chatbot that can query the SQL database. Ask me anything!"}
    ]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])



if user_query:=st.chat_input(placeholder="Enter your query"):
    st.session_state["messages"].append({"role":"user","content":user_query})
    st.chat_message("user").write(user_query)
    agent=create_sql_agent(llm=llm,toolkit=toolkit,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True,handle_parsing_errors=True)
    with st.chat_message("assistant"):
        streamlit_callback=StreamlitCallbackHandler(st.container())
        response=agent.run(st.session_state["messages"],callbacks=[streamlit_callback])
        st.session_state["messages"].append({"role":"assistant","content":response})
        st.write(response)
    
    

    



