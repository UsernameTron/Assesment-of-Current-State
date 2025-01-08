import streamlit as st
import pandas as pd
import base64
import random

st.set_page_config(
    page_title="AI & ML Readiness Assessment",
    layout="wide",
    page_icon=":robot_face:"
)

# Minor style adjustments
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F7F9FC;
        max-width: 1000px;
        margin: auto;
        padding: 20px;
        border-radius: 10px;
    }
    html, body, [data-testid="stMarkdownContainer"] {
        color: #232323 !important;
    }
    h1, h2, h3, h4, h5, h6, .question-header, .metrics-title {
        color: #1A1A1A !important;
        font-weight: 600;
    }
    .stButton>button {
        background: linear-gradient(135deg, #00C9FF, #92FE9D);
        color: #000;
        font-weight: bold;
        border: none;
        border-radius: 4px;
        padding: 0.6rem 1.2rem;
    }
    .quote-box {
        background-color: #ffffff;
        border-left: 4px solid #007ACC;
        padding: 10px 15px;
        margin-bottom: 5px;
        color: #2B2B2B;
        font-style: italic;
        font-size: 0.95rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-radius: 4px;
    }
    .question-card {
        background-color: #FFFFFF;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 20px 25px 10px 25px;
        border-radius: 10px;
        margin: 0 !important;
    }
    .result-card {
        background-color: #FFFFFF;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 25px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .stRadio label {
        font-size: 16px;
        color: #333333 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def initialize_session():
    if "started" not in st.session_state:
        st.session_state.started = False
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "scores" not in st.session_state:
        st.session_state.scores = {"Strategy": 0, "Execution": 0, "Culture": 0, "Data": 0}
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None

initialize_session()

def load_questions():
    return [
        {
            "question": "How clearly has your organization defined a strategic vision for AI and ML?",
            "mapping": {"Strategy": 2, "Execution": 1, "Culture": 0, "Data": 0},
        },
        {
            "question": "How confident are you in your current team’s ability to deploy and maintain AI solutions?",
            "mapping": {"Strategy": 1, "Execution": 2, "Culture": 0, "Data": 0},
        },
        {
            "question": "How do you gauge overall enthusiasm and acceptance of AI initiatives in your organizational culture?",
            "mapping": {"Strategy": 0, "Execution": 0, "Culture": 2, "Data": 1},
        },
        {
            "question": "How well-prepared are your data collection methods to support AI projects?",
            "mapping": {"Strategy": 0, "Execution": 0, "Culture": 1, "Data": 2},
        },
        {
            "question": "Are your stakeholders aligned on AI priorities and potential ROI?",
            "mapping": {"Strategy": 2, "Execution": 1, "Culture": 1, "Data": 0},
        },
        {
            "question": "Does your organization have a clear plan for addressing data privacy and compliance in AI projects?",
            "mapping": {"Strategy": 0, "Execution": 1, "Culture": 1, "Data": 2},
        },
        {
            "question": "How frequently do you reassess AI initiatives for strategic relevance?",
            "mapping": {"Strategy": 2, "Execution": 0, "Culture": 1, "Data": 0},
        },
        {
            "question": "How robust is your infrastructure for large-scale data processing?",
            "mapping": {"Strategy": 0, "Execution": 1, "Culture": 0, "Data": 2},
        },
        {
            "question": "Do you regularly train employees on AI best practices and innovations?",
            "mapping": {"Strategy": 0, "Execution": 2, "Culture": 2, "Data": 0},
        },
    ]

# Sample quotes for demonstration
quotes = [
    "\"AI will continue to grow in 2025, but workplaces must accompany implementation with regular AI literacy.\" ",
    "\"By 2025, AI governance can't be addressed in pockets—holistic strategy is key.\" ",
    "\"Rigorous risk management practices for AI become nonnegotiable in fast-paced implementations.\" ",
    # ... You can add or remove more quotes as needed ...
]

snippets = [
    "An AI strategist clarifies goals and avoids wasted AI investments.",
    "Vendor-agnostic approaches reduce licensing fees and hidden service charges.",
    "Strategically scaling AI can yield up to 3x return over siloed implementations.",
    "Custom solutions from the start reduce expensive modifications later.",
    "Internal implementations can save millions by removing incremental user fees.",
    # ... More snippet lines if desired ...
]

def generate_insights(scores):
    # Provide a simple narrative based on top and bottom categories
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_cat, top_val = sorted_scores[0]
    bottom_cat, bottom_val = sorted_scores[-1]

    insights = []
    insights.append(
        f"**Highest Potential:** {top_cat}.\n"
        "This indicates an area where your organization can push forward with AI initiatives."
    )
    insights.append(
        f"**Greatest Room for Growth:** {bottom_cat}.\n"
        "By focusing on this aspect, you can create a more balanced AI strategy."
    )
    insights.append(
        "Consider cross-functional teams, ongoing AI literacy, and robust data governance "
        "to ensure sustainable AI adoption."
    )
    return "\n\n".join(insights)

def on_response_change():
    if st.session_state.selected_option is not None:
        current_q = st.session_state.current_question
        mapping = st.session_state.questions[current_q]["mapping"]
        options = [
            "1 - Strongly Disagree",
            "2 - Disagree",
            "3 - Neutral",
            "4 - Agree",
            "5 - Strongly Agree"
        ]
        response_value = options.index(st.session_state.selected_option) + 1
        for cat, weight in mapping.items():
            st.session_state.scores[cat] += weight * (response_value - 3)
        st.session_state.current_question += 1
        st.session_state.selected_option = None

def main():
    if not st.session_state.started:
        st.markdown("# Welcome to the AI & ML Readiness Assessment")
        st.write(
            "Evaluate your understanding of AI/ML strategies, execution capabilities, "
            "organizational culture, and data readiness. Identify gaps and explore ways "
            "to align your initiatives with long-term goals."
        )
        if st.button("Begin Assessment"):
            st.session_state.questions = load_questions()
            st.session_state.started = True

    elif st.session_state.current_question < len(st.session_state.questions):
        q_index = st.session_state.current_question
        question_data = st.session_state.questions[q_index]

        # Display the quote box (optional)
        if q_index < len(quotes):
            st.markdown(f"<div class='quote-box'>{quotes[q_index]}</div>", unsafe_allow_html=True)

        # Display the question and snippet
        st.markdown("<div class='question-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='question-header'>Question {q_index + 1}</div>", unsafe_allow_html=True)
        st.write(question_data["question"])
        st.write(
            "Reflect on how this aspect of AI/ML readiness applies to your organization. "
            "Consider strategic goals, potential roadblocks, and the internal alignment of teams."
        )
        if q_index < len(snippets):
            st.markdown(f"**{snippets[q_index]}**")

        st.radio(
            "Select your response:",
            ["1 - Strongly Disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly Agree"],
            key="selected_option",
            on_change=on_response_change
        )
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # Final results
        st.markdown("## Assessment Completed!")
        df_scores = pd.DataFrame(
            {
                "Score": list(st.session_state.scores.values())
            },
            index=st.session_state.scores.keys()
        )
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="metrics-title">Overall Assessment Snapshot</div>', unsafe_allow_html=True)
        st.bar_chart(df_scores)

        insights_text = generate_insights(st.session_state.scores)
        st.markdown("### Comprehensive Insights and Recommendations:")
        st.markdown(insights_text)
        st.markdown("</div>", unsafe_allow_html=True)

        # Optionally, remove PDF generation code entirely—no references to reportlab needed.

        if st.button("Restart Assessment"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]

if __name__ == "__main__":
    main()
