import streamlit as st
import pickle
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Cosmic Sentiment Analyzer",
    page_icon="🌌",
    layout="centered"
)

# Custom CSS with Animated Flying/Floating Stars & Solar System Background
st.markdown("""
    <style>
    /* Animated Space & Solar System Background */
    body {
        color: #ffffff;
    }
    .stApp {
        background: radial-gradient(ellipse at bottom, #0d1b2a 0%, #1b263b 50%, #000814 100%);
        overflow-x: hidden;
    }
    
    /* Flying/Floating Animated Stars Effect */
    @keyframes moveStars {
        from { transform: translateY(0px); }
        to { transform: translateY(-2000px); }
    }

    .star-field {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 200%;
        pointer-events: none;
        z-index: 0;
        background-image: radial-gradient(2px 2px at 20px 30px, #ffffff, rgba(0,0,0,0)),
                          radial-gradient(2px 2px at 40px 170px, #00f5ff, rgba(0,0,0,0)),
                          radial-gradient(1px 1px at 90px 40px, #ff007f, rgba(0,0,0,0)),
                          radial-gradient(2px 2px at 160px 220px, #ffffff, rgba(0,0,0,0)),
                          radial-gradient(1.5px 1.5px at 300px 250px, #7209b7, rgba(0,0,0,0)),
                          radial-gradient(2px 2px at 450px 100px, #00b4d8, rgba(0,0,0,0));
        background-repeat: repeat;
        background-size: 500px 500px;
        animation: moveStars 60s linear infinite;
        opacity: 0.8;
    }

    /* Main Glassmorphism Container Styling */
    .main-content {
        position: relative;
        z-index: 1;
        background: rgba(13, 27, 42, 0.85);
        padding: 35px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 245, 255, 0.2);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    h1, h2, h3, label {
        color: #e0fbfc !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Custom Button Style */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #00b4d8, #7209b7);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 16px;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #0077b6, #560bad);
        box-shadow: 0 0 20px rgba(0, 180, 216, 0.6);
    }
    </style>
    <div class="star-field"></div>
""", unsafe_allow_html=True)

# Load the trained model safely
@st.cache_resource
def load_model():
    try:
        with open('sentiment.pkl', 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        return None

model = load_model()

# App Layout Container
st.markdown('<div class="main-content">', unsafe_allow_html=True)

st.title("🪐 Cosmic Sentiment Analyzer")
st.write("Explore the emotional universe of your text. Enter your sentence below to classify it as **Positive**, **Negative**, or **Zero**.")

# User text input
user_input = st.text_area("✍️ Input Text:", placeholder="Type your text here to scan the cosmos...")

if st.button("🚀 Analyze Sentiment"):
    if not user_input.strip():
        st.warning("⚠️ Please provide text before launching the analysis.")
    elif model is None:
        st.error("❌ Error: Could not locate or load `sentiment.pkl`. Make sure the file is in the same directory as `app.py`.")
    else:
        try:
            # Handles text prediction safely (supports lists, 1D/2D requirements depending on pipeline structure)
            data_input = [user_input]
            
            try:
                prediction = model.predict(data_input)[0]
            except ValueError:
                # Fallback reshape if the estimator expects a 2D array structure
                prediction = model.predict(np.array(data_input).reshape(-1, 1))[0]
            
            st.markdown("---")
            st.markdown("### 🔭 Analysis Results:")
            
            # Format outputs for positive, negative, or zero
            pred_str = str(prediction).strip().lower()
            
            if pred_str in ['positive', '1', 'pos']:
                st.success("✨ **Sentiment: Positive** (Stellar vibes detected!)")
                st.markdown("⭐ ⭐ ⭐ ⭐ ⭐")
            elif pred_str in ['negative', '-1', 'neg']:
                st.error("☄️ **Sentiment: Negative** (Asteroid impact of negativity.)")
                st.markdown("⭐ ⚪ ⚪ ⚪ ⚪")
            else:
                st.info("🪐 **Sentiment: Zero / Neutral** (Orbiting in equilibrium.)")
                st.markdown("⭐ ⭐ ⭐ ⚪ ⚪")
                
        except Exception as e:
            st.error(f"⚠️ Prediction Error: {e}")
            st.info("Note: Make sure your `sentiment.pkl` contains a full scikit-learn Pipeline that handles both vectorization and classification from raw text strings.")

st.markdown('</div>', unsafe_allow_html=True)
