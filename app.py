from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the trained MultinomialNB model and vectorizer
# Ensure 'model.pkl' and 'vectorizer.pkl' are placed in the same directory
try:
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
except Exception as e:
    print(f"Error loading model or vectorizer: {e}")

@app.route('/')
def home():
    return "MultinomialNB Classifier API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Vectorize the input text and predict
        X = vectorizer.transform([text])
        prediction = model.predict(X)[0]
        confidence = float(model.predict_proba(X).max())
        
        return jsonify({
            'prediction': str(prediction),
            'confidence': confidence
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
