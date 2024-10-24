import streamlit as st
import os
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchResults
from langchain_community.utilities import WikipediaAPIWrapper,ArxivAPIWrapper,DuckDuckGoSearchAPIWrapper
from langchain.agents import initialize_agent,AgentType
from langchain_groq import ChatGroq
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=250)
wiki=WikipediaQueryRun(api_wrapper=api_wrapper_wiki)

arxiv_wrapper_wiki = ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=250)
arxiv=ArxivQueryRun(api_wrapper=api_wrapper_wiki)

duckduckgo_wrapper=DuckDuckGoSearchAPIWrapper(max_results=1)
duckduckgo=DuckDuckGoSearchResults(api_wrapper=duckduckgo_wrapper)


st.sidebar.title("Enter GROQ API Key")
api_key=st.sidebar.text_input("GROQ API Key",type="password")

llm= ChatGroq(model="llama3-8b-8192",api_key=api_key)

#streamlit code with title,description and chat_input
st.title("Langchain Chatbot")
st.write("Chatbot querying Wikipedia, Arxiv and DuckDuckGo")

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assistant","content":"Hello! I am a chatbot that can query Wikipedia, Arxiv and DuckDuckGo. Ask me anything!"}
    ]
    
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt:=st.chat_input(placeholder="Enter your query"):
    st.session_state["messages"].append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)


    tools=[arxiv,wiki,duckduckgo]
    search_agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handling_parsing_errors=True,
    )


    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        response=search_agent.run(st.session_state["messages"],callbacks=[st_callback])
        st.session_state["messages"].append({"role":"assistant","content":response})
        st.write(response)
    
    
    
    
    


   
        




