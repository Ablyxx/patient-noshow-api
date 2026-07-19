import requests

API_URL = "https://patient-noshow-api.onrender.com/predict"

# The patient data we want to predict
patient_data = {
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
}

# Send the POST request
print("Sending request to live API...")
response = requests.post(API_URL, json=patient_data)

# Print the result
if response.status_code == 200:
    print("✅ Success! API Response:")
    print(response.json())
else:
    print(f"❌ Error {response.status_code}: {response.text}")