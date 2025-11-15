from flask import Flask, request, render_template, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/catboost_telco_churn.pkl")
DATA_PATH = os.path.join(BASE_DIR, "../dataset/feature_engineered_telco.csv")

# load model and data
model = joblib.load(MODEL_PATH)
data = pd.read_csv(DATA_PATH)

# home page
@app.route('/')
def home():
    return render_template('CatBoost.html')

# prediction endpoint
@app.route('/predict')
def predict():
    customer_id = request.args.get('customerID')

    # check if customer exists
    if customer_id not in data['customerID'].astype(str).values:
        return jsonify({'error': 'Customer ID not found'})

    # select customer row
    customer_row = data[data['customerID'].astype(str) == customer_id].drop(
        ['customerID', 'Churn', 'Churn_encoded'], axis=1
    )

    # match model feature order
    customer_row = customer_row.reindex(columns=model.feature_names_, fill_value=0)

    # get prediction
    prediction = model.predict(customer_row)[0]
    probability = model.predict_proba(customer_row)[0][1]

    return jsonify({
        'customerID': customer_id,
        'prediction': 'Yes' if prediction == 1 else 'No',
        'probability': round(probability, 3)
    })

# run server
if __name__ == '__main__':
    app.run(debug=True)
