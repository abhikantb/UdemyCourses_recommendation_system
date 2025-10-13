# Project Title

This project is a recommendation system built with a Large Language Model (LLM) and a Chroma vector database.

---

## 📂 Project Structure
.
├── .venv/                   # Python virtual environment
├── artifacts/               # Saved models and other outputs
├── chroma_db/               # Directory for the Chroma vector database
│   ├── 297bedb2-e5e8-43c5-a1ec-8923478b761b
│   └── chroma.sqlite3
├── data/                    # For storing datasets
├── .gitignore               # Files and folders to ignore in Git
├── requirements.txt         # Project dependencies
├── EDA_PP_recomm_system.ipynb   # Exploratory Data Analysis and Preprocessing Notebook
└── recommendation_system.ipynb  # Main recommendation system notebook

---

## 🚀 Getting Started

### Prerequisites

* Python 3.x
* `pip`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    # On macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    
    # On Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 💻 Usage

* **Exploratory Data Analysis:** Run the `EDA_PP_recomm_system.ipynb` notebook to explore the data and perform any necessary preprocessing.
* **Run the Recommendation System:** Execute the `recommendation_system.ipynb` notebook to train the model and generate recommendations.

---

## 📝 Key Features

* **Data Analysis:** Analyzes the dataset to gain insights.
* **Preprocessing:** Cleans and prepares the data for the model.
* **Vector Database:** Uses Chroma to store and retrieve data embeddings.
* **Recommendation Engine:** Generates personalized recommendations using an LLM.

---