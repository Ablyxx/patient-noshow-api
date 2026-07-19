from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Initialize the FastAPI App
app = FastAPI(title="Smart Healthcare No-Show Predictor API")

# Load the trained model artifact
model = joblib.load("missed_appointment_model.joblib")

# Define the incoming data schema (Raw format before One-Hot Encoding)
class PatientData(BaseModel):
    Gender: str
    Age: int
    Neighbourhood: str
    Scholarship: int
    Hipertension: int
    Diabetes: int
    Alcoholism: int
    Handcap: int
    SMS_received: int
    Wait_days: int
    historical_no_show_rate: float

# Create the Prediction Endpoint
@app.post("/predict")
def predict_no_show(data: PatientData):
    # Convert incoming JSON data into a Pandas DataFrame
    input_df = pd.DataFrame([data.dict()])
    
    # Apply one-hot encoding (This creates 'Gender_M', 'Neighbourhood_JARDIM...', etc.)
    input_encoded = pd.get_dummies(input_df)
    
    # --- THE MAGIC ALIGNMENT TRICK ---
    # Scikit-learn models remember the exact columns they were trained on in 'feature_names_in_'
    # We force the new dataframe to match these columns exactly. 
    # Missing columns (neighbourhoods the patient isn't from) are automatically filled with 0!
    expected_columns = model.feature_names_in_
    input_aligned = input_encoded.reindex(columns=expected_columns, fill_value=0)
    
    # Generate Prediction and Probability
    prediction = model.predict(input_aligned)[0]
    probabilities = model.predict_proba(input_aligned)[0]
    
    # Probability of Class 1 (Missed Appointment)
    no_show_prob = probabilities[1] 

    return {
        "prediction": int(prediction),
        "no_show_probability": float(no_show_prob),
        "risk_status": "High Risk of No-Show" if prediction == 1 else "Likely to Attend"
    }
    