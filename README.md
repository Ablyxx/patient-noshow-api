# Smart Healthcare No-Show Predictor API

This repository contains the machine learning inference API for a medical appointment no-show prediction system. It is deployed as a public REST API via Render and designed to be integrated into an automated n8n agentic workflow.

## Project Architecture
- **Machine Learning:** A size-constrained Random Forest Classifier trained on imbalanced healthcare data (SMOTE applied).
- **Serialization:** The model is compressed and exported using `joblib`.
- **API Framework:** FastAPI provides a fast, robust REST interface with Pydantic data validation.
- **Hosting:** Deployed via Render as a live web service.

## Live API Endpoint
The API is live and can be tested interactively via the Swagger UI interface:
**[Live API URL pending Render deployment]/docs**

## How to Use
Send a `POST` request to `/predict` with the following JSON payload structure:

```json
{
  "Gender": "F",
  "Age": 45,
  "Neighbourhood": "JARDIM DA PENHA",
  "Scholarship": 0,
  "Hipertension": 1,
  "Diabetes": 0,
  "Alcoholism": 0,
  "Handcap": 0,
  "SMS_received": 1,
  "Wait_days": 12,
  "historical_no_show_rate": 0.2
```

## Expected Response
```json
{
  "prediction": 1,
  "no_show_probability": 0.76,
  "risk_status": "High Risk of No-Show"
}
```

## Local Setup
To run this API locally:
1. Clone the repository.
2. Install the dependencies: pip install -r requirements.txt
3. Start the server: uvicorn main:app --reload