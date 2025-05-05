# 🧬 Biological Age Predictor

**Author**: Sunan Gao, Siyu Zou

[![Streamlit App](https://img.shields.io/badge/Launch%20App-Streamlit-brightgreen)](https://ba-calculator.streamlit.app/)

This project provides a user-friendly Streamlit web app to estimate **Biological Age (BA)** based on clinical biomarkers. Users can input their values, and the model will output:

- ✅ Their predicted biological age
- 📊 A comparison with peers of the same chronological age
- 🎯 Percentile ranking within that group
- 📈 A clean, transparent density plot of BA distribution

---

## 🔗 Try the App Now

👉 **[Click here to launch the app](https://ba-calculator.streamlit.app/)**  
No installation needed — works directly in your browser.

---

## 🧪 Biomarkers Used

| Biomarker                  | Unit                |
|---------------------------|---------------------|
| Blood Weight              | mg                  |
| Uric Acid                 | mg/dl               |
| Hemoglobin                | g/dl                |
| Glycated Hemoglobin (HbA1c) | %                 |
| C-Reactive Protein (CRP)  | mg/l                |
| LDL Cholesterol           | mg/dl               |
| HDL Cholesterol           | mg/dl               |
| Glucose                   | mg/dl               |
| Creatinine                | mg/dl               |
| Total Cholesterol         | mg/dl               |
| Triglycerides             | mg/dl               |
| Blood Urea Nitrogen (BUN)| mg/dl                |
| Platelets                 | 10⁹/L               |
| Mean Corpuscular Volume (MCV) | fl              |
| White Blood Cell (WBC)    | 10⁹/L               |
| Waist                     | cm                  |
| Body Mass Index           | kg/m2               |
| Weight                    | Kg                  |
| Gender                    | Male(1)/Female(2)   |

---

## 🧠 How It Works

- The app uses a trained **XGBoost regression model** to predict Biological Age based on user inputs.
- The clinical inputs are scaled using a saved `StandardScaler` to match model training.
- The model then estimates the BA and compares it to age-matched distributions from the training dataset.
- The output includes:
  - Predicted BA
  - Age group percentile
  - Transparent density plot of BA distribution with user's BA highlighted
