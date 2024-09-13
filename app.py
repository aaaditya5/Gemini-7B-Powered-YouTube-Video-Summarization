import os
import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
from dotenv import load_dotenv
load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")
#streamlit app
st.set_page_config(page_title="LANGCHAIN:Summarize text from YT or website",page_icon="🦜")
st.title("🦜 Langchain: Summarize Text from from YT or website ")
st.subheader("Summarize URL")
##llm that we used is gemma 7b it model ##now i need to set the groq api key
llm=ChatGroq(model='Gemma-7b-It',groq_api_key=groq_api_key)
#now we will create the prompt template for user 
prompt_template="""
provide a text summary of the following content in 300 words
Content:{text}
"""
#NOW WE WILL DEFINE OUR PROMPT 
prompt=PromptTemplate(template=prompt_template,input_variable=['text'])
with st.sidebar:
    groq_api_key=st.text_input("Groq Api key",value="",type="password")


genric_url=st.text_input("URL",label_visibility="collapsed")
if st.button("Summarize content from YT or websites"):
    if not groq_api_key.strip() or not genric_url.strip():
        st.error("Please provide the info. guys")
    elif not validators.url(genric_url):
        st.error("Please enter valid URL.")

    else:
        try:
            with st.spinner("abhi krke deta hu"):
                if "youtube.com" in genric_url:
                    loader=YoutubeLoader.from_youtube_url(genric_url,add_video_info=True)
                else:
                    loader=UnstructuredURLLoader([genric_url],ssl_verify=False,loader=UnstructuredURLLoader(urls=[genric_url],ssl_verify=False,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}))
                    
                docs=loader.load()
                #now we will create chain for summarization
                chain=load_summarize_chain(llm,chain_type='stuff',prompt=prompt)
                output_summary=chain.run(docs)
                st.success(output_summary)

        except Exception as e:
            st.exception(f"Exception:{e}")


        









