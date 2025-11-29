# -*- coding: utf-8 -*-
"""AI Data Cleaner with Streamlit - Error Fixed"""

import streamlit as st
import pandas as pd
import io
import google.generativeai as genai

# -------------------------
# Streamlit UI
# -------------------------
st.title("🧹 AI Data Cleaner using Gemini")

# -------------------------
# API Key Input
# -------------------------
api_key = st.text_input("🔑 Enter your Gemini API Key", type="password", help="Get your API key from https://makersuite.google.com/app/apikey")

if api_key:
    try:
        # Configure Gemini with user-provided key
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        st.success("✅ API Key configured successfully!")
    except Exception as e:
        st.error(f"❌ Error configuring API: {str(e)}")
        st.stop()
else:
    st.warning("⚠️ Please enter your Gemini API key to continue")
    st.stop()

# -------------------------
# File Upload
# -------------------------
uploaded_file = st.file_uploader("📂 Upload your dataset (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # -------------------------
        # Load dataset
        # -------------------------
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.write("### 🔍 Original Dataset Preview")
        st.dataframe(df.head(10))
        st.write(f"**Original Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Copy dataset for cleaning
        cleaned_df = df.copy()
        cleaning_steps = []
        
        # -------------------------
        # 1. Handle duplicates
        # -------------------------
        dup_count = cleaned_df.duplicated().sum()
        if dup_count > 0:
            cleaned_df.drop_duplicates(inplace=True)
            cleaning_steps.append(f"Removed {dup_count} duplicate rows.")
        
        # -------------------------
        # 2. Handle null values
        # -------------------------
        null_counts = cleaned_df.isnull().sum()
        total_nulls = null_counts.sum()
        
        if total_nulls > 0:
            for col in cleaned_df.columns:
                null_count = cleaned_df[col].isnull().sum()
                if null_count > 0:
                    if cleaned_df[col].dtype in ["int64", "float64"]:
                        mean_val = cleaned_df[col].mean()
                        cleaned_df[col].fillna(mean_val, inplace=True)
                        cleaning_steps.append(
                            f"Filled {null_count} missing values in **{col}** with mean ({mean_val:.2f})."
                        )
                    else:
                        # Handle mode safely
                        mode_series = cleaned_df[col].mode()
                        if len(mode_series) > 0:
                            mode_val = mode_series[0]
                        else:
                            mode_val = "Unknown"
                        cleaned_df[col].fillna(mode_val, inplace=True)
                        cleaning_steps.append(
                            f"Filled {null_count} missing values in **{col}** with mode ('{mode_val}')."
                        )
        
        # -------------------------
        # 3. Create cleaning summary prompt
        # -------------------------
        summary_prompt = f"""
You are an AI Data Cleaner. The dataset had {df.shape[0]} rows and {df.shape[1]} columns.
After cleaning, it has {cleaned_df.shape[0]} rows and {cleaned_df.shape[1]} columns.

Cleaning steps performed:
{chr(10).join(cleaning_steps) if cleaning_steps else "No cleaning was required."}

Write a clear, human-like summary report explaining what was cleaned and why.
"""
        
        # -------------------------
        # 4. Generate Gemini summary
        # -------------------------
        with st.spinner("🤖 Generating AI cleaning report..."):
            response = model.generate_content(summary_prompt)
            report_text = response.text
        
        # -------------------------
        # 5. Show results
        # -------------------------
        st.write("### 📝 Cleaning Summary Report")
        st.markdown(report_text)
        st.write(f"**Cleaned Shape:** {cleaned_df.shape[0]} rows × {cleaned_df.shape[1]} columns")
        
        st.write("### 📊 Cleaned Dataset Preview")
        st.dataframe(cleaned_df.head(10))
        
        # -------------------------
        # 6. Download cleaned dataset
        # -------------------------
        csv_buffer = io.BytesIO()
        cleaned_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        st.download_button(
            label="⬇️ Download Cleaned Dataset",
            data=csv_buffer.getvalue(),
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )
        
        # -------------------------
        # 7. Download cleaning report
        # -------------------------
        st.download_button(
            label="⬇️ Download Cleaning Report",
            data=report_text,
            file_name="cleaning_report.txt",
            mime="text/plain"
        )
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info("Please make sure your file is a valid CSV or Excel file.")
else:
    st.info("👆 Please upload a CSV or Excel file to begin cleaning")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.markdown("""
💡 **Tips:**
- The tool automatically removes duplicates and fills missing values
- Numeric columns use mean for missing values
- Text columns use mode (most common value) for missing values
- Get your free Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
""")
