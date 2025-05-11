import os
import streamlit as st
from dotenv import load_dotenv
from langchain.llms import Cohere
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
# Load environment variables from .env file
load_dotenv(dotenv_path=r"C:\Users\swapn\Kaggle Practice\.env")

# Get the key from the environment
cohere_api_key = os.getenv("COHERE_API_KEY")

st.logo('streamlit_logo.png')
st.image('chatbot.jpg')

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_question_asked" not in st.session_state:
    st.session_state.last_question_asked = ""

if "show_follow_up_input" not in st.session_state:
    st.session_state.show_follow_up_input = False

if "most_recent_input" not in st.session_state:
    st.session_state.most_recent_input = []


# Clear chat callback
def clear_chat():
    st.session_state["styled_input"] = ""
    st.session_state["follow_up_input"] = ""
    st.session_state.chat_history = []
    st.session_state.most_recent_input = []
    st.session_state.last_question_asked = ""
    st.session_state.show_follow_up_input = False
#appapp-5q5c4fs2vt2ctigtcvtcve.streamlit.app -- generated on streamlit deployment page
    
# Initialize LLM + memory
llm = Cohere(cohere_api_key=cohere_api_key, temperature=0)
print("Using Cohere model:", llm.model)
memory = ConversationBufferMemory(return_messages=False)
conversation = ConversationChain(llm=llm, memory=memory)

# User input for first question
text_input = st.text_input("",placeholder = "Need help? Ask me",key='styled_input', label_visibility='collapsed')

# Only respond if it's a new question
if text_input and text_input != st.session_state.last_question_asked:
    with st.spinner("Please wait.."):
        response = conversation.run(text_input)
        st.session_state.chat_history.append(('You', text_input))
        st.session_state.chat_history.append(('Response', response))
        st.session_state.last_question_asked = text_input

# Display chat history if response is ready

for speaker, message in st.session_state.chat_history:
    st.markdown(f"***{speaker}:** {message}")

if st.session_state.chat_history:
    st.markdown("---")
    
    st.subheader("How satisfied are you with this conversation?")
    st.slider(
        "Rate from 1 (Not Satisfied) to 5 (Satisfied)",
        min_value=1,
        max_value=5,
        key="rating_scale"
    )
    
    if st.button("Next Question :question: "):
        st.session_state.show_follow_up_input = True

    # Show follow-up input field if allowed
    if st.session_state.show_follow_up_input:
        follow_up = st.text_input("Ask another question/Follow-up question?", key="follow_up_input")
        if follow_up and follow_up != st.session_state.last_question_asked:
            with st.spinner("Please wait.."):
                response_new = conversation.run(follow_up)
                st.session_state.chat_history.append(("You", follow_up))
                st.session_state.chat_history.append(("Response", response_new))
                st.session_state.most_recent_input.append(("You", follow_up))
                st.session_state.most_recent_input.append(("Response", response_new))
                st.session_state.last_question_asked = follow_up
            for speaker_, message_ in st.session_state.most_recent_input:
                st.markdown(f"***{speaker_}:** {message_}")


if st.session_state.chat_history or st.session_state.most_recent_input:
    # Add Clear Chat button BEFORE text_input widgets
    if st.button(" Clear Chat :wastebasket:", on_click=clear_chat):
    
        # Input after clear button
        text_input = st.text_input(
            "", 
            placeholder="Need help? Ask me", 
            key="styled_input", 
            label_visibility="collapsed"
        )