from backend.backend_recomm_sys import UNIQUE_LANGUAGES, UNIQUE_SUBCATEGORIES
from frontend.helper import format_course_results, process_ai_search, process_filter_search
import gradio as gr

def reset_all_filters():
    """Resets all UI inputs to their default states."""
    return "", "All", 1000.0, "All", "All", "All", 0.0, "Most Relevant", 5, ""

with gr.Blocks(title="AI Course Recommender") as demo:
    gr.Markdown("# 🎓 AI Course Recommendation Engine")  # Markdown is created first which will be at top

    with gr.Row():
        # LEFT COLUMN: All Filter Widgets + Filter & Reset Buttons
        with gr.Column(scale=1):
            user_query = gr.Textbox(label="Search Query",placeholder="e.g., python, machine learning, web development") 
            is_paid = gr.Dropdown(choices=["All", "Free", "Paid"],value="All",label="Course Type")
            max_price = gr.Number(value=1000.0,label="Max Price ($)")
            language = gr.Dropdown(choices=UNIQUE_LANGUAGES,value="All",label="Language")
            subcategory = gr.Dropdown(choices=UNIQUE_SUBCATEGORIES,value="All",label="Subcategory")
            duration = gr.Dropdown(choices=["All", "Short", "Medium", "Long"],value="All",label="Duration")
            min_rating = gr.Slider(minimum=0.0,maximum=5.0,value=0.0,step=0.5,label="Min Rating (Stars)")
            sort_by = gr.Dropdown(choices=["Most Relevant", "Latest First"],value="Most Relevant",label="Sort By")
            top_k = gr.Slider(minimum=1,maximum=10,value=5,step=1,label="Number of Results")

        with gr.Row():
            filter_search_btn = gr.Button("🎛️ Search by Filters", variant="primary")
            reset_btn = gr.Button("🔄 Reset Filters")

        # RIGHT COLUMN: Output Box + AI Query Search Button Below It
        with gr.Column(scale=2):
            output_box = gr.Textbox(label="Recommended Courses", lines=18, interactive=False)
            ai_search_btn = gr.Button("🤖 Search by AI Query", variant="primary")

    # 3. Connect Button Click to Function
    filter_search_btn.click(fn=process_filter_search, inputs=[user_query,is_paid,max_price,language,subcategory,duration,min_rating,sort_by,top_k], outputs=output_box)
    ai_search_btn.click(fn=process_ai_search, inputs=[user_query], outputs=output_box)
    reset_btn.click(fn=reset_all_filters,inputs=[], outputs=[user_query,is_paid,max_price,language,subcategory,duration,min_rating,sort_by,top_k])

if __name__ == "__main__":
    demo.launch()