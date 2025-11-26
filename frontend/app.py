import streamlit as st
import requests
import json

# Backend URL
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Health Assistant AI", page_icon="🩺", layout="wide")

st.title("🩺 AI Health Assistant")
st.markdown("""
**Disclaimer:** This AI is for informational purposes only and does NOT provide medical advice, diagnosis, or treatment. 
Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
""")

# Session state for auth
if "token" not in st.session_state:
    st.session_state.token = None

# Sidebar
st.sidebar.header("Navigation")

if not st.session_state.token:
    st.sidebar.warning("Please Log In")
    auth_mode = st.sidebar.radio("Auth", ["Login", "Signup"])
    
    if auth_mode == "Login":
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            try:
                res = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
                if res.status_code == 200:
                    st.session_state.token = res.json()["access_token"]
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            except Exception as e:
                st.error(f"Error: {e}")
                
    elif auth_mode == "Signup":
        st.header("Signup")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        if st.button("Signup"):
            try:
                res = requests.post(f"{API_URL}/signup", json={"username": new_user, "password": new_pass})
                if res.status_code == 200:
                    st.success("Account created! Please log in.")
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.stop() # Stop execution if not logged in

if st.sidebar.button("Logout"):
    st.session_state.token = None
    st.rerun()

page = st.sidebar.radio("Go to", ["Chat", "Symptom Analysis", "History"])

if page == "Chat":
    st.header("Medical Chat Assistant")
    
    # Session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a health-related question..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call Backend
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.token}"}
                    response = requests.post(
                        f"{API_URL}/chat", 
                        json={"session_id": "streamlit_user", "message": prompt},
                        headers=headers
                    )
                    if response.status_code == 200:
                        data = response.json()
                        ai_response = data["response"]
                        st.markdown(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

elif page == "Symptom Analysis":
    st.header("Symptom Analyzer")
    
    user_input = st.text_area("Describe your symptoms in detail:", height=150)
    
    if st.button("Analyze"):
        if user_input:
            with st.spinner("Analyzing symptoms..."):
                try:
                    headers = {"Authorization": f"Bearer {st.session_state.token}"}
                    # 1. Analyze Symptoms
                    analysis_res = requests.post(
                        f"{API_URL}/analyze_symptoms",
                        json={"user_input": user_input},
                        headers=headers
                    )
                    
                    if analysis_res.status_code == 200:
                        analysis_data = analysis_res.json()
                        st.subheader("Extracted Symptoms")
                        st.write(analysis_data)
                        
                        # 2. Get Diagnosis Suggestion
                        st.subheader("Possible Conditions (AI Generated)")
                        diag_res = requests.post(
                            f"{API_URL}/diagnose",
                            json={"user_input": user_input},
                            headers=headers
                        )
                        if diag_res.status_code == 200:
                            diag_data = diag_res.json()
                            st.markdown(diag_data["diagnosis_suggestion"])
                        else:
                            st.error("Failed to get diagnosis suggestion.")
                    else:
                        st.error("Failed to analyze symptoms.")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
        else:
            st.warning("Please enter your symptoms.")

elif page == "History":
    st.header("Your Medical History")
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        res = requests.get(f"{API_URL}/history", headers=headers)
        
        if res.status_code == 200:
            interactions = res.json()
            if not interactions:
                st.info("No history found.")
            else:
                for item in interactions:
                    with st.expander(f"{item['timestamp']} - {item['user_query'][:50]}..."):
                        st.markdown(f"**Query:** {item['user_query']}")
                        st.markdown(f"**AI Response:** {item['llm_response']}")
        else:
            st.error("Failed to fetch history.")
    except Exception as e:
        st.error(f"Error: {e}")
