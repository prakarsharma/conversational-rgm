import streamlit as st
import openai
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, llms, memory

openai.api_key = st.secrets.openai_key
st.header("Chat with a Revenue Growth Manager 💬 📚")

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
                                {"role": "assistant", 
                                 "content": "Ask me a question RGM for your CPG company..."}
                                ]

@st.cache_resource(show_spinner=False)
def load_and_index():
    sys_prom = """You are an expert on Revenue Growth Management (RGM).
    Your job is to answer questions on RGM.
    Assume that all questions are related to RGM.
    Answers based on facts only."""
    llm = llms.OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt=sys_prom)
    with st.spinner(text="Loading and indexing the documentation..."):
        reader = SimpleDirectoryReader(input_dir="./docs", recursive=True)
        docs = reader.load_data()
        sc = ServiceContext.from_defaults(llm=llm)
        index = VectorStoreIndex.from_documents(docs, service_context=sc)
        return index

index = load_and_index()

mode = "condense_question"
# mode = "context"
max_token = 1500
mem = memory.ChatMemoryBuffer.from_defaults(token_limit=1500)
chat_engine = index.as_chat_engine(chat_mode=mode, memory=mem, verbose=True)

prompt = st.chat_input("Your question...")
if prompt: # prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # add response to message history
