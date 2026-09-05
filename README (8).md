# ✨ Gemini The Data Analyzer

**AI Data Cleaner — Premium Edition** is a Streamlit web app that cleans messy datasets like a human data analyst, powered by **Google Gemini AI**. It handles large files (500K+ rows) with chunked processing, gives you a live diagnostics dashboard, generates a polished **PDF quality report**, and includes a built-in **AI chatbot** that can answer questions about your cleaned dataset.

---

## 🔹 Features

- **File Upload** — Supports CSV and Excel (`.xlsx`) files, with an instant preview before cleaning.
- **Pre-Clean Diagnostics** — Total rows/columns, missing-value count, duplicate count, and a per-column completeness breakdown before you run anything.
- **Chunked Cleaning Engine** — Processes data in 50,000-row chunks so large datasets (100,000+ rows) clean smoothly without stalling the app.
- **Configurable Cleaning Options**
  - Remove duplicate rows
  - Fill missing values (numeric → **mean**, **median**, or **zero**; categorical/text → **mode**)
  - Strip leading/trailing whitespace from text columns
  - Normalize text case (optional lowercase)
- **Live Cleaning Log** — A terminal-style log shows every fix as it happens (duplicates removed, nulls filled, per chunk).
- **AI-Generated PDF Report** — A structured, designed PDF (via ReportLab) with a summary cover page, before/after metrics, a full list of cleaning operations, and a column-by-column quality breakdown.
- **Dataset Chatbot** — Ask Gemini natural-language questions about your cleaned dataset (trends, missing data, outliers, correlations, summaries), with quick-suggestion chips and conversation history.
- **Downloadable Outputs**
  - Cleaned dataset as **CSV**
  - Full cleaning report as **PDF**
- **Large Dataset Support** — Built to scale to very large files through chunked reads and processing.
- **Custom Dark UI** — A polished, purpose-built Streamlit theme (not the default Streamlit look).

---

## 🔹 How It Works

1. **Enter your Gemini API key** in the sidebar (never stored — used only for your session).
2. **Upload a dataset** (CSV or Excel) and review the instant preview.
3. **Choose cleaning options** — duplicates, missing-value strategy, whitespace, casing.
4. **Run the Cleaning Pipeline** — the app processes your data in chunks and shows live progress and a diagnostics dashboard (before vs. after).
5. **Review results** — completeness bars, a cleaning-operations log, and row/column metrics.
6. **Download** the cleaned CSV and/or the AI-generated PDF report.
7. **Chat with your data** — ask Gemini follow-up questions about the cleaned dataset directly in the app.

---

## 🔹 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-data-cleaner.git
cd ai-data-cleaner
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

**Required packages:**
- Python 3.9+
- `streamlit`
- `pandas`
- `numpy`
- `google-generativeai`
- `reportlab`
- `openpyxl` (for Excel support)

You can generate a `requirements.txt` with:
```bash
streamlit
pandas
numpy
google-generativeai
reportlab
openpyxl
```

### 3. Get a Gemini API Key
Grab a free key from [Google AI Studio](https://aistudio.google.com/app/apikey). You'll paste this directly into the app's sidebar — it isn't stored anywhere.

### 4. Run the Application
```bash
streamlit run "AI-Data-Cleaner-Using-Gemini.py"
```

---

## 🔹 Usage

1. Open the app in your browser (Streamlit will launch it automatically).
2. Paste your **Gemini API key** into the sidebar field.
3. Upload your dataset (**CSV or Excel**).
4. Review the dataset preview and pick your cleaning options.
5. Click **Run Cleaning Pipeline**. The app will:
   - Show pre-clean diagnostics (rows, columns, missing values, duplicates)
   - Process the data in chunks, removing duplicates and filling missing values
   - Display a live cleaning log and before/after metrics
6. **Download** the cleaned CSV and the PDF quality report.
7. Use the **Dataset Chatbot** to ask Gemini questions about your cleaned data.

---

## 🔹 Example Screenshots

*(Add screenshots here)*

- Dataset preview & pre-clean diagnostics
- Cleaning pipeline log & metrics
- PDF quality report
- Dataset chatbot in action

---

## 🔹 Advanced Features (Future Updates)

- **Outlier Detection** — Automatically flag extreme values using Z-score or IQR methods.
- **Data Type Correction** — Detect and fix incorrect column data types automatically.
- **Custom Cleaning Rules** — Let users define column-specific cleaning logic.
- **Batch Processing** — Clean multiple datasets in a single run.

---

## 🔹 Project Structure

```
ai-data-cleaner/
│
├── AI-Data-Cleaner-Using-Gemini.py   # Main Streamlit app
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
```

---

## 🔹 License

This project is licensed under the MIT License.

## 🔹 Contributing

Contributions are welcome! Please open an issue or submit a pull request for bug fixes, improvements, or new features.

## 🔹 Contact

Created by **[Your Name]**
- Email: your.email@example.com
- GitHub: https://github.com/yourusername
