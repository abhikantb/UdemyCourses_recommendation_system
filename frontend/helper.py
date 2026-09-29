from backend.backend_recomm_sys import get_courses,generate_intro, generate_outro  # Imports your notebook main function

def process_filter_search(query, is_paid, max_price, language, subcategory, duration, min_rating, sort_by, top_k):
    """Complete Bridge Function: Accepts all 8 UI widget inputs and maps them directly to backend's ui_filters dictionary."""
    ui_filters = {
        "is_paid": is_paid,     "max_price": float(max_price),
        "language": language,   "subcategory": subcategory,
        "duration": duration,   "min_rating": float(min_rating),
        "sort_by": sort_by,     "top_k": int(top_k)
    }    
    courses = get_courses(user_prompt=query, ui_filters=ui_filters) #passes query and full filter dictionary to backend
    return format_course_results(query, courses)

def process_ai_search(query):
    """Searches purely via LLM intent extraction from the search query."""
    courses = get_courses(user_prompt=query, ui_filters=None)
    return format_course_results(query, courses)


# --- STEP 2: SIMPLE STRING FORMATTING ---
def format_course_results(query, courses):
    """Takes the list of courses and turns it into a simple text string."""
    if not courses:
        return "No courses found matching your criteria. Try changing your filters or query!" #If no courses were found, return a simple message

    # Getting intro and outro Texts
    query_text = query if query.strip() else "Recommended courses as per filters"
    intro_text = generate_intro(query_text, len(courses))
    outro_text = generate_outro(query_text)

    # Combine everything into one simple string using standard newlines (\n)
    output_text = intro_text + "\n\n"
    for idx, course in enumerate(courses, 1):
        output_text += f"Course {idx}: {course['title']} (Link: {course['course_url']})\n"
        output_text += f"Details: Price: {course['price']} | Rating: {course['avg_rating']}★ | Language: {course['language']} | Duration: {course['content_length_minutes']} mins | Enrolled: {course['num_subscribers']}\n\n"
    output_text += outro_text
    return output_text