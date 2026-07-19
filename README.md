# 🏥 Smart Healthcare No-Show Predictor & Autonomous Agent
An end-to-end Agentic AI workflow designed to predict medical appointment no-shows and autonomously deploy personalized mitigation strategies via WhatsApp. 

## 📖 Project Overview
Missed medical appointments (no-shows) cost healthcare systems significant time and resources. This project solves this problem by moving beyond simple predictions. It employs an **Agentic AI Workflow** that perceives patient risk, reasons over the data to formulate a retention strategy, and takes autonomous action by messaging the patient.

This project was developed for **AIT403 (Advanced Data Analysis)** and fulfills the requirements for predictive model development, API deployment, and agentic AI orchestration.

## ⚙️ Architecture & Pipeline
This system follows a strict **Perceive → Reason → Act** agentic pipeline:

1. **The Frontend (Streamlit):** A dashboard for hospital administrators to input patient data and monitor AI actions.
2. **The Orchestrator (n8n):** The "brain" of the operation, managing the flow of data between the UI, the predictive model, the LLM, and the messaging API.
3. **The Predictor (FastAPI + Scikit-Learn):** A custom Machine Learning REST API hosted on Render. It calculates the statistical probability of a patient missing their appointment.
4. **The Reasoning Engine (Google Gemini):** An LLM integrated via n8n that evaluates the patient's profile (age, wait days) and the predicted risk to draft a personalized intervention strategy (e.g., offering telehealth or transport).
5. **The Action Mechanism (WhatsApp Cloud API):** Meta's API automatically dispatches the Gemini-drafted message directly to the patient's phone.

## 🛠️ Technology Stack
* **Machine Learning:** Python, Scikit-Learn, Pandas, Imbalanced-Learn (SMOTE), Joblib
* **API & Deployment:** FastAPI, Uvicorn, Pydantic, Render
* **Agentic Orchestration:** n8n (Webhook & HTTP nodes)
* **Generative AI:** Google Gemini (via n8n integration)
* **Frontend:** Streamlit, Streamlit Community Cloud
* **External Integrations:** Meta WhatsApp Cloud API

## 📊 Model Development Highlights
The predictive model is a size-constrained **Random Forest Classifier** (`n_estimators=75`, `max_depth=12`) trained on a public dataset of over 100,000 medical appointments in Brazil. 
* **Feature Engineering:** Extracted `Wait_days` from timestamps and engineered a robust `historical_no_show_rate` to capture patient behavior without data leakage.
* **Class Imbalance:** Applied **SMOTE** strictly to the training data to correct an 80/20 class imbalance, prioritizing high Recall for catching true no-shows.
* **Optimization:** Serialized via `joblib` with zlib compression to ensure the deployment artifact remains lightweight (under 20MB).

## 📂 Repository Structure
```text
├── Data Preparation, EDA, Predictive Model Development.ipynb  # Data wrangling, SMOTE, and ML training
├── main.py                                                    # FastAPI backend script
├── app.py                                                     # Streamlit frontend script
├── noshow_model.joblib                                        # Serialized Random Forest model
├── requirements.txt                                           # Python dependencies
└── README.md                                                  # Project documentation
```

## How To Run Locally
1. Clone the repository:
```Bash
git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
cd your-repo-name
```

2. Install dependencies:
```Bash
pip install -r requirements.txt
```

3. Start the FastAPI Backend:
```Bash
uvicorn main:app --reload
```

4. Start the Streamlit Frontend:
```Bash
streamlit run app.py
```

** Note: To test the full end-to-end pipeline, an active n8n instance with configured Gemini and WhatsApp credentials is required