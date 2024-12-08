from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the pre-trained model
with open(r"C:\Users\MOUNISHA\Downloads\CustomerChurnPrediction\gradient_boosting_model.pkl", "rb") as f:
    model = pickle.load(f)

# Home route to display the HTML form
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route to handle form submission
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract form data
        form_data = request.form

        # Convert form data into a DataFrame (adjust the column order and types as needed)
        input_data = pd.DataFrame([{
            "gender": 1 if form_data["gender"] == "Female" else 0,
            "SeniorCitizen": int(form_data["SeniorCitizen"]),
            "Partner": 1 if form_data["Partner"] == "Yes" else 0,
            "Dependents": 1 if form_data["Dependents"] == "Yes" else 0,
            "tenure": float(form_data["tenure"]),
            "PhoneService": 1 if form_data["PhoneService"] == "Yes" else 0,
            "MultipleLines": 1 if form_data["MultipleLines"] == "Yes" else 0,
            "InternetService": 1 if form_data["InternetService"] == "DSL" else 0,
            "OnlineSecurity": 1 if form_data["OnlineSecurity"] == "Yes" else 0,
            "OnlineBackup": 1 if form_data["OnlineBackup"] == "Yes" else 0,
            "DeviceProtection": 1 if form_data["DeviceProtection"] == "Yes" else 0,
            "TechSupport": 1 if form_data["TechSupport"] == "Yes" else 0,
            "StreamingTV": 1 if form_data["StreamingTV"] == "Yes" else 0,
            "StreamingMovies": 1 if form_data["StreamingMovies"] == "Yes" else 0,
            "Contract": 1 if form_data["Contract"] == "Month-to-month" else 0,
            "PaperlessBilling": 1 if form_data["PaperlessBilling"] == "Yes" else 0,
            "PaymentMethod": 1 if form_data["PaymentMethod"] == "Electronic check" else 0,
            "MonthlyCharges": float(form_data["MonthlyCharges"]),
            "TotalCharges": float(form_data["TotalCharges"]),
        }])

        # Make a prediction
        prediction = model.predict(input_data)

        # Render prediction result
        return render_template('result.html', prediction=prediction[0])

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
