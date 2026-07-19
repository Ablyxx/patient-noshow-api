import streamlit as st
import requests

st.set_page_config(page_title="Smart Healthcare Agent", layout="centered")

st.title("Patient No-Show Predictor & AI Agent")
st.write("Enter patient details to predict attendance and generate an intervention strategy.")

# 1. User Inputs
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Patient Age", min_value=0, max_value=120, value=45)
    wait_days = st.number_input("Days Waited", min_value=0, max_value=200, value=12)
with col2:
    gender = st.selectbox("Gender", ["M", "F"])
    historical_rate = st.slider("Historical No-Show Rate", 0.0, 1.0, 0.2)

# 2. Trigger Workflow
if st.button("Analyze Patient Risk"):
    with st.spinner("AI Agent is evaluating risk and drafting strategy..."):
        
        # Prepare the payload
        payload = {
            "Age": age,
            "Wait_days": wait_days,
            "Gender": gender,
            "historical_no_show_rate": historical_rate,
            # Add all other variables your FastAPI expects (Scholarship, Hipertension, etc.)
            "Neighbourhood": "JARDIM DA PENHA", 
            "Scholarship": 0, "Hipertension": 1, "Diabetes": 0, 
            "Alcoholism": 0, "Handcap": 0, "SMS_received": 1
        }
        
        N8N_WEBHOOK_URL = "https://ablyx.app.n8n.cloud/webhook/evaluate-patient"
        
        try:
            # Send to n8n
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                
                # 3. Display Results
                st.success("Analysis Complete!")
                
                # Display the AI's response (Adjust these keys based on exactly what your LLM outputs)
                st.subheader("Agent Output:")
                st.write(result.get('output', 'No response generated.'))
                
            else:
                st.error(f"Error {response.status_code} from n8n.")
        except Exception as e:
            st.error(f"Failed to connect to n8n: {e}")