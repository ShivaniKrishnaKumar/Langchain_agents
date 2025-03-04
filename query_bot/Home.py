import streamlit as st
from langchain_core.messages import HumanMessage
from utils.agents import run_agent

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role" : "ai", "content" : "Hi, how can I help you?"}
    ]

if "chat_history" not in st.session_state.keys():
    st.session_state.chat_history = []


st.set_page_config(
    page_title="MedBot",
    layout="wide"
)

st.title("NOVA welcomes you, 👋", anchor=False)

main_con = st.container(
    height=500,
)

prompt_con = st.container(
    height=70,
    border=False
)

chat_con = main_con.container(
    height=465
)

with prompt_con:
    prompt = st.chat_input(
                "Chat with MedBot..."
            )

with chat_con:
    for message in st.session_state.messages:
        st.chat_message(
            name=message["role"]      
        ).markdown(message["content"])

    if prompt:
        st.chat_message(
            "user"
        ).markdown(prompt)

        #Chatbot processing
        agent_response = run_agent(prompt)
        st.chat_message(
            "ai"
        ).markdown(agent_response)

        # st.session_state.chat_history.extend([HumanMessage(content=prompt), agent_response["answer"]])

        st.session_state.messages.append(
            {"role" : "human", "content" : prompt}
        )
        st.session_state.messages.append(
            {"role" : "ai", "content" : agent_response}
        )





