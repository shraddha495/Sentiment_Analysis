import os
import pickle
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="CyberSentiment AI", page_icon="⚡", layout="centered"
)

# Custom CSS for Cyberpunk / Matrix Matrix Rain Theme & Styling
st.markdown(
    """
    <style>
        /* Global Cyberpunk Dark Theme */
        .stApp {
            background: #05050a;
            background-image: 
                radial-gradient(circle at 50% 10%, #1f1035 0%, transparent 60%),
                radial-gradient(circle at 10% 90%, #0a2535 0%, transparent 50%);
            color: #00ffcc;
            font-family: 'Courier New', Courier, monospace;
        }

        /* Matrix Digital Rain Background Effect */
        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
            opacity: 0.15;
        }
        .matrix-column {
            position: absolute;
            top: -50%;
            color: #00ffcc;
            font-size: 14px;
            line-height: 14px;
            writing-mode: vertical-lr;
            animation: fall linear infinite;
        }
        @keyframes fall {
            0% { transform: translateY(-50%); }
            100% { transform: translateY(150vh); }
        }

        /* Floating Neon Orbs */
        .neon-orb {
            position: fixed;
            width: 300px;
            height: 300px;
            background: rgba(0, 255, 204, 0.08);
            border-radius: 50%;
            filter: blur(80px);
            z-index: 0;
            animation: floatOrb 8s ease-in-out infinite alternate;
            pointer-events: none;
        }
        .orb-2 {
            background: rgba(255, 0, 128, 0.08);
            right: 5%;
            bottom: 10%;
            animation-delay: -4s;
        }
        @keyframes floatOrb {
            0% { transform: translateY(0px) scale(1); }
            100% { transform: translateY(-30px) scale(1.1); }
        }

        /* Main Glass Card */
        .block-container {
            position: relative;
            z-index: 2;
            background: rgba(10, 10, 20, 0.75);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(0, 255, 204, 0.3);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 0 30px rgba(0, 255, 204, 0.15), inset 0 0 15px rgba(0, 255, 204, 0.05);
            margin-top: 5vh;
        }
        
        /* Typography */
        h1 {
            text-align: center;
            color: #ffffff;
            font-size: 32px;
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 0 0 10px rgba(0, 255, 204, 0.6);
            margin-bottom: 25px;
        }
        
        label {
            color: #00ffcc !important;
            font-weight: bold;
            letter-spacing: 1px;
        }

        /* Input Elements */
        .stSelectbox div[data-baseweb="select"] {
            background: rgba(0, 0, 0, 0.6) !important;
            border: 1px solid rgba(0, 255, 204, 0.4) !important;
            color: #fff !important;
            border-radius: 8px;
        }
        
        .stTextArea textarea {
            background: rgba(0, 0, 0, 0.6) !important;
            color: #00ffcc !important;
            border: 1px solid rgba(0, 255, 204, 0.4) !important;
            border-radius: 8px;
            font-family: inherit;
        }
        .stTextArea textarea:focus {
            border-color: #ff0080 !important;
            box-shadow: 0 0 10px rgba(255, 0, 128, 0.5);
        }

        /* Neon Action Button */
        .stButton button {
            width: 100%;
            background: linear-gradient(90deg, #00ffcc, #0077ff);
            color: #05050a;
            font-weight: bold;
            border: none;
            padding: 12px;
            border-radius: 8px;
            letter-spacing: 2px;
            text-transform: uppercase;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
        }
        .stButton button:hover {
            background: linear-gradient(90deg, #ff0080, #ff8c00);
            color: #ffffff;
            box-shadow: 0 0 25px rgba(255, 0, 128, 0.8);
            transform: translateY(-2px);
        }
    </style>

    <!-- Background Elements -->
    <div class="matrix-bg" id="matrix"></div>
    <div class="neon-orb"></div>
    <div class="neon-orb orb-2"></div>

    <script>
        // Generate Matrix Rain Character Columns
        const matrixContainer = document.getElementById('matrix');
        const characters = "0101010101XYZ_CYBER_AI_NLP+-$#@";
        const columns = Math.floor(window.innerWidth / 30);
        
        for (let i = 0; i < columns; i++) {
            const col = document.createElement('div');
            col.classList.add('matrix-column');
            col.style.left = `${i * 30}px`;
            col.style.animationDuration = `${Math.random() * 5 + 3}s`;
            col.style.animationDelay = `${Math.random() * 5}s`;
            
            let text = "";
            for (let j = 0; j < 25; j++) {
                text += characters.charAt(Math.floor(Math.random() * characters.length)) + "<br>";
            }
            col.innerHTML = text;
            matrixContainer.appendChild(col);
        }
    </script>
    """,
    unsafe_allow_html=True,
)

# App Header
st.markdown("<h1>⚡ CyberSentiment AI</h1>", unsafe_allow_html=True)

# Category selection dropdown
category = st.selectbox(
    "SELECT ANALYSIS PROTOCOL:",
    ["General Review", "Product Feedback", "Movie Review"],
)

# Text input area
user_text = st.text_area(
    "INPUT TARGET TEXT:", placeholder="Enter sentence or review stream..."
)

# Load Model/Vectorizer file safely
model_path = os.path.join(os.path.dirname(__file__), "vector.pkl")

@st.cache_resource
def load_saved_object():
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Could not find '{model_path}' in the repository directory.")
    with open(model_path, "rb") as f:
        return pickle.load(f)

loaded_obj = None
load_error = None
try:
    loaded_obj = load_saved_object()
except Exception as e:
    load_error = str(e)
    st.error(f"**System Warning:** {e}")

# Prediction execution
if st.button("EXECUTE ANALYSIS"):
    if not user_text.strip():
        st.warning("⚠️ Warning: Data stream empty. Please input text.")
    elif load_error:
        st.error("⚠️ System halted due to model loading exceptions.")
    else:
        try:
            # Case 1: Tuple containing (vectorizer, classifier)
            if isinstance(loaded_obj, tuple) and len(loaded_obj) == 2:
                vectorizer, classifier = loaded_obj
                transformed_text = vectorizer.transform([user_text])
                prediction = classifier.predict(transformed_text)[0]
            
            # Case 2: Pipeline or object with direct predict method
            elif hasattr(loaded_obj, "predict"):
                prediction = loaded_obj.predict([user_text])[0]
            
            # Case 3: Fallback if only vectorizer exists
            else:
                text_lower = user_text.lower()
                positive_words = ["good", "great", "awesome", "excellent", "happy", "love", "wonderful", "fantastic", "best", "positive", "nice", "super", "brilliant"]
                negative_words = ["bad", "worst", "terrible", "awful", "sad", "hate", "poor", "disappointing", "negative", "horrible", "useless", "boring"]
                
                pos_count = sum(1 for word in positive_words if word in text_lower)
                neg_count = sum(1 for word in negative_words if word in text_lower)
                
                prediction = "Positive" if pos_count >= neg_count else "Negative"
                st.info("ℹ️ Note: Vectorizer-only file detected. Executing fallback matrix evaluation.")

            # Dynamic Result Styling
            is_positive = str(prediction).lower() in ['positive', '1', 'joy']
            result_color = "#00ffcc" if is_positive else "#ff0055"
            glow_shadow = "rgba(0, 255, 204, 0.6)" if is_positive else "rgba(255, 0, 85, 0.6)"

            st.markdown(
                f"""
                <div style="margin-top: 25px; padding: 20px; border-radius: 12px; background: rgba(0, 0, 0, 0.7); text-align: center; border: 1px solid {result_color}; box-shadow: 0 0 20px {glow_shadow};">
                    <span style="font-size: 14px; color: #a4b0be; letter-spacing: 2px; display: block; margin-bottom: 5px;">ANALYSIS RESULT</span>
                    <span style="font-size: 24px; font-weight: bold; color: {result_color}; text-shadow: 0 0 10px {glow_shadow}; text-transform: uppercase;">{prediction}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"**Execution Error:** {e}")
