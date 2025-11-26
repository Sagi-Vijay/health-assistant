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

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Chat", "Symptom Analysis"])

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
                    response = requests.post(
                        f"{API_URL}/chat", 
                        json={"session_id": "streamlit_user", "message": prompt}
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
                    # 1. Analyze Symptoms
                    analysis_res = requests.post(
                        f"{API_URL}/analyze_symptoms",
                        json={"user_input": user_input}
                    )
                    
                    if analysis_res.status_code == 200:
                        analysis_data = analysis_res.json()
                        st.subheader("Extracted Symptoms")
                        st.write(analysis_data)
                        
                        # 2. Get Diagnosis Suggestion
                        st.subheader("Possible Conditions (AI Generated)")
                        diag_res = requests.post(
                            f"{API_URL}/diagnose",
                            json={"user_input": user_input}
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
