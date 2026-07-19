import streamlit as st
import requests

st.set_page_config(page_title="Smart Healthcare Agent", layout="centered")
st.title("Patient No-Show Predictor & AI Agent")

# 1. User Inputs
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Patient Age", min_value=0, max_value=120, value=45)
    wait_days = st.number_input("Days Waited", min_value=0, max_value=200, value=12)
    phone_number = st.text_input("Patient Phone Number (e.g., +60123456789)")
with col2:
    gender = st.selectbox("Gender", ["M", "F"])
    historical_rate = st.slider("Historical No-Show Rate", 0.0, 1.0, 0.2)

if st.button("Analyze & Automate Outreach"):
    if not phone_number:
        st.warning("Please enter a phone number to enable automated WhatsApp outreach.")
    else:
        with st.spinner("AI Agent is evaluating risk and dispatching WhatsApp message..."):

            payload = {
                "Age": age,
                "Wait_days": wait_days,
                "Gender": gender,
                "historical_no_show_rate": historical_rate,
                "Phone": phone_number,
                "Neighbourhood": "JARDIM DA PENHA",
                "Scholarship": 0, "Hipertension": 1, "Diabetes": 0,
                "Alcoholism": 0, "Handcap": 0, "SMS_received": 1
            }

            # Production webhook URL (workflow must be published/active)
            N8N_WEBHOOK_URL = "https://ablyx.app.n8n.cloud/webhook/evaluate-patient"

            try:
                response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=60)

                if response.status_code == 200:
                    result = response.json()

                    st.success("Analysis Complete & WhatsApp Message Dispatched!")

                    # n8n returns:
                    # {
                    #   "status": "success",
                    #   "drafted_message": {
                    #       "risk_tier": "...",
                    #       "recommended_strategy": "...",
                    #       "draft_message": "..."   <-- the patient-facing text
                    #   }
                    # }
                    agent_output = result.get("drafted_message", {})

                    # Guard in case n8n ever returns a plain string instead of an object
                    if isinstance(agent_output, dict):
                        dispatched_text = agent_output.get(
                            "draft_message", "No message text returned by n8n."
                        )
                        risk_tier = agent_output.get("risk_tier", "N/A")
                        strategy = agent_output.get("recommended_strategy", "N/A")
                    else:
                        dispatched_text = str(agent_output)
                        risk_tier = "N/A"
                        strategy = "N/A"

                    st.subheader("Message Delivered to Patient:")
                    st.info(dispatched_text)

                    with st.expander("Internal Risk Assessment"):
                        st.write(f"**Risk tier:** {risk_tier}")
                        st.write(f"**Recommended strategy:** {strategy}")

                else:
                    st.error(f"Failed to trigger workflow. Error {response.status_code}")
                    st.caption(response.text)  # surface n8n's error body for debugging

            except Exception as e:
                st.error(f"Failed to connect to n8n: {e}")