# 🧹 AI Data Cleaner using Google Gemini

**AI Data Cleaner** is a Python-based application powered by **Google Gemini** that automatically cleans datasets like a human data analyst. It is designed to handle **large datasets (100,000+ rows)** and generates a detailed, human-readable summary of all cleaning actions performed. This tool is perfect for data analysts, students, and professionals who want to quickly clean and understand their datasets.

---

## 🔹 Features

- **File Upload:** Supports CSV and Excel (`.xlsx`) files.
- **Duplicate Removal:** Automatically detects and removes duplicate rows.
- **Missing/Null Value Handling:**  
  - Numeric columns → filled with **mean**  
  - Categorical columns → filled with **mode**  
- **Human-like Cleaning Summary:** Generates a descriptive summary using Gemini AI explaining what changes were made and why.
- **Shape Tracking:** Shows dataset shape **before and after cleaning**.
- **Downloadable Outputs:**  
  - Cleaned dataset as CSV  
  - Cleaning summary report as TXT
- **Large Dataset Support:** Handles datasets with over 100,000 rows efficiently.
- **Extensible:** Can be extended to include outlier detection, type corrections, and other advanced cleaning operations.

---

## 🔹 How It Works

1. **Upload Dataset:** CSV or Excel file.  
2. **Automatic Cleaning:** Duplicates removed, nulls filled intelligently.  
3. **AI Summary:** Google Gemini generates a human-readable report explaining each cleaning action.  
4. **Review Changes:** Users can see the cleaning steps and dataset shape before and after cleaning.  
5. **Download Results:** Cleaned dataset and cleaning summary report are downloadable.

---

## 🔹 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-data-cleaner.git
cd ai-data-cleaner

2. Install Dependencies
pip install -r requirements.txt


Required Packages:

Python 3.9+

Streamlit

Pandas

Google Generative AI SDK (google-generativeai)

Openpyxl (for Excel support)

3. Run the Application
streamlit run "Ai Data Cleaner.py"


🔹 Usage

Open the Streamlit app in your browser.

Upload your dataset (CSV or Excel).

View dataset preview and original shape.

The app automatically:

Removes duplicates

Fills missing/null values

Generates a human-like cleaning summary

Download the cleaned dataset and report.

🔹 Example Screenshots

(Add screenshots here)

Original dataset preview

Cleaning summary report

Cleaned dataset shape

🔹 Advanced Features (Future Updates)

Outlier Detection: Automatically detect and handle extreme values using Z-score or IQR methods.

Data Type Correction: Detect incorrect data types and automatically correct them.

Custom Cleaning Rules: Users can define their own cleaning rules for specific columns.

Batch Processing: Handle multiple datasets in one go.

🔹 Project Structure
ai-data-cleaner/
│
├── Ai Data Cleaner.py     # Main Streamlit app
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

🔹 License

This project is licensed under the MIT License.

🔹 Contributing

Contributions are welcome! Please open an issue or submit a pull request for bug fixes, improvements, or new features.

🔹 Contact

Created by [Your Name]
Email: your.email@example.com

GitHub: https://github.com/yourusername


---

✅ This README.md is **detailed, professional, and ready to use** for GitHub.  

If you want, I can **also make an “ultra-big version” with diagrams, workflow steps, and Gemini AI explanation examples** so it becomes a **full project showcase**.  

Do you want me to do that?
