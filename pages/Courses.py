import streamlit as st
import pandas as pd
from urllib.parse import urlencode, quote
import re

def get_href(link_text):
    """Return a navigable URL from a CSV link value."""
    link_text = link_text.strip()
    if not link_text:
        return ""
    
    # Extract embedded URL if present anywhere in the text
    url_match = re.search(r'https?://\S+', link_text)
    if url_match:
        return url_match.group(0).rstrip(";,).")
    
    # Strip any trailing ellipsis
    if link_text.endswith("…"):
        link_text = link_text[:-1].strip()
    elif link_text.endswith("..."):
        link_text = link_text[:-3].strip()

    # # Extract the content name after 'Percipio <Type>' prefix
    # for prefix in ["Percipio Track", "Percipio Journey", "Percipio Channel",
    #                "Percipio Course", "Percipio Book", "Percipio Content",
    #                "Percipio Video", "Percipio"]:
    #     if link_text.startswith(prefix):
    #         query = link_text[len(prefix):].strip()
    #         return f"https://hclcontent.percipio.com/search?{urlencode({'q': query})}"
    # return f"https://hclcontent.percipio.com/search?{urlencode({'q': link_text})}"


st.set_page_config(
    page_title="Data Engineering Learning Portal",
    layout="wide"
)

# Streamlit auto-generates a sidebar for multi-page apps (pages/ folder).
# This CSS hides that auto-generated sidebar and its toggle button.
# st.markdown("""
#     <style>
#         [data-testid="stSidebar"] {display: none;}
#         [data-testid="collapsedControl"] {display: none;}
#     </style>
# """, unsafe_allow_html=True)

# Back to Home Button
if st.button("← Back to Home"):
    st.switch_page("home_page.py")

# -----------------------------
# Sample Data
# -----------------------------


df = pd.read_csv("Courses.csv", usecols=["Course Name", "Link", "Duration(Hr)"])
df = df.dropna(subset=["Course Name"])
df["Duration(Hr)"] = pd.to_numeric(df["Duration(Hr)"], errors="coerce").fillna(0)
df = df.reset_index(drop=True)

# Category Filtering Mapping
CATEGORY_MAPPING = {
    "Data Engineering": [
        "Data Engineering", "Data Architecture", "Data Warehouse", "ETL", 
        "DataOps", "MLOps", "Data Mangement", "Datastage", "Airflow", "Data Science", "GCP Data Engineer",
        "PubSub", "Dataproc"
    ],
    "Azure": [
        "Azure", "Cosmos DB", "Logic App", "MS Fabric", "SSAS & SSIS", "PubSub"
    ],
    "AWS": [
        "AWS"
    ],
    "Spark": [
        "Spark", "PySpark", "Scala", "Hadoop", "Dataproc"
    ],
    "Snowflake": [
        "Snowflake"
    ],
    "Power BI": [
        "Power BI", "Power Platform", "Power Automate", "Power Apps", "Tableau"
    ],
    "SQL": [
        "SQL", "MySQL", "Postgre", "MongoDB", "Teradata", "Kustos", "BigQuery"
    ]
}

selected_category = st.query_params.get("category", "All")

if selected_category != "All":
    keywords = CATEGORY_MAPPING.get(selected_category, [])
    if keywords:
        pattern = "|".join(keywords)
        df = df[df["Course Name"].str.contains(pattern, case=False, na=False)]
        df = df.reset_index(drop=True)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
body, .main, .block-container {
    background-color: white !important;
}

/* White text in sidebar */
[data-testid="stSidebar"] * {
    color: white !important;
}

.main {
    padding-top:0rem;
}

.hero {
    background: white;
    padding:40px;
    border-radius:15px;
    color:#333;
    text-align:center;
    border: 1px solid #ddd;
}

.hero h1{
    font-size:42px;
}

.hero p{
    font-size:18px;
    color:#555;
}

.skill-pill{
    display:inline-block;
    padding:10px 20px;
    margin:5px;
    border-radius:25px;
    background:white;
    color:#2575FC !important;
    border: 1px solid #ddd;
    font-weight:600;
    text-decoration:none;
    transition: all 0.2s ease;
}

.skill-pill:hover{
    background:#f7f7f7;
    transform: translateY(-2px);
    box-shadow: 0px 4px 8px rgba(0,0,0,0.15);
}

.active-skill-pill{
    display:inline-block;
    padding:10px 20px;
    margin:5px;
    border-radius:25px;
    background:white;
    color:#2575FC !important;
    font-weight:600;
    text-decoration:none;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
    transform: translateY(-2px);
}

.course-card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.1);
    margin-bottom:20px;
    min-height:260px;
}

.course-title{
    font-size:20px;
    font-weight:bold;
    color:#333;
}

.duration{
    color:#6A11CB;
    font-weight:bold;
    font-size:18px;
}

.launch-btn{
    background:#2575FC;
    color:white !important;
    padding:8px 16px;
    border-radius:8px;
    text-decoration:none;
    display:inline-block;
    font-weight:600;
    transition: background 0.2s ease;
}

.launch-btn:hover{
    background:#1a5fd6;
}

.launch-btn-disabled{
    background:#e0e0e0;
    color:#999 !important;
    padding:8px 16px;
    border-radius:8px;
    display:inline-block;
    font-weight:600;
    cursor:not-allowed;
}

.course-link{
    font-size:12px;
    color:#555;
    word-break:break-all;
    margin-top:8px;
    line-height:1.4;
}

.course-link a{
    color:#2575FC;
    text-decoration:underline;
    word-break:break-all;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Banner
# -----------------------------
skills = ["All", "Data Engineering", "Azure", "AWS", "Spark", "Snowflake", "Power BI", "SQL"]
pills_html = []
for skill in skills:
    is_active = (selected_category == skill)
    pill_class = "active-skill-pill" if is_active else "skill-pill"
    escaped_skill = quote(skill)
    pills_html.append(f"<a href='?category={escaped_skill}' target='_self' class='{pill_class}'>{skill}</a>")

pills_str = "\n".join(pills_html)

st.markdown('<h2 style="color: #2575FC; margin-bottom: 20px;">📚 Courses</h2>', unsafe_allow_html=True)

st.markdown(f"""
<div class='hero'>
<h1>Data Engineering Capability</h1>
<p>Upskilling and Reskilling Program</p>
<div style='margin-top:20px;'>
{pills_str}
</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# -----------------------------
# Search
# -----------------------------
search = st.text_input(
                    "🔍 Search Course", 
                    key=f"search",
                    placeholder="Search all data in Courses"
                )

if search:
    df = df[df["Course Name"].str.contains(search, case=False)]
    df = df.reset_index(drop=True)

# -----------------------------
# Course Cards (one card = one CSV row = one link)
# -----------------------------
cols = st.columns(3)

for idx, row in df.iterrows():
    col = cols[idx % 3]

    link_val = str(row["Link"]).strip() if pd.notna(row["Link"]) else ""
    href = get_href(link_val)

    if href:
        short_link = link_val[:55] + "..." if len(link_val) > 55 else link_val
        btn_html = (
            f'<a href="{href}" target="_blank" class="launch-btn" '
            f'style="display:block;text-decoration:none;margin-top:12px;">'
            f'🚀 Launch Course<br>'
            f'<small style="font-weight:400;font-size:11px;opacity:0.85;">{short_link}</small>'
            f'</a>'
        )
    else:
        btn_html = '<span class="launch-btn-disabled" style="margin-top:12px;display:inline-block;">🔗 No Link</span>'

    with col:
        st.markdown(f"""
        <div class='course-card'>
            <div class='course-title'>{row['Course Name']}</div>
            <div class='duration' style='margin-top:8px;'>⏱ Duration: {row['Duration(Hr)']} Hours</div>
            {btn_html}
        </div>
        """, unsafe_allow_html=True)



# -----------------------------
# Summary
# -----------------------------
# --------------------------------------------------
# Metrics
# --------------------------------------------------
total_courses = len(df)
total_hours = df["Duration(Hr)"].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="📚 Total Courses",
        value=total_courses
    )

with col2:
    st.metric(
        label="⏱ Total Learning Hours",
        value=f"{total_hours:.0f} Hours"
    )

st.write("")
