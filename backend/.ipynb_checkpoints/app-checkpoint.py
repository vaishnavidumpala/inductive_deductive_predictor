from flask import Flask, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load your model and preprocessor
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
PREPROCESSOR_PATH = os.path.join(os.path.dirname(__file__), 'preprocessor.pkl')

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

with open(PREPROCESSOR_PATH, 'rb') as f:
    preprocessor = pickle.load(f)

# Mapping of answers to numerical values
score_map = {'Never': 1, 'Sometimes': 2, 'Usually': 3, 'Always': 4}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        answers = request.json  # Frontend sends JSON with answers, e.g., {Q1: 'Never', Q2: 'Usually', ...}

        
        if not answers or len(answers) != 14:
            return jsonify({"error": "Invalid input. Please provide 14 answers."}), 400

        # Calculate inductive and deductive scores
        inductive_indices = [0, 2, 4, 6, 8, 9, 12]
        deductive_indices = [1, 3, 5, 7, 10, 11, 13]

        # Map answer options to numeric scores
        score_map = {'Never': 1, 'Sometimes': 2, 'Usually': 3, 'Always': 4}
        numeric_answers = [score_map.get(ans, 0) for ans in answers]

        inductive_score = sum([numeric_answers[i] for i in inductive_indices])
        deductive_score = sum([numeric_answers[i] for i in deductive_indices])

        # Add scores to the input for prediction
        input_data = numeric_answers + [inductive_score, deductive_score]
        
        # Transform input using preprocessor (the one used during training)
        X_input = preprocessor.transform([input_data])

        # Make prediction and get class probabilities
        probabilities = model.predict_proba(X_input)[0]
        labels = model.classes_
        
        # Convert keys and values in proba_dict to native types (str, int, float)
        proba_dict = {str(label): round(float(prob), 2) for label, prob in zip(labels, probabilities)}

        # Get top 2 probabilities
        sorted_probs = sorted(proba_dict.items(), key=lambda x: x[1], reverse=True)
        top_label, top_confidence = sorted_probs[0]
        second_label, second_confidence = sorted_probs[1]

        # Threshold to decide "hybrid"
        if abs(top_confidence - second_confidence) < 10:
            prediction = "hybrid"
            confidence = round((top_confidence + second_confidence) / 2, 2)
        else:
            prediction = top_label
            confidence = top_confidence

        return jsonify({
            "prediction": prediction,
            "confidence": confidence,
            "proba": proba_dict
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(port=5000, debug=True)
