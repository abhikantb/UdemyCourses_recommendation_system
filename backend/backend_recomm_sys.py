import json
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
from huggingface_hub import login,InferenceClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

EMBEDDING_MODEL='sentence-transformers/all-MiniLM-L6-v2'
LLM_MODEL_NAME = "Qwen/Qwen2.5-72B-Instruct"
# LLM_MODEL_NAME = "DeepSeek-R1-Distill-Qwen-32B"
HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(api_key=HF_TOKEN)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")
EXCEL_PATH = os.path.join(DATA_DIR, "udemy_data_cleaned.xlsx")

# #### Import embeddings and create vectorstore from database
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
vectorstore = Chroma(
    persist_directory=CHROMA_DIR,   # folder containing chroma.sqlite3
    embedding_function=embeddings
)
# #### All default search parameters
DEFAULT_SEARCH_FILTERS = {
    "query": "courses","is_paid": "All","max_price": 1000.0,"language": "All","subcategory": "All",
    "duration": "All","min_rating": 0.0,"sort_by": "Most Relevant","top_k": 5
}

# #### Filter Search by LLM
SYSTEM_PROMPT = """
You are an intent extraction engine for a course search tool.
Extract explicit search criteria from the user's query into JSON.

Valid values:
- "query": Cleaned semantic topic string (remove keywords like free, top, arabic, etc.).
- "is_paid": "Free", "Paid", or "All"
- "max_price": float (default 1000.0)
- "language": "English", "Arabic", "Chinese", etc., or "All"
- "duration": "Short", "Medium", "Long", or "All"
- "min_rating": float (0.0 to 5.0, default 0.0)
- "sort_by": "Latest First" or "Most Relevant"
- "top_k": integer (default 5)

Output ONLY raw JSON. No explanation, no markdown tags.
"""
def extract_llm_filters(user_query):
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ],
            max_tokens=250,
            temperature=0.0
        )
        return json.loads(response.choices[0].message.content.strip())
    except Exception:
        return {}

# #### Filter Search by UI/keywords
def search_courses(final_filters):
    search_k = max(int(final_filters["top_k"]) * 10, 50)
    raw_results = vectorstore.similarity_search(query=final_filters["query"], k=search_k)
    filtered_courses = []
    for doc in raw_results:
        meta = doc.metadata
        # Filter: Free vs Paid
        if final_filters["is_paid"] == "Free" and meta["is_paid"] != "Free":
            continue
        if final_filters["is_paid"] == "Paid" and meta["is_paid"] == "Free":
            continue
        # Filter: Max Price
        if final_filters["is_paid"] == "Paid" and float(meta["price"]) > float(final_filters["max_price"]):
            continue
        # Filter: Language
        if final_filters["language"] != "All" and meta["language"] != final_filters["language"]:
            continue
        # Filter: Subcategory
        if final_filters["subcategory"] != "All" and meta["subcategory"] != final_filters["subcategory"]:
            continue
        # Filter: Duration
        if final_filters["duration"] != "All" and meta["content_length_minutes"] != final_filters["duration"]:
            continue
        # Filter: Minimum Rating
        if float(meta["avg_rating"]) < float(final_filters["min_rating"]):
            continue
        # Map clean metadata
        filtered_courses.append({
            "title": meta["title"],
            "is_paid": meta["is_paid"],
            "price": "Free" if meta["is_paid"] == "Free" else f"${meta['price']}",
            "num_subscribers": meta["num_subscribers"],
            "avg_rating": round(float(meta["avg_rating"]), 2),
            "published_time": meta["published_time"],
            "subcategory": meta["subcategory"],
            "language": meta["language"],
            "course_url": meta["course_url"],
            "content_length_minutes": meta["content_length_minutes"]
        })
    if final_filters["sort_by"] == "Latest First":
        filtered_courses.sort(key=lambda x: x["published_time"], reverse=True)
    return filtered_courses[:final_filters["top_k"]] 
    # filtered_courses is a LIST of dictionaries e.g. [Dictionary for Course 1, Dictionary for Course 2 etc]

# #### Final function - calling both Filter search by LLM and filter search by UI/keywords
def get_courses(user_prompt="", ui_filters=None):
    final_filters = DEFAULT_SEARCH_FILTERS.copy()

    # 1. Update from UI choices
    if ui_filters:
        for key, value in ui_filters.items():
            if value is not None:
                final_filters[key] = value
        if user_prompt and user_prompt.strip():
            final_filters["query"] = user_prompt.strip()

    # 2. Update from LLM extraction if user entered a query string
    elif user_prompt and user_prompt.strip():
        llm_filters = extract_llm_filters(user_prompt)
        for key, value in llm_filters.items():
            if value:
                final_filters[key] = value

    # 3. Execute search
    return search_courses(final_filters)


# #### LLM Intro & Outro Generation
def generate_llm_response(prompt: str, max_tokens: int = 200) -> str:
    """Sends prompt to Hugging Face Inference API."""
    try:
        completion = client.chat.completions.create(
            model=LLM_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM API Error: {e}")
        return ""

def generate_intro(user_query: str, num_courses: int) -> str:
    prompt = f"Generate a friendly, brief conversational introduction for course recommendations. User Query: '{user_query}', Number of courses found: {num_courses}."
    response = generate_llm_response(prompt)
    return response if response else f"Here are the top {num_courses} courses matching your search:"

def generate_outro(user_query: str) -> str:
    prompt = f"Generate a brief closing sentence for a course recommendation list based on user query: '{user_query}'."
    response = generate_llm_response(prompt)
    return response if response else "Hope these recommendations help you find the right course!"



df = pd.read_excel(EXCEL_PATH)
# Extract unique values directly from DataFrame columns
UNIQUE_LANGUAGES = ["All"] + sorted(df["language"].dropna().unique().tolist())
UNIQUE_SUBCATEGORIES = ["All"] + sorted(df["subcategory"].dropna().unique().tolist())
