import streamlit as st

st.set_page_config(
    page_title="HCL Learning Portal Hub",
    layout="wide"
)

st.markdown(
    """
    <style>
        /* White text in sidebar */
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        body, .main, .block-container {
            background-color: white !important;
        }
        p, div, span, li {
            color: black !important;
        }

        /* Green buttons for both columns */
        div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
            background-color: #27AE60 !important;
            color: white !important;
            border: 1px solid #1e8449 !important;
        }
        div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button:hover {
            background-color: #1e8449 !important;
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit auto-generates a sidebar for multi-page apps (pages/ folder).
# This CSS hides that auto-generated sidebar and its toggle button.
# st.markdown("""
#     <style>
#         [data-testid="stSidebar"] {display: none;}
#         [data-testid="collapsedControl"] {display: none;}
#     </style>
# """, unsafe_allow_html=True)

# Banner and Title
#st.image("assets/banner.png", use_column_width=True)
st.markdown('<h1 style="color: #2575FC;">📚 HCL Learning Portal Hub</h1>', unsafe_allow_html=True)
st.markdown("---")

# # Introduction
# st.markdown("""
# Welcome to the HCL HCL HCL HCL Learning Portal! Choose an option below to explore different sections.
# """)

# Create two columns for navigation links
col1, col2 = st.columns(2)

with col1:
    st.markdown('<h3 style="color: #27AE60;">🎓 Courses</h3>', unsafe_allow_html=True)
    st.markdown("""
    Browse and explore our comprehensive collection of courses.
    """)
    if st.button("Go to Courses", key="btn_courses"):
        st.switch_page("pages/Courses.py")

with col2:
    st.markdown('<h3 style="color: #FF9F1C;">📖 Training List</h3>', unsafe_allow_html=True)
    st.markdown("""
    View and manage the complete training list.
    """)
    if st.button("Go to Training List", key="btn_training"):
        st.switch_page("pages/Training_list.py")

st.markdown("<br>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown('<h3 style="color: #2575FC;">🚀 Pilots</h3>', unsafe_allow_html=True)
    st.markdown("""
    Explore and track the pilot programs and initiatives.
    """)
    if st.button("Go to Pilots", key="btn_pilots"):
        st.switch_page("pages/Pilots.py")

with col4:
    st.markdown('<h3 style="color: #E74C3C;">💻 HackerRank Assessment</h3>', unsafe_allow_html=True)
    st.markdown("""
    Practice and complete your technical and HackerRank assessments.
    """)
    if st.button("Go to Assessment", key="btn_hackerrank"):
        st.switch_page("pages/Hacker_Rank_Assessment.py")

# Footer
st.markdown("---")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")
st.markdown(" ")

st.markdown("### About This Portal")
st.info("""
This HCL  Learning Portal helps you discover and track various training resources and courses.
""")
