"""
Main Streamlit Application for the Loan Prediction Data Analysis System.
Provides a multi-page interactive dashboard for data analysis, model performance,
and real-time loan risk prediction.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys
from PIL import Image

from src.prediction import load_models, load_scaler, predict_risk

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Loan Prediction Data Analysis System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DIRECTORIES ---
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
VIS_DIR = os.path.join(BASE_DIR, 'visualizations')
MODEL_EVAL_VIS_DIR = os.path.join(VIS_DIR, 'model_evaluation')

# --- CACHED DATA LOADING ---
@st.cache_data
def load_dataset():
    """Loads the cleaned dataset for analysis."""
    path = os.path.join(DATA_DIR, 'cleaned_loan_data.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

@st.cache_data
def load_comparison_data():
    """Loads the model comparison results."""
    path = os.path.join(DATA_DIR, 'model_comparison.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

@st.cache_resource
def init_models():
    """Loads machine learning models into cache."""
    return load_models(BASE_DIR)

@st.cache_resource
def init_scaler():
    """Loads the fitted scaler into cache."""
    return load_scaler(BASE_DIR)

# Initialize resources
df = load_dataset()
comparison_df = load_comparison_data()
models = init_models()
scaler = init_scaler()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏦 Loan Prediction Data Analysis System")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "🔮 Risk Prediction", "📊 Data Analysis", "🤖 Model Performance", "📈 Visualizations", "ℹ️ About Project"]
)

st.sidebar.markdown("---")
st.sidebar.info("DAE Academic Project Demonstration")

# ==========================================
# PAGE 1: DASHBOARD
# ==========================================
if page == "🏠 Dashboard":
    st.title("Loan Prediction Data Analysis System")
    st.subheader("AI-powered loan risk analysis and prediction using Machine Learning")
    
    st.markdown("---")
    
    if df is not None:
        # Calculate metrics
        total_applicants = len(df)
        low_risk_count = len(df[df['Risk_Status'] == 'Low'])
        high_risk_count = len(df[df['Risk_Status'] == 'High'])
        
        # Display Metric Cards
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Applicants", total_applicants)
        col2.metric("Low Risk Applicants", low_risk_count)
        col3.metric("High Risk Applicants", high_risk_count)
        col4.metric("Dataset Columns", len(df.columns))
        
        st.markdown("---")
        
        col_text, col_chart = st.columns([1, 1])
        
        with col_text:
            st.markdown("### 📖 Project Overview")
            st.write(
                "This application uses advanced Machine Learning algorithms to evaluate "
                "historical loan applicant data and predict whether a new applicant "
                "poses a **Low** or **High** risk of defaulting."
            )
            st.write("### 🔑 Key Predictive Features")
            st.markdown(
                """
                - **Income**: Annual earnings of the applicant.
                - **Credit Score**: Standardized creditworthiness indicator.
                - **Loan Amount**: Total capital requested.
                - **Loan Term**: Repayment duration in months.
                - **Employment Status**: Employed, Self-Employed, or Unemployed.
                """
            )
            
        with col_chart:
            st.markdown("### 📊 Target Distribution")
            fig = px.pie(
                df, 
                names='Risk_Status', 
                title='Historical Risk Distribution',
                color='Risk_Status',
                color_discrete_map={'Low': '#2ecc71', 'High': '#e74c3c'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.error("Error: Could not load the cleaned dataset. Please ensure Step 3 was completed successfully.")

# ==========================================
# PAGE 2: RISK PREDICTION
# ==========================================
elif page == "🔮 Risk Prediction":
    st.title("🔮 Interactive Risk Prediction")
    st.write("Enter the applicant's details below to generate an AI-driven risk assessment.")
    st.markdown("---")
    
    if not models or scaler is None:
        st.error("Error: Machine Learning models or Scaler not found. Please complete Steps 6 and 7.")
    else:
        # Model Selection
        selected_model = st.selectbox(
            "Select Prediction Model", 
            ["Random Forest", "Logistic Regression", "Decision Tree"],
            index=0,
            help="Random Forest is the recommended default."
        )
        
        st.markdown("### Applicant Details")
        
        # Input Form
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
                income = st.number_input("Annual Income ($)", min_value=1000, value=50000, step=1000)
                credit_score = st.number_input("Credit Score", min_value=300, max_value=900, value=650, step=1)
                
            with col2:
                loan_amount = st.number_input("Loan Amount ($)", min_value=1000, value=15000, step=500)
                loan_term = st.number_input("Loan Term (Months)", min_value=12, max_value=60, value=36, step=12)
                emp_status = st.selectbox("Employment Status", ["Employed", "Self-Employed", "Unemployed"])
                
            submit_btn = st.form_submit_button("PREDICT LOAN RISK", type="primary")
            
        if submit_btn:
            applicant_data = {
                'Age': age,
                'Income': income,
                'Credit_Score': credit_score,
                'Loan_Amount': loan_amount,
                'Loan_Term_Months': loan_term,
                'Employment_Status': emp_status
            }
            
            with st.spinner(f"Analyzing applicant with {selected_model}..."):
                # Call existing prediction function
                result = predict_risk(applicant_data, models, scaler, model_name=selected_model)
                
                if "error" in result:
                    st.error(result['error'])
                else:
                    st.markdown("---")
                    st.markdown("### 🎯 Prediction Result")
                    
                    if result['risk_label'] == 'Low Risk':
                        st.success(f"✅ **Approved**: Applicant is classified as **LOW RISK**.")
                    else:
                        st.error(f"⚠️ **Warning**: Applicant is classified as **HIGH RISK**.")
                        
                    col_res1, col_res2, col_res3 = st.columns(3)
                    col_res1.metric("Risk Status", result['risk_label'])
                    if result['prediction_probability'] is not None:
                        col_res2.metric("Confidence Probability", f"{result['prediction_probability']}%")
                    else:
                        col_res2.metric("Confidence Probability", "N/A")
                    col_res3.metric("Model Used", result['model_name'])

# ==========================================
# PAGE 3: DATA ANALYSIS
# ==========================================
elif page == "📊 Data Analysis":
    st.title("📊 Exploratory Data Analysis")
    
    if df is not None:
        st.subheader("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Dataset Shape:** {df.shape[0]} rows, {df.shape[1]} columns")
        with col2:
            st.info(f"**Missing Values:** {df.isnull().sum().sum()} total missing cells")
            
        st.markdown("---")
        st.subheader("Statistical Summary")
        # Exclude applicant ID and dummy vars from stats
        num_cols = ['Age', 'Income', 'Credit_Score', 'Loan_Amount', 'Loan_Term_Months']
        num_cols = [c for c in num_cols if c in df.columns]
        st.dataframe(df[num_cols].describe().round(2), use_container_width=True)
        
        st.markdown("---")
        st.subheader("Risk Profiling")
        
        # Averages by Risk Status
        if 'Risk_Status' in df.columns:
            profile_df = df.groupby('Risk_Status')[num_cols].mean().round(2).reset_index()
            
            fig_inc = px.bar(profile_df, x='Risk_Status', y='Income', color='Risk_Status', title="Average Income by Risk")
            fig_cs = px.bar(profile_df, x='Risk_Status', y='Credit_Score', color='Risk_Status', title="Average Credit Score by Risk")
            
            c1, c2 = st.columns(2)
            c1.plotly_chart(fig_inc, use_container_width=True)
            c2.plotly_chart(fig_cs, use_container_width=True)
    else:
        st.error("Error: Could not load the dataset.")

# ==========================================
# PAGE 4: MODEL PERFORMANCE
# ==========================================
elif page == "🤖 Model Performance":
    st.title("🤖 Machine Learning Model Comparison")
    
    # Disclaimer
    st.warning(
        "**Academic Disclaimer:** This model was trained on a small educational dataset containing only 100 records "
        "with a 20-record test set. These evaluation metrics should be interpreted cautiously and do not represent "
        "real-world financial or loan performance."
    )
    
    if comparison_df is not None:
        st.subheader("Evaluation Metrics Table")
        st.dataframe(comparison_df, use_container_width=True)
        
        st.markdown("---")
        
        st.subheader("Performance Comparison Chart")
        
        # Melt DataFrame for Plotly grouped bar chart
        melted_df = comparison_df.melt(id_vars='Model', var_name='Metric', value_name='Score')
        fig = px.bar(
            melted_df, 
            x='Model', 
            y='Score', 
            color='Metric', 
            barmode='group',
            title='Model Metrics Comparison'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        with st.expander("ℹ️ Understanding the Metrics", expanded=False):
            st.markdown("""
            - **Accuracy**: The percentage of totally correct predictions. (Can be misleading in imbalanced datasets).
            - **Precision**: Out of all the applicants predicted as *High Risk*, how many were actually High Risk? (Minimizes False Positives).
            - **Recall**: Out of all actual *High Risk* applicants, how many did the model successfully catch? (Minimizes False Negatives).
            - **F1-Score**: The harmonic mean of Precision and Recall. Provides a single balanced score.
            """)
            
        st.markdown("---")
        st.subheader("Confusion Matrices")
        st.write("Visual breakdown of True Positives, True Negatives, False Positives, and False Negatives.")
        
        cm_col1, cm_col2, cm_col3 = st.columns(3)
        
        def display_cm_image(model_prefix, column, title):
            path = os.path.join(MODEL_EVAL_VIS_DIR, f"{model_prefix}_confusion_matrix.png")
            if os.path.exists(path):
                img = Image.open(path)
                column.image(img, caption=title, use_container_width=True)
            else:
                column.warning(f"Image not found for {title}")
                
        display_cm_image("logistic_regression", cm_col1, "Logistic Regression")
        display_cm_image("decision_tree", cm_col2, "Decision Tree")
        display_cm_image("random_forest", cm_col3, "Random Forest")
            
    else:
        st.error("Error: Could not load the model comparison data. Please ensure Step 8 is completed.")

# ==========================================
# PAGE 5: VISUALIZATIONS
# ==========================================
elif page == "📈 Visualizations":
    st.title("📈 Detailed Visualizations")
    st.write("Browse through the charts generated during the Exploratory Data Analysis (EDA) phase.")
    
    st.markdown("---")
    
    def display_static_image(filename, title):
        path = os.path.join(VIS_DIR, filename)
        if os.path.exists(path):
            img = Image.open(path)
            st.image(img, caption=title, use_container_width=True)
        else:
            st.warning(f"Visualization not found: {filename}")
            
    # Row 1
    c1, c2 = st.columns(2)
    with c1:
        display_static_image("credit_score_distribution.png", "Credit Score Distribution")
    with c2:
        display_static_image("credit_score_vs_risk.png", "Credit Score by Risk Status")
        
    st.markdown("---")
    
    # Row 2
    c3, c4 = st.columns(2)
    with c3:
        display_static_image("income_distribution.png", "Income Distribution")
    with c4:
        display_static_image("income_vs_risk.png", "Income by Risk Status")
        
    st.markdown("---")
    
    # Row 3
    c5, c6 = st.columns(2)
    with c5:
        display_static_image("loan_amount_vs_risk.png", "Loan Amount by Risk Status")
    with c6:
        display_static_image("employment_vs_risk.png", "Employment Status vs Risk")
        
    st.markdown("---")
    
    st.subheader("Correlation Heatmap")
    display_static_image("correlation_heatmap.png", "Feature Correlation Heatmap")

# ==========================================
# PAGE 6: ABOUT PROJECT
# ==========================================
elif page == "ℹ️ About Project":
    st.title("ℹ️ About the Project")
    st.subheader("Loan Prediction Data Analysis System")
    
    st.markdown("---")
    
    st.markdown("### 💻 Technology Stack")
    st.write(
        "This project was developed strictly using Python-based data science and machine learning libraries. "
        "No separate front-end web framework was utilized."
    )
    tech_tags = ["Python", "Pandas", "NumPy", "Scikit-learn", "Matplotlib", "Seaborn", "Plotly", "Streamlit", "Joblib"]
    st.markdown(" • ".join([f"**{tag}**" for tag in tech_tags]))
    
    st.markdown("### 🤖 ML Algorithms Implemented")
    st.markdown("- Logistic Regression\n- Decision Tree Classifier\n- Random Forest Classifier")
    
    st.markdown("### 📊 Dataset Overview")
    st.markdown(
        "- **Size**: 100 loan applicant records (Academic Sample)\n"
        "- **Target Variable**: `Risk_Status` (0 = Low Risk, 1 = High Risk)\n"
        "- **Key Features**: Age, Income, Credit Score, Loan Amount, Loan Term, Employment Status"
    )
    
    st.markdown("### 🔄 Project Architecture & Workflow")
    st.markdown(
        """
        1. **Data Collection**: Synthesizing applicant records.
        2. **Data Cleaning**: Handling missing values, duplicates, and outliers safely.
        3. **Exploratory Data Analysis (EDA)**: Statistical profiling.
        4. **Visualization**: Creating intuitive charts to understand relationships.
        5. **Feature Engineering**: Standard Scaling and One-Hot Encoding.
        6. **ML Training**: Training robust algorithms with reproducibility.
        7. **Model Evaluation**: Generating classification reports and confusion matrices.
        8. **Risk Prediction**: Connecting models to fresh user input.
        9. **Streamlit Dashboard**: Bringing the architecture to life interactively.
        """
    )
    
    st.info("Developed for a DAE Academic Project Demonstration.")

