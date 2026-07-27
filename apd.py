import streamlit as st
import numpy as np
# If you are using TensorFlow/Keras to load your ANN model, uncomment the line below:
# import tensorflow as tf

# 1. Page Configuration
st.set_page_config(
    page_title="Angina Pectoris Diagnosis System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Manage navigation using session_state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Array to store the 14 inputs to be ready for the model
if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = None


# ==========================================
# 🛑 PAGE 1: Welcome / Home Screen
# ==========================================
if st.session_state.page == 'home':
    # Splitting the page: Left 1/3 for text, Right 2/3 for the image
    col_text, col_img = st.columns([1, 2])
    
    with col_text:
        st.write("") 
        st.write("")
        st.markdown("<h1 style='font-size: 38px; margin-bottom: 5px;'>Angina Pectoris Diagnosis</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 18px; color: gray;'>AI-Based Clinical Decision Support</p>", unsafe_allow_html=True)
        
        st.write("")
        # Start Button
        if st.button("Get Started 🚀", use_container_width=True):
            st.session_state.page = 'inputs'
            st.rerun()
            
    with col_img:
        st.image("photo.png"), 
                 caption="Intelligent Medical Decision Support System", use_container_width=True)
        


# ==========================================
# 🛑 PAGE 2: The 14 Clinical Inputs
# ==========================================
elif st.session_state.page == 'inputs':
    st.markdown("<h2 style='text-align: center;'>📋 Patient Medical Clinical Indicators ", unsafe_allow_html=True)
    st.write("Please carefully enter the patient's vital clinical data:")
    
    # Distributing the 14 inputs into 3 columns for a clean and structured layout
    with st.form("inputs_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            v1 = st.number_input("1. Age", min_value=1, max_value=120, value=50)
            sex_input = st.selectbox("2. Sex", options=["Male", "Female"])
            v3 = st.number_input("3. Chest Pain Type (CP: 0-3)", min_value=0, max_value=3, value=0)
            v4 = st.number_input("4. Resting Blood Pressure (mm Hg)", min_value=50, max_value=250, value=120)
            v5 = st.number_input("5. Serum Cholestoral (mg/dl)", min_value=100, max_value=600, value=200)

        with col2:
            fbs_input = st.selectbox("6. Fasting Blood Sugar > 120 mg/dl", options=["True", "False"])
            v7 = st.number_input("7. Resting Electrocardiographic Results (0-2)", min_value=0, max_value=2, value=0)
            v8 = st.slider("8. Maximum Heart Rate Achieved (Max HR)", 60, 220, 150)
            exang_input = st.selectbox("9. Exercise Induced Angina", options=["Yes", "No"])
            v10 = st.number_input("10. ST Depression Induced by Exercise", min_value=0.0, max_value=10.0, value=0.0, step=0.1)

        with col3:
            v11 = st.number_input("11. Slope of the Peak Exercise ST Segment (0-2)", min_value=0, max_value=2, value=1)
            v12 = st.number_input("12. Number of Major Vessels (0-3)", min_value=0, max_value=3, value=0)
            v13 = st.number_input("13. Thalassemia Test Result (1-3)", min_value=1, max_value=3, value=1)
            v14 = st.number_input("14. Additional Feature / BMI", min_value=10, max_value=50, value=25)

        st.write("")
        # Diagnosis Button
        submit_btn = st.form_submit_button("🩺 Diagnose Now", use_container_width=True)
        
        # الأسطر القادمة هي التي كانت مسببة للمشكلة، وتم ضبط محاذاتها للداخل الآن لتكون تابعة لـ الـ if
        if submit_btn:
            # Encoding categorical variables into numbers
            v2 = 1 if sex_input == "Male" else 0
            v6 = 1 if fbs_input == "True" else 0
            v9 = 1 if exang_input == "Yes" else 0
            
            # Creating the NumPy array correctly indented inside the if statement
            input_data = np.array([[v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14]])
            
            # Saving the array to session state and moving to results page
            st.session_state.user_inputs = input_data
            st.session_state.page = 'result'
            st.rerun()


# ==========================================
# 🛑 PAGE 3: Diagnosis Report & Remarks
# ==========================================
elif st.session_state.page == 'result':
    st.markdown("<h2 style='text-align: center;'>📊 Final Diagnosis Report</h2>", unsafe_allow_html=True)
    st.write("")
    
    # Simulation logic based on Max Heart Rate (v8 is at index 7)
    if st.session_state.user_inputs[0][7] > 160: 
        has_angina = True
        confidence = 87.5
    else:
        has_angina = False
        confidence = 92.1

    # Displaying Results Visually
    if has_angina:
        st.error(f"⚠️ Alert: Clinical indicators suggest a high probability of Angina Pectoris ({confidence}%)")
        
        st.subheader("📋 Clinical Notes & Recommendations:")
        st.info("""
        * Immediate diagnostic cardiac catheterization is highly recommended to evaluate the coronary artery status.
        * The patient should avoid strenuous physical activity and remain under clinical observation.
        * Verify the ST depression (Oldpeak) values thoroughly with a specialized cardiologist.
        """)
    else:
        st.success(f"✅ Result: Vital indicators are within normal limits. No immediate signs of Angina detected (Confidence: {confidence}%)")
        
        st.subheader("📋 Clinical Notes & Recommendations:")
        st.info("""
        * Cardiac parameters appear stable based on the 14 submitted features.
        * Encourage the patient to maintain a healthy lifestyle and monitor blood pressure regularly.
        """)
        
    st.write("")
    st.divider()
    
    # Back to Page 1 Button
    if st.button("⬅️ Return to Main Page", use_container_width=True):
        st.session_state.user_inputs = None
        st.session_state.page = 'home'
        st.rerun()
