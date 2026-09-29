# AI Course Recommendation Engine

A course recommendation system built with a Large Language Model (LLM), Chroma Vector Database, and an interactive Gradio web interface.

---

## 🚀 How to Run the App

### 1. Create and Activate Virtual Environment

**On Windows:**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate
```

**On macOS / Linux:**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### 2. Install Dependencies
With your virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

### 3. Set Up Your Environment Variable
Create a `.env` file in the root directory and add your Hugging Face token:

```env
HF_TOKEN=your_huggingface_token_here
```

### 4. Run the Gradio App
Start the web application by running:

```bash
python app.py
```

### 5. Open in Browser
Once the server is running, open your browser and go to:

👉 **http://127.0.0.1:7860** (or **http://localhost:7860**)

---

## 💡 How to Use the App

1. **🤖 Search by AI Query:**
   - Type what kind of course you want in the **Search Query** box (e.g., *"free beginner python courses with rating above 4.5"*).
   - Click **"Search by AI Query"** to let the LLM extract your intent and find matching courses.

2. **🎛️ Search by Filters:**
   - Set your preferred options on the left (Course Type, Max Price, Language, Subcategory, Duration, Min Rating, etc.).
   - Click **"Search by Filters"** to view matching courses.
   - Click **"Reset Filters"** to reset all inputs to default.

---

## 📂 Project Structure

```text
├── app.py                             # Main Gradio web application
├── requirements.txt                   # Project dependencies
├── .env                               # Environment variables (API token)
├── backend/
│   ├── backend_recomm_sys.py          # Recommendation logic & vector search
│   ├── backend_recomm_sys.ipynb       # Backend testing notebook
│   └── EDA_PP_recomm_sys.ipynb        # Data analysis & preprocessing notebook
├── frontend/
│   └── helper.py                      # UI helper functions
└── data/
    ├── chroma_db/                     # Chroma vector database
    ├── udemy_data_cleaned.xlsx        # Cleaned dataset
    └── udemy_data_till_2023.csv       # Raw dataset
```