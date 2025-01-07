import streamlit as st
import pandas as pd
import base64
import random
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(
    page_title="AI & ML Readiness Assessment",
    layout="wide",
    page_icon=":robot_face:"
)

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
    .quote-and-question {
        margin: 0 !important; 
        padding: 0 !important;
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

quotes = [
    "\"AI will continue to grow in 2025, but workplaces must accompany implementation with regular AI literacy and fluency training.\" [1]",
    "\"By 2025, company leaders will no longer have the luxury of addressing AI governance inconsistently or in pockets.\" [5]",
    "\"Rigorous assessment and validation of AI risk management practices and controls will become nonnegotiable.\" [5]",
    "\"Generative AI and AI-driven analytics are set to transform automated customer service by 2025.\" [4]",
    "\"Small businesses can join in, using AI to create personalized customer service with less effort and wider reach.\" [4]",
    "\"The countries with the highest robot density have among the lowest unemployment rates; it's about tech plus people.\" [6]",
    "\"AI is sometimes incorrectly framed as machines replacing humans. It's about machines augmenting humans.\" [6]",
    "\"Systematic, transparent approaches will be needed to confirm sustained value from AI investments.\" [5]",
    "\"Integration with legacy systems can be as tricky as navigating a thorny patch, but it's essential.\" [3]",
]

snippets = [
    "An AI strategist can help clarify goals to avoid wasted AI investments and ensure strategic alignment.",
    "Vendor-agnostic approaches reduce licensing fees and hidden service charges across the organization.",
    "Organizations strategically scaling AI report up to 3x the return compared to siloed implementations.",
    "Customizing AI solutions from the start avoids the high cost of adapting off-the-shelf platforms.",
    "Implementing solutions internally can save millions by eliminating ongoing licensing or user fees.",
    "Alignment with internal data privacy standards mitigates compliance risks and unforeseen costs.",
    "Regular AI assessments improve ROI by identifying new opportunities and preventing project stagnation.",
    "Robust data pipelines can cut operational costs by up to 19% in supply chain optimization[5].",
    "Internal training programs enable a self-sufficient AI culture, minimizing reliance on external vendors."
]

def generate_insights(scores):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_category, _ = sorted_scores[0]
    bottom_category, _ = sorted_scores[-1]

    insights = []
    insights.append(
        f"Your organization shows the highest potential in **{top_category}**. "
        "This suggests strengths that can be leveraged for larger AI initiatives, "
        "such as focusing resources or pilot projects in this area first."
    )
    insights.append(
        f"Meanwhile, **{bottom_category}** appears to have the greatest room for growth. "
        "By addressing potential gaps here, your organization can create "
        "a more balanced AI strategy with fewer blind spots."
    )
    insights.append(
        "Consider using cross-functional teams to promote alignment among stakeholders, "
        "and continuously revisit your strategy to ensure projects stay relevant."
    )
    insights.append(
        "Encourage ongoing AI literacy programs, build strong data governance, "
        "and track measurable outcomes—this will help you scale sustainably over time."
    )
    return "\n\n".join(insights)

def generate_pdf_report(scores, insights):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI & ML Readiness Assessment Report", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Overview of Findings:", styles['Heading2']))
    story.append(Paragraph(
        "Based on your responses, we've identified key areas that reflect how prepared your "
        "organization may be for AI implementation. Below you'll find a qualitative assessment "
        "of your organization's strongest aspects, along with areas that may require additional "
        "focus or resources.",
        styles['BodyText']
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Overall Insights and Recommendations:", styles['Heading2']))
    story.append(Paragraph(insights, styles['BodyText']))

    doc.build(story)
    buffer.seek(0)
    return buffer

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
        st.write(
            "**Based on Proven Scientific Algorithms**\n\n"
            "This assessment uses foundational principles similar to established behavioral and "
            "organizational research, enhanced by Retrieval-Augmented Generation (RAG) and advanced "
            "machine learning. By leveraging AI capabilities, organizations can develop custom strategic "
            "personality assessments at a fraction of the typical market cost.\n\n"
            "**ROI Potential**\n"
            "- Elimination of per-assessment costs ($24-100 per person)\n"
            "- Reduced training and development expenses\n"
            "- Improved team productivity through better role alignment\n\n"
            "**Core Pillars**\n"
            "- Scientific validation\n"
            "- Detailed reporting capabilities\n"
            "- Integration with existing systems\n"
            "- Reliable data collection methods\n"
        )

        if st.button("Begin Assessment"):
            st.session_state.questions = load_questions()
            st.session_state.started = True

    elif st.session_state.current_question < len(st.session_state.questions):
        q_index = st.session_state.current_question
        question_data = st.session_state.questions[q_index]

        # Quote box
        quote_text = quotes[q_index] if q_index < len(quotes) else random.choice(quotes)
        st.markdown(f"<div class='quote-box'>{quote_text}</div>", unsafe_allow_html=True)

        # Directly display question in question-card
        st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="question-header">Question {q_index + 1}</div>', unsafe_allow_html=True)
        st.write(question_data["question"])

        st.write(
            "Reflect on how this aspect of AI/ML readiness applies to your organization. "
            "Consider strategic goals, potential roadblocks, and the internal alignment of teams."
        )

        if q_index < len(snippets):
            st.markdown(f"**{snippets[q_index]}**")

        st.radio(
            "Select your response:",
            [
                "1 - Strongly Disagree",
                "2 - Disagree",
                "3 - Neutral",
                "4 - Agree",
                "5 - Strongly Agree"
            ],
            key="selected_option",
            on_change=on_response_change
        )
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("## Assessment Completed!")
        df_scores = pd.DataFrame({"Score": list(st.session_state.scores.values())},
                                 index=st.session_state.scores.keys())
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown('<div class="metrics-title">Overall Assessment Snapshot</div>', unsafe_allow_html=True)
        st.bar_chart(df_scores)

        insights_text = generate_insights(st.session_state.scores)
        st.markdown("### Comprehensive Insights and Recommendations:")
        st.markdown(insights_text)
        st.markdown('</div>', unsafe_allow_html=True)

        pdf = generate_pdf_report(st.session_state.scores, insights_text)
        b64 = base64.b64encode(pdf.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="AI_ML_Readiness_Report.pdf"><strong>Download PDF Report</strong></a>'
        st.markdown(href, unsafe_allow_html=True)

        if st.button("Restart Assessment"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]

if __name__ == "__main__":
    main()
