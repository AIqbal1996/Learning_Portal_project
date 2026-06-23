import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Training List",
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

# Custom CSS for tabs
st.markdown("""
<style>
    body, .main, .block-container {
        background-color: white !important;
    }

    /* All markdown texts, headers, and bullet points in black */
    .stMarkdown, .stMarkdown * {
        color: black !important;
    }

    /* All form/search labels in black */
    .main label {
        color: black !important;
    }

    /* Ensure children inside tabs inherit the tab's specific color */
    .stTabs [data-baseweb="tab"] * {
        color: inherit !important;
    }

    /* White text in sidebar */
    [data-testid="stSidebar"] * {
        color: white !important;
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
        color: #2575FC !important;
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
col1, col2, col3 = st.columns([1, 1, 5])
with col1:
    if st.button("← Back to Home"):
        st.switch_page("home_page.py")

# Title
st.markdown('<h1 style="color: #FF9F1C;">📖 Training List</h1>', unsafe_allow_html=True)
#st.markdown("---")

# Description
# st.markdown("""
# This page displays training data from sheets in the Courses.xlsx file.
# Each sheet is shown as a searchable table with CSV download support.
# """)

try:
    # Read from local Courses.xlsx file
    excel_file_path = "Courses.xlsx"
    
    if not os.path.exists(excel_file_path):
        st.error("❌ Courses.xlsx file not found!")
        st.warning("""
        **To use this page:**
        1. Download the Excel file from SharePoint
        2. Save it as `Courses.xlsx` in the project directory
        3. Reload this page
        """)
        st.stop()
    
    # Load all sheet names from the Excel file
    excel_file = pd.ExcelFile(excel_file_path)
    sheet_names = excel_file.sheet_names
    
    # # Display sheets
    # st.markdown("---")
    
    # Add instruction text
    st.markdown("### 📚 Select the course below")
    
    # Create tabs for each sheet with larger styling
    tab_labels = [f"<h3 style='text-align: center; padding: 10px;'>📊 {sheet}</h3>" for sheet in sheet_names]
    tabs = st.tabs(sheet_names)
    
    for idx, (tab, sheet_name) in enumerate(zip(tabs, sheet_names)):
        with tab:
            try:
                # Read the specific sheet
                df_sheet = pd.read_excel(excel_file_path, sheet_name=sheet_name)
                
                # Sheet title
                # st.subheader(f"📋 {sheet_name}...")
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
    st.error("❌ Courses.xlsx file not found in the project directory.")
except Exception as e:
    st.error(f"❌ An error occurred while loading the file: {str(e)}")

st.markdown("---")
st.info("💡 **Tips:**\n- Use tabs above to switch between sheets\n- Search within each sheet to filter data\n- Download each sheet as CSV for external use")
