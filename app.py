import os
import pickle
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Load the model/vectorizer from vector.pkl
MODEL_PATH = os.path.join(os.path.dirname(__file__), "vector.pkl")
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    model = None

# HTML Template with Solar System, Flying Stars, and Category Form
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cosmic Sentiment Analyzer</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: radial-gradient(ellipse at bottom, #1b2735 0%, #090a0f 100%);
            color: #ffffff;
            min-height: 100vh;
            overflow-x: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }

        /* Flying Stars Background Effect */
        .stars {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            background: transparent;
            z-index: 1;
        }
        .star {
            position: absolute;
            background: #ffffff;
            border-radius: 50%;
            animation: fly linear infinite;
        }
        @keyframes fly {
            from {
                transform: translateY(0px) scale(0.5);
                opacity: 0;
            }
            50% {
                opacity: 1;
            }
            to {
                transform: translateY(100vh) scale(1.2);
                opacity: 0;
            }
        }

        /* Solar System Background Effect */
        .solar-system {
            position: absolute;
            width: 100vw;
            height: 100vh;
            top: 0;
            left: 0;
            pointer-events: none;
            z-index: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            opacity: 0.35;
        }
        .sun {
            width: 80px;
            height: 80px;
            background: radial-gradient(circle, #ffcc00, #ff6600);
            border-radius: 50%;
            box-shadow: 0 0 50px #ff3300;
            position: absolute;
        }
        .orbit {
            position: absolute;
            border: 1px dashed rgba(255, 255, 255, 0.15);
            border-radius: 50%;
        }
        .planet {
            position: absolute;
            border-radius: 50%;
        }

        /* Orbit 1 */
        .orbit-1 { width: 200px; height: 200px; animation: spin 10s linear infinite; }
        .planet-1 { width: 12px; height: 12px; background: #00ffff; top: -6px; left: calc(50% - 6px); box-shadow: 0 0 10px #00ffff; }

        /* Orbit 2 */
        .orbit-2 { width: 350px; height: 350px; animation: spin 18s linear infinite reverse; }
        .planet-2 { width: 18px; height: 18px; background: #ff4757; top: -9px; left: calc(50% - 9px); box-shadow: 0 0 12px #ff4757; }

        /* Orbit 3 */
        .orbit-3 { width: 520px; height: 520px; animation: spin 25s linear infinite; }
        .planet-3 { width: 24px; height: 24px; background: #2ed573; top: -12px; left: calc(50% - 12px); box-shadow: 0 0 15px #2ed573; }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        /* UI Container */
        .container {
            position: relative;
            z-index: 2;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 16px;
            width: 100%;
            max-width: 480px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
            text-align: center;
        }
        h1 {
            margin-bottom: 20px;
            font-size: 26px;
            letter-spacing: 1px;
            color: #f1f2f6;
        }
        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-size: 14px;
            color: #a4b0be;
        }
        textarea, select {
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            background: rgba(0, 0, 0, 0.3);
            color: #fff;
            font-size: 15px;
            outline: none;
            transition: border-color 0.3s;
        }
        textarea:focus, select:focus {
            border-color: #00ffff;
        }
        button {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            background: linear-gradient(135deg, #00b4d8, #0077b6);
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 180, 216, 0.4);
        }
        .result {
            margin-top: 25px;
            padding: 15px;
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.4);
            font-size: 18px;
            font-weight: bold;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .positive { color: #2ed573; }
        .negative { color: #ff4757; }
    </style>
</head>
<body>

    <!-- Flying Stars Container -->
    <div class="stars" id="stars"></div>

    <!-- Solar System Background -->
    <div class="solar-system">
        <div class="sun"></div>
        <div class="orbit orbit-1"><div class="planet planet-1"></div></div>
        <div class="orbit orbit-2"><div class="planet planet-2"></div></div>
        <div class="orbit orbit-3"><div class="planet planet-3"></div></div>
    </div>

    <!-- Main UI Card -->
    <div class="container">
        <h1>Sentiment Analyzer</h1>
        <form method="POST">
            <div class="form-group">
                <label for="category">Select Domain / Category:</label>
                <select id="category" name="category">
                    <option value="general" style="background: #111;">General Review</option>
                    <option value="product" style="background: #111;">Product Feedback</option>
                    <option value="movie" style="background: #111;">Movie Review</option>
                </select>
            </div>

            <div class="form-group">
                <label for="text">Enter Text for Analysis:</label>
                <textarea id="text" name="text" rows="4" placeholder="Type your text here..." required>{{ user_text if user_text else '' }}</textarea>
            </div>
            
            <button type="submit">Predict Sentiment</button>
        </form>

        {% if prediction %}
        <div class="result">
            Prediction: <span class="{{ prediction | lower }}">{{ prediction }}</span>
        </div>
        {% endif %}
    </div>

    <script>
        // Generate Dynamic Flying Stars
        const starsContainer = document.getElementById('stars');
        const numStars = 60;
        for (let i = 0; i < numStars; i++) {
            const star = document.createElement('div');
            star.classList.add('star');
            const size = Math.random() * 3 + 1;
            star.style.width = `${size}px`;
            star.style.height = `${size}px`;
            star.style.left = `${Math.random() * 100}vw`;
            star.style.top = `${Math.random() * -100}vh`;
            star.style.animationDuration = `${Math.random() * 3 + 2}s`;
            star.style.animationDelay = `${Math.random() * 5}s`;
            starsContainer.appendChild(star);
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    user_text = ""
    if request.method == "POST":
        user_text = request.form.get("text")
        category = request.form.get("category") # Categorical form field captured
        
        if model and user_text:
            try:
                # If your model expects a list/array of text inputs:
                pred = model.predict([user_text])
                prediction = str(pred[0])
            except Exception as e:
                prediction = f"Error during prediction: {str(e)}"
        else:
            prediction = "Model not loaded or text missing."

    return render_template_string(HTML_TEMPLATE, prediction=prediction, user_text=user_text)

if __name__ == "__main__":
    app.run(debug=True)
