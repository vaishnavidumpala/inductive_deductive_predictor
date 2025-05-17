from flask import Flask, request, jsonify
import pickle
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model, preprocessor, and encoder
with open('D:/inductive_deductive/backend/model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('D:/inductive_deductive/backend/preprocessor.pkl', 'rb') as f:
    preprocessor = pickle.load(f)

with open('D:/inductive_deductive/backend/encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)

score_map = {'Never': 1, 'Sometimes': 2, 'Usually': 3, 'Always': 4}
feature_names = [
    'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8',
    'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14',
    'inductive_score', 'deductive_score'
]

def calculate_scores(numeric_answers):
    inductive_indices = [0, 2, 4, 6, 8, 9, 12]
    deductive_indices = [1, 3, 5, 7, 10, 11, 13]
    inductive_score = sum(numeric_answers[i] for i in inductive_indices)
    deductive_score = sum(numeric_answers[i] for i in deductive_indices)
    return inductive_score, deductive_score


@app.route('/predict', methods=['POST'])
def predict():
    try:
        answers = request.json
        if not answers or len(answers) != 14:
            return jsonify({"error": "Invalid input. Please provide 14 answers."}), 400

        numeric_answers = [score_map.get(answers[f'Q{i+1}'], 0) for i in range(14)]
        inductive_score, deductive_score = calculate_scores(numeric_answers)

        input_data = numeric_answers + [inductive_score, deductive_score]
        input_df = pd.DataFrame([input_data], columns=feature_names)

        X_input = preprocessor.transform(input_df)
        predicted_index = model.predict(X_input)[0]
        predicted_label = encoder.inverse_transform([predicted_index])[0]

 # Calculate the percentage for Inductive and Deductive
        total_score = inductive_score + deductive_score
        inductive_percentage = (inductive_score / total_score) * 100 if total_score != 0 else 0
        deductive_percentage = (deductive_score / total_score) * 100 if total_score != 0 else 0

        return jsonify({
            "prediction": predicted_label,
            "inductive_percentage": round(inductive_percentage, 2),
            "deductive_percentage": round(deductive_percentage, 2)
        })
    
    except Exception as e:
        print("Error during prediction:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
