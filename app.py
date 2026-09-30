import os
import pickle
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Cosmic Sentiment Analyzer", page_icon="🚀", layout="centered"
)

# Custom CSS for Solar System, Flying Stars, and Styling
st.markdown(
    """
    <style>
        /* Global Background */
        .stApp {
            background: radial-gradient(ellipse at bottom, #1b2735 0%, #090a0f 100%);
            color: #ffffff;
        }

        /* Flying Stars Effect */
        .stars {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
        }
        .star {
            position: absolute;
            background: #ffffff;
            border-radius: 50%;
            animation: fly linear infinite;
        }
        @keyframes fly {
            from { transform: translateY(0px) scale(0.5); opacity: 0; }
            50% { opacity: 1; }
            to { transform: translateY(100vh) scale(1.2); opacity: 0; }
        }

        /* Solar System Background */
        .solar-system {
            position: fixed;
            width: 100vw;
            height: 100vh;
            top: 0;
            left: 0;
            pointer-events: none;
            z-index: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 0.25;
            overflow: hidden;
        }
        .sun {
            width: 70px;
            height: 70px;
            background: radial-gradient(circle, #ffcc00, #ff6600);
            border-radius: 50%;
            box-shadow: 0 0 40px #ff3300;
            position: absolute;
        }
        .orbit {
            position: absolute;
            border: 1px dashed rgba(255, 255, 255, 0.2);
            border-radius: 50%;
        }
        .planet {
            position: absolute;
            border-radius: 50%;
        }
        .orbit-1 { width: 180px; height: 180px; animation: spin 10s linear infinite; }
        .planet-1 { width: 10px; height: 10px; background: #00ffff; top: -5px; left: calc(50% - 5px); box-shadow: 0 0 8px #00ffff; }
        
        .orbit-2 { width: 320px; height: 320px; animation: spin 18s linear infinite reverse; }
        .planet-2 { width: 16px; height: 16px; background: #ff4757; top: -8px; left: calc(50% - 8px); box-shadow: 0 0 10px #ff4757; }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        /* Foreground container styling */
        .block-container {
            position: relative;
            z-index: 2;
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
            margin-top: 5vh;
        }
        
        h1 {
            text-align: center;
            color: #f1f2f6;
            font-size: 28px;
        }
        
        .stTextArea textarea {
            background: rgba(0, 0, 0, 0.4) !important;
            color: #fff !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
    </style>

    <div class="stars" id="stars"></div>
    <div class="solar-system">
        <div class="sun"></div>
        <div class="orbit orbit-1"><div class="planet planet-1"></div></div>
        <div class="orbit orbit-2"><div class="planet planet-2"></div></div>
    </div>

    <script>
        const starsContainer = document.getElementById('stars');
        for (let i = 0; i < 40; i++) {
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
    """,
    unsafe_allow_html=True,
)

# App UI Content
st.markdown("<h1>Cosmic Sentiment Analyzer</h1>", unsafe_allow_html=True)

# Category selection dropdown
category = st.selectbox(
    "Select Domain / Category:",
    ["General Review", "Product Feedback", "Movie Review"],
)

# Text input area
user_text = st.text_area(
    "Enter Text for Analysis:", placeholder="Type your text here..."
)

# Load Model with safe error handling
model_path = os.path.join(os.path.dirname(__file__), "vector.pkl")

@st.cache_resource
def load_model():
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Could not find '{model_path}' in the repository directory."
        )
    with open(model_path, "rb") as f:
        return pickle.load(f)

try:
    model = load_model()
except Exception as e:
    st.error(f"**Model Loading Error:** {e}")
    model = None

# Prediction button
if st.button("Predict Sentiment", use_container_width=True):
    if not user_text.strip():
        st.warning("Please enter some text before predicting.")
    elif model is None:
        st.error("Model is not available due to loading errors.")
    else:
        try:
            # Predict using the model (assumes pipeline handles vectorization)
            prediction = model.predict([user_text])[0]

            # Display outcome with styling
            st.markdown(
                f"""
                <div style="margin-top: 20px; padding: 15px; border-radius: 8px; background: rgba(0, 0, 0, 0.4); text-align: center; border: 1px solid rgba(255,255,255,0.1);">
                    Prediction: <span style="font-size: 20px; font-weight: bold; color: {'#2ed573' if str(prediction).lower() in ['positive', '1'] else '#ff4757'};">{prediction}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"**Prediction Error:** {e}")
