import streamlit as st
import numpy as np
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout='wide')
st.title("🧬 Biological Age Predictor")

st.markdown("""
Enter your clinical measurements to predict your **Biological Age (BA)**.  
We'll also show the **distribution of BA among people your age** and your **percentile ranking**.
""")

# Load model, scaler, and distribution
@st.cache_resource
def load_all():
    model = joblib.load("trained_models/ba_xgboost_model.pkl")
    CA_scaler = joblib.load("trained_models/LR_adjust_ba_ca.pkl")
    ba_distribution = pd.read_csv("data/df_ba_distribution.csv")
    return model, CA_scaler, ba_distribution

model, CA_scaler, df_dist = load_all()

# Variable display names with units
feature_info = {
    'Blood_weight': "Blood Weight (ug)",
    'Uric_Acid': "Uric Acid (mg/dl)",
    'Hemoglobin': "Hemoglobin (g/dl)",
    'Glycated_Hemoglobin': "Glycated Hemoglobin (%)",
    'CRP': "C-Reactive Protein (mg/l)",
    'LDL': "LDL Cholesterol (mg/dl)",
    'HDL': "HDL Cholesterol (mg/dl)",
    'Glucose': "Glucose (mg/dl)",
    'Creatinine': "Creatinine (mg/dl)",
    'Cholesterol': "Total Cholesterol (mg/dl)",
    'Triglycerides': "Triglycerides (mg/dl)",
    'BUN': "Blood Urea Nitrogen (mg/dl)",
    'Platelets': "Platelets (10⁹/L)",
    'MCV': "Mean Corpuscular Volume (fl)",
    'White_Blood_Cell': "White Blood Cell (10⁹/L)",
    'Waist': 'Waist(cm)',
    'Weight': 'Weight(kg)',
    'BMI': 'BMI (kg/m2)',
    'Gender': 'Male:1; Female:2'
}


# Default values (adjust as needed)
default_values = {
    'Blood_weight': 30000.0,
    'Uric_Acid': 5.5,
    'Hemoglobin': 14.0,
    'Glycated_Hemoglobin': 5.5,
    'CRP': 1.0,
    'LDL': 110.0,
    'HDL': 55.0,
    'Glucose': 90.0,
    'Creatinine': 0.9,
    'Cholesterol': 190.0,
    'Triglycerides': 120.0,
    'BUN': 14.0,
    'Platelets': 250.0,
    'MCV': 90.0,
    'White_Blood_Cell': 6.5,
    'Waist': 90.0,
    'Weight': 80.0,
    'BMI': 25.0,
    'Gender': 1.0
}

# User input form
st.markdown("### 🧾 Enter Your Clinical Measurements")

with st.form("ba_input_form"):
    cols = st.columns(4)
    user_input = []

    for i, (var, label) in enumerate(feature_info.items()):
        with cols[i % 4]:
            val = st.number_input(label, value=default_values[var], step=0.1)
            user_input.append(val)

    user_actual_age = st.number_input("🎂 Your Chronological Age", min_value=0, max_value=120, value=50, step=1)
    submitted = st.form_submit_button("🔍 Predict Biological Age Acceleration")

st.markdown("""
We'll also show the **distribution of BA among people your age** and your **percentile ranking**.
""")

# Run prediction
if submitted:
    try:
        user_input_df = pd.DataFrame([user_input], columns=feature_info.keys())
        ba = model.predict(user_input_df)[0]
        age_grp = int(np.floor(user_actual_age))
        group_data = df_dist[df_dist['age_group'] == age_grp]['predicted_ba']
        median_ba = group_data.median()
        baa = ba - median_ba

        if not group_data.empty:
            percentile = (group_data < ba).mean() * 100
            group_data_baa = group_data.values - median_ba

            # Plot and metrics in 2-column layout
            col1, col2 = st.columns([1, 2])

            with col1:
                st.metric(label="🎯 Predicted BAA", value=f"{baa:.1f} years")
                st.markdown(f"- **Chronological Age (CA):** {user_actual_age} years")
                st.markdown(f"- **Biological Age (BA):** {ba:.1f} years")
                st.markdown(f"- **Median BA (Age {age_grp}):** {median_ba:.1f} years")
                st.markdown(f"- **Percentile Rank:** {percentile:.1f}th")

            with col2:
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.kdeplot(group_data_baa, fill=True, color='skyblue', linewidth=2, ax=ax)
                ax.axvline(baa, color='red', linestyle='--', linewidth=2, label='Your BAA')
                ax.axvline(0, color='gray', linestyle='--', linewidth=1.5, label='BAA = 0 (Median BA)')
                ax.set_title(f"BAA Distribution (Age {age_grp})", fontsize=14)
                ax.set_xlabel("Biological Age Acceleration (BAA)", fontsize=12)
                ax.set_ylabel("Density")
                ax.legend()
                sns.despine(trim=True)
                ax.set_facecolor("white")
                fig.patch.set_facecolor("white")
                st.pyplot(fig)

        else:
            st.warning("Not enough samples in your age group to show the distribution.")

    except Exception as e:
        st.error(f"Error: {e}")