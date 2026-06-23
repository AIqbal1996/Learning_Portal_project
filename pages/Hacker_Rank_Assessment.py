import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="HackerRank Assessment",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    body, .main, .block-container {
        background-color: white !important;
    }
    /* White text in sidebar */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    /* All markdown texts, subheaders, and bullet points in black */
    .stMarkdown, .stMarkdown *, .main h2, .main h2 *, .main h3, .main h3 *, .main h4, .main h4 *, .main h5, .main h5 * {
        color: black !important;
    }
    /* Ensure children inside tabs inherit the tab's specific color */
    .stTabs [data-baseweb="tab"] * {
        color: inherit !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        padding: 0.5rem 1.5rem;
        background-color: white;
        border-radius: 10px;
        border: 2px solid #2575FC;
        font-size: 1.3rem;
        font-weight: 700;
        color: black !important;
        box-shadow: 0 2px 6px rgba(37, 117, 252, 0.1);
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #ebf3fe;
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(37, 117, 252, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2575FC !important;
        color: white !important;
        border-color: #2575FC !important;
    }
</style>
""", unsafe_allow_html=True)

# Back to Home Button
if st.button("← Back to Home"):
    st.switch_page("home_page.py")

st.markdown('<h1 style="color: #E74C3C;">💻 HackerRank Assessment</h1>', unsafe_allow_html=True)
#st.markdown("---")

try:
    # Read from local Hacker_Rank_assessments.xlsx file
    excel_file_path = "Hacker_Rank_assessments.xlsx"
    
    if not os.path.exists(excel_file_path):
        st.error("❌ Hacker_Rank_assessments.xlsx file not found!")
        st.stop()
    
    # Load all sheet names from the Excel file
    excel_file = pd.ExcelFile(excel_file_path)
    sheet_names = excel_file.sheet_names
    
    # Add instruction text
    st.markdown("### 📊 Select the assessment sheet below")
    
    # Create tabs for each sheet
    tabs = st.tabs(sheet_names)
    
    for idx, (tab, sheet_name) in enumerate(zip(tabs, sheet_names)):
        with tab:
            try:
                # Read the specific sheet
                df_sheet = pd.read_excel(excel_file_path, sheet_name=sheet_name)
                
                # # Sheet title
                # st.subheader(f"📋 {sheet_name}")
                # st.markdown("---")
                
                # Add search functionality
                search_term = st.text_input(
                    f"🔍 Search in {sheet_name}...", 
                    key=f"search_{sheet_name}",
                    placeholder=f"Search across all data in {sheet_name}"
                )
                
                # Filter based on search term
                if search_term:
                    filtered_df = df_sheet[df_sheet.astype(str).apply(
                        lambda x: x.str.contains(search_term, case=False, na=False)
                    ).any(axis=1)]
                    st.info(f"📊 Showing {len(filtered_df)} of {len(df_sheet)} rows")
                else:
                    filtered_df = df_sheet
                
                # Display the table
                st.dataframe(
                    filtered_df,
                    use_container_width=True,
                    height=500
                )
                
                # Download option
                csv_data = filtered_df.to_csv(index=False)
                st.download_button(
                    label=f"📥 Download {sheet_name} as CSV",
                    data=csv_data,
                    file_name=f"{sheet_name}.csv",
                    mime="text/csv",
                    key=f"download_{sheet_name}"
                )
                
            except Exception as e:
                st.error(f"❌ Error reading sheet '{sheet_name}': {str(e)}")

except FileNotFoundError:
    st.error("❌ Hacker_Rank_assessments.xlsx file not found in the project directory.")
except Exception as e:
    st.error(f"❌ An error occurred while loading the file: {str(e)}")

st.markdown("---")
st.info("💡 **Tips:**\n- Use tabs above to switch between different assessment sheets\n- Search within each sheet to filter data\n- Download each sheet as CSV for external use")
