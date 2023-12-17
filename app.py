import streamlit as st
import openai
client = openai.OpenAI(api_key=st.secrets.openai_key)

st.header("Chat with a Revenue Growth Manager 💬 📚")

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
                                {"role": "assistant", 
                                 "content": "Ask me a question about RGM for your CPG company..."}
                                ]

with open("examples.txt", "r") as f:
    examples = f.read()

def system_prompt_template(examples):
    prompt = f"""consider the examples delimited with triple backticks and\
        answer the followeing question in the same manner:
        ```
        {examples}
        ```
        """
    return prompt

# st.session_state.messages.append({"role": "system", "content": system_prompt_template(examples)})

question = st.chat_input("Your question...")
if question: # prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": question})

for message in st.session_state.messages: # display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            prompt = system_prompt_template(examples) + "\n\n" + f"Question: {question}" + "\n" + "Answer: "
            response = client.completions.create(model='gpt-3.5-turbo-instruct', 
                                                 prompt=prompt, 
                                                 temperature=0, 
                                                 max_tokens=100)
            response = response.choices[0].text
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message) # add response to message history
            # examples += "\n\n" + question + "\n" + response
