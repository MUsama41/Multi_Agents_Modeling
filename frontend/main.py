import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(page_title="Rasha AI Agents Research", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main { background-color: #f0f2f6; }
    .stButton>button {
        border-radius: 20px;
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #357ABD;
        transform: translateY(-2px);
    }
    .card {
        padding: 2rem;
        border-radius: 15px;
        background: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def init_session():
    if "user_id" not in st.session_state:
        try:
            res = requests.post(f"{BACKEND_URL}/api/user/create")
            st.session_state.user_id = res.json()["user_id"]
        except:
            st.session_state.user_id = "TEMP_USER"
    if "step" not in st.session_state:
        st.session_state.step = "consent"
    if "agent" not in st.session_state:
        st.session_state.agent = "Informational"

def main():
    init_session()
    
    with st.sidebar:
        st.title("Settings")
        st.info(f"User ID: {st.session_state.user_id}")
        if st.button("Reset Session"):
            st.session_state.clear()
            st.rerun()

    if st.session_state.step == "consent":
        display_consent()
    elif st.session_state.step == "instruction":
        display_instruction()
    elif st.session_state.step == "interaction":
        display_interaction()
    elif st.session_state.step == "survey":
        display_survey()

def display_consent():
    st.title("Informed Consent Form")
    with st.container():
        st.markdown("""
        <div class="card">
            <h3>Purpose of the Research</h3>
            <p>We are conducting research to understand how AI managers affect workers. 
            Your participation is voluntary and anonymous.</p>
            <p>By clicking "I Agree", you consent to participate in this study.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("I Agree"):
            st.session_state.step = "instruction"
            st.rerun()

def display_instruction():
    st.title("Instructions")
    st.markdown("""
    <div class="card">
        <p>You will be assigned an AI manager to help you with a freelancing task.</p>
        <p>Please interact with the agent as you would in a real work scenario.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.agent = st.selectbox("Choose your AI Manager Type (for research testing):", 
                                        ["Informational", "Interpersonal", "Decision Making"])
    
    if st.button("Start Task"):
        st.session_state.step = "interaction"
        st.rerun()

def display_interaction():
    agent_type = st.session_state.agent
    st.title(f"Task with {agent_type} Agent")
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if agent_type == "Informational":
            question = st.text_input("What would you like to ask your manager?")
            if st.button("Submit"):
                handle_agent_call("informational", {"question": question})
        
        elif agent_type == "Interpersonal":
            idea = st.text_area("Share your idea with your manager:")
            if st.button("Share"):
                handle_agent_call("interpersonal", {"idea": idea})
        
        elif agent_type == "Decision Making":
            idea = st.text_area("Submit your idea for evaluation:")
            if st.button("Evaluate"):
                handle_agent_call("decision-making", {"idea": idea})
        st.markdown('</div>', unsafe_allow_html=True)

    if "last_response" in st.session_state:
        st.markdown(f'<div class="card"><h4>Manager Response:</h4><p>{st.session_state.last_response}</p></div>', unsafe_allow_html=True)
        if st.button("Proceed to Survey"):
            st.session_state.step = "survey"
            st.rerun()

def handle_agent_call(endpoint, payload):
    with st.spinner("Communicating with agent..."):
        try:
            res = requests.post(f"{BACKEND_URL}/api/agents/{endpoint}", json=payload)
            if res.status_code == 200:
                data = res.json()
                st.session_state.last_response = data["response"]
                # Save to DB
                requests.post(f"{BACKEND_URL}/api/idea/update/{st.session_state.user_id}", 
                             json={"main_idea": payload.get("idea", payload.get("question")), 
                                   "agent_name": endpoint})
            else:
                st.error("Error from backend")
        except:
            st.error("Connection failed")

def display_survey():
    st.title("Final Step: Survey")
    if "unique_num" not in st.session_state:
        res = requests.post(f"{BACKEND_URL}/api/utils/generate-number")
        st.session_state.unique_num = res.json()["number"]
        requests.post(f"{BACKEND_URL}/api/idea/update/{st.session_state.user_id}", 
                     json={"generative_num": st.session_state.unique_num})

    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <h2>Your Unique Survey Code:</h2>
        <h1 style="color:#4A90E2;">{st.session_state.unique_num}</h1>
        <p>Please enter this code in the Qualtrics survey.</p>
        <a href="https://umich.qualtrics.com/jfe/form/SV_dipJksYhpyJOnTo" target="_blank">
            <button style="padding:10px 20px; border-radius:5px; background:#4A90E2; color:white; border:none; cursor:pointer;">
                Go to Qualtrics Survey
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
