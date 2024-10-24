from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain

st.set_page_config(page_title="Langchain Chatbot",page_icon="🤖")
st.title("Langchain Chatbot")
st.subheader("Chatbot summarising text and video content")

with st.sidebar:
    groq_api_key=st.text_input("Enter GROQ API Key",value="",type="password")

llm=ChatGroq(model="Gemma-7b-It",groq_api_key=groq_api_key)
prompt_template="""
Provide the summary of the content from the given URL in about 300 words
Content:{text}
"""
prompt=PromptTemplate(template=prompt_template,input_variables=["text"])
generic_url=st.text_input("Enter URL",label_visibility="collapsed")
if st.button("Summarise the content from YT or website"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please enter the required information")
    elif not validators.url(generic_url):
        st.error("Invalid URL")
    else:
        try:
            with st.spinner("Summarising ..."):
                if "youtube" in generic_url:
                    loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=True)
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False)     
            docs=loader.load()
                
            chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
            output_summary=chain.run(docs)
            st.success(output_summary)
        except Exception as e:
            st.error(f"Exception : {e}")
            