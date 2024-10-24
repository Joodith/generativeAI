import streamlit as st
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain.chains import LLMMathChain,LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import Tool,initialize_agent,AgentType
from langchain_groq import ChatGroq
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from dotenv import load_dotenv
# load_dotenv()

st.set_page_config(page_title="ChatSQL",page_icon="🦜",layout="wide")
st.title("Maths Solver using Langchain")
st.subheader("Chatbot to solve math and reasoning problems")

with st.sidebar.title("Enter GROQ API Key"):
    groq_api_key=st.text_input("Enter GROQ API Key",value="",type="password")

# llm=ChatGroq(model="Gemma-7b-It")
llm=ChatGroq(model="Gemma-7b-It",groq_api_key=groq_api_key)

wikipedia=WikipediaAPIWrapper()
wikipedia_tool=WikipediaQueryRun(api_wrapper=wikipedia)

problem_chain=LLMMathChain(llm=llm)
maths_tool=Tool.from_function(name="Calculator",func=problem_chain.run,description="Useful when you need to answer questions about math and is used only for math questions and for nothing else.Only input math expressions")

word_problem_template="""You are a reasoning agent expert at solving user's logic based questions.Logically solve the problem and keep it factual.
Clearly explain the steps involved in bullet points and give the final answer.Question : {question} Answer: 
"""
math_assistant_template=PromptTemplate(template=word_problem_template,input_variables=["question"])
word_problem_chain=LLMChain(llm=llm,prompt=math_assistant_template)
word_problem_tool=Tool.from_function(name="Reasoning tool",func=word_problem_chain.run,description="Useful when you need to solve a reasoning/logic-based questions")

agent=initialize_agent(
    tools=[wikipedia_tool,maths_tool,word_problem_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)
# response=agent.invoke({"input": "I initially have 3 apples and 4 oranges. I give half of my oranges away and buy two dozen new ones, alongwith three packs of  strawberries. Each pack of strawberry has 30 strawberries. How  many total pieces of fruit do I have at the end?"})
# print(response)

if "messages" not in st.session_state or st.sidebar.button("Clear chat history"):
    st.session_state["messages"]=[{
        "role":"assistant","content":"Hello! I am a chatbot that can solve math and reasoning problems. Ask me anything!"
    }]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if user_query:=st.chat_input(placeholder="Enter the logical query: "):
    st.session_state["messages"].append({"role":"user","content":user_query})
    st.chat_message("user").write(user_query)
    with st.chat_message("assistant"):
        streamlit_callback=StreamlitCallbackHandler(st.container())
        response=agent.run(st.session_state["messages"],callbacks=[streamlit_callback])
        st.session_state["messages"].append({"role":"assistant","content":response})
        st.chat_message("assistant").write(response)
        
        

