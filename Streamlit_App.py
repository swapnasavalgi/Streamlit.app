import os
import streamlit as st
from dotenv import load_dotenv
from langchain_cohere import CohereRagRetriever, ChatCohere
from langchain.retrievers import WikipediaRetriever
from langchain.llms import Cohere
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import datetime
# Load environment variables from .env file
#load_dotenv(dotenv_path=r"C:\Users\swapn\Kaggle Practice\.env")

load_dotenv()
# Get the key from the environment
cohere_api_key = os.getenv("COHERE_API_KEY")



st.logo('streamlit_logo.png')
st.image('AI-Chat-Mobile-Thumbnail.png',width=600)

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "multi_language_response" not in st.session_state:
    st.session_state.multi_language_response = []

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
    st.session_state["multi_language"] = ""
    st.session_state.chat_history = []
    st.session_state.most_recent_input = []
    st.session_state.multi_language_response=[]
    st.session_state.last_question_asked = ""
    st.session_state.show_follow_up_input = False


prompt1 = PromptTemplate(
    input_variables = ["history","input"],
    template = """

    You are a helpful assistant. Generate the response for the questions asked. 
    Also, if asked in multi languages other than English such as French, Spanish, Italian, German, Portuguese, Japanese, Korean, Chinese, Arabic, Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, Persian,
    then ask them to select desired languages from the dropdown.
    You :{input}
    Response:
    Translated in English : 
    """
)

prompt2 = PromptTemplate(
    input_variables = ["history","input"],
    template = """

    You are a helpful assistant. Generate the response for the questions asked. 
    Also, if asked in multi languages other than English such as French, Spanish, Italian, German, Portuguese, Japanese, Korean, Chinese, Arabic, Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew, Persian,
    then provide answer in multi languages .As well as translate it to English, only if asked in multi languages.

    You :{input}
    Response:
    Translated in English : 
    """
)

prompt3 = PromptTemplate(
    input_variables = ["history","input"],
    template = """

    You are a helpful assistant.If user is asking a follow up question by clicking 'Next Question' Button,  
    then generate the follow up response and continue the conversation based on the chat history or original question.

    You :{input}
    Response:
    """
)

# Initialize LLM + memory
llm = ChatCohere(
    cohere_api_key= cohere_api_key, model="command-a-03-2025",temperature=0.3,max_tokens = 500)
# print("Using Cohere model:", llm.model)
memory = ConversationBufferMemory(return_messages=False)
# print(memory.buffer)
conversation_user_input = LLMChain(llm=llm,prompt=prompt1,memory=memory)
conversation_multi_lang = LLMChain(llm=llm,prompt=prompt2,memory=memory)
conversation_follow_up = LLMChain(llm=llm, prompt=prompt3, memory=memory)

#Create a unique id for each language
languages = {
    'English' :1,
    'French':2, 'Spanish':3, 'Italian':4, 'German':5, 'Portuguese':6, 'Japanese':7, 'Korean':8, 'Chinese':9, 'Arabic':10, 'Russian':11, 'Polish':12, 'Turkish':13, 'Vietnamese':14, 'Dutch':15, 'Czech':16, 'Indonesian':17, 'Ukrainian':18, 'Romanian':19, 'Greek':20, 'Hindi':21, 'Hebrew':22, 'Persian':23   
}


#Select language options from the dropdown menu
option = st.selectbox(
    "Preferred Language",
       list(languages.keys()),
    index=None,
)

if option =='English':
    language_id = languages[option]#get unique id for language English
    # User input for first question
    text_input = st.text_input("",placeholder = "Need help? Ask me",key='styled_input', label_visibility='collapsed')


    # Only respond if it's a new question
    if text_input and text_input != st.session_state.last_question_asked:
        with st.spinner("Please wait.."):
            response = conversation_user_input.run(text_input)
            st.session_state.chat_history.append(('You', text_input))
            st.session_state.chat_history.append(('Response', response))
            st.session_state.last_question_asked = text_input
    
    # Display chat history if response is ready
    
    for speaker, message in st.session_state.chat_history:
        st.markdown(f"***{speaker}:** {message}")
    
    if st.session_state.chat_history:
        st.markdown("---")
        
        st.subheader("How satisfied are you with this conversation?")
        rating = st.slider(
            "Rate from 1 (Not Satisfied) to 5 (Satisfied)",
            min_value=1,
            max_value=5,
            key="rating_scale"
        )
       
        st.download_button(
            label = "Download :arrow_down:",
            data=message,
            file_name='chat_history.txt',
            mime = 'text/plain',
            type='primary')
            
        if st.button("Next Question :question: ", type='primary'):
            st.session_state.show_follow_up_input = True
    
        # Show follow-up input field if allowed
        if st.session_state.show_follow_up_input:
            follow_up = st.text_input("Ask another question/Follow-up question?", key="follow_up_input")
            if follow_up and follow_up != st.session_state.last_question_asked:
                with st.spinner("Please wait.."):
                    response_new = conversation_follow_up.run(follow_up)
                    st.session_state.chat_history.append(("You", follow_up))
                    st.session_state.chat_history.append(("Response", response_new))
                    st.session_state.most_recent_input.append(("You", follow_up))
                    st.session_state.most_recent_input.append(("Response", response_new))
                    st.session_state.last_question_asked = follow_up
        if st.session_state.most_recent_input:
                    with st.expander(label = 'Expland me',expanded=False):
                        for speaker_, message_ in st.session_state.most_recent_input:
                            st.markdown(f"***{speaker_}:** {message_}")
                
        if st.session_state.chat_history or st.session_state.most_recent_input:
            # Add Clear Chat button BEFORE text_input widgets
            if st.button(" Clear Chat :wastebasket:", on_click=clear_chat,type='primary'):
            
                # Input after clear button
                text_input = st.text_input(
                    "", 
                    placeholder="Need help? Ask me", 
                    key="styled_input", 
                    label_visibility="collapsed"
                )
elif option :
    languages_id_for_multi = languages[option]
    text_input_for_multi = st.text_input("",
        placeholder = 'Ask me in the selected language',
        key = 'multi_language',
        label_visibility= 'collapsed'
    )
    if text_input_for_multi and text_input_for_multi != st.session_state.last_question_asked:
        with st.spinner("Please wait..."):
            response_for_multi = conversation_multi_lang.run(text_input_for_multi)
            st.session_state.multi_language_response.append(("You",text_input_for_multi))
            st.session_state.multi_language_response.append(("Response",response_for_multi))
            st.session_state.last_question_asked = text_input_for_multi

        # Display chat history if response is ready
    
    for speaker, message in st.session_state.multi_language_response:
        st.markdown(f"***{speaker}:** {message}")
    
    if st.session_state.multi_language_response:
        st.markdown("---")
        
        st.subheader("How satisfied are you with this conversation?")
        rating = st.slider(
            "Rate from 1 (Not Satisfied) to 5 (Satisfied)",
            min_value=1,
            max_value=5,
            key="rating_scale_for_multi"
        )

        st.download_button(
            label = "Download :arrow_down:",
            data = message,
            file_name = 'chat_history.txt',
            mime= 'text/plain',
            type='primary')
            
       
        if st.button(" Clear Chat :wastebasket:", on_click = clear_chat,type='primary'):
            text_input_for_multi = st.text_input(
                "",
                placeholder = 'Ask me in the selected language',
                key = 'multi_language',
                label_visibility = 'collapsed')


     #Chatbot Arena or Writing bench for model evaluation   
                