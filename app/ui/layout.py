"""
Layout configuration and page setup
"""

import streamlit as st
from config.ui_text import TITLE


def setup_page():
    """Configure page settings and layout"""
    st.set_page_config(
        page_title=TITLE,
        layout="wide",  # Use wide but add margins with columns
        initial_sidebar_state="collapsed",  # No sidebar
    )

    # Custom CSS for better styling
    st.markdown(
        """
        <style>
        /* Hide sidebar */
        section[data-testid="stSidebar"] {
            display: none;
        }
        
        /* Main container padding */
        .main {
            padding-top: 1rem;
        }
        
        /* Center the main title */
        h1 {
            text-align: center !important;
        }
        
        /* Center the tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
            justify-content: center !important;
        }
        
        /* Center Step headers */
        h2 {
            text-align: center !important;
        }
        
        /* Add spacing after all subheaders */
        .stMarkdown h3 {
            margin-bottom: 1.5rem !important;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding-left: 20px;
            padding-right: 20px;
            background-color: white;
            border-radius: 5px 5px 0 0;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #ff2b2b;
            color: white;
        }
        
        /* Button styling - Red primary buttons */
        div.stButton > button[kind="primary"] {
            background-color: #ff2b2b;
            border-color: #ff2b2b;
        }
        
        div.stButton > button[kind="primary"]:hover {
            background-color: #C82333;
            border-color: #BD2130;
        }
        
        div.stButton > button {
            width: 100%;
        }
        
        /* File uploader styling */
        .uploadedFile {
            background-color: #f0f2f6;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
        }
        
        /* Success message styling */
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            padding: 10px;
            color: #155724;
        }
        
        /* Error message styling */
        .error-box {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            padding: 10px;
            color: #721c24;
        }
        
        /* Warning message styling */
        .warning-box {
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            border-radius: 5px;
            padding: 10px;
            color: #856404;
        }
        
        /* Pink notice for calculation errors */
        .pink-notice {
            background-color: #FFE4E1;
            border: 1px solid #FFB6C1;
            border-radius: 5px;
            padding: 15px;
            color: #8B0000;
            margin: 15px 0;
        }
        
        /* Center align for certain elements */
        .center-content {
            text-align: center;
        }
        
        /* Portfolio list box */
        .portfolio-list {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
            font-family: monospace;
            max-height: 200px;
            overflow-y: auto;
        }
        
        /* Metric display */
        .metric-container {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #ff2b2b;
        }
        
        .metric-label {
            font-size: 1.2em;
            color: #666;
            margin-top: 5px;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


def show_header():
    """Display application header - centered"""
    st.title(TITLE)
    st.markdown("---")


def show_subheader(text: str):
    """Display subheader with consistent spacing after it"""
    st.subheader(text)
    # The CSS handles the spacing automatically now


def create_columns(ratios: list = None, gap: str = "medium"):
    """
    Create columns with specified ratios and gap between them

    Args:
        ratios: List of column width ratios (default [1, 1])
        gap: Gap size - "small", "medium", or "large" (default "medium")
    """
    if ratios is None:
        ratios = [1, 1]

    # Add margins for medium width layout
    _, center, _ = st.columns([10, 25, 10])  # Create side margins

    with center:
        # Add gap between columns by inserting spacer columns
        if len(ratios) == 2 and gap:
            # For 2 columns, add a spacer in the middle
            gap_size = {"small": 0.1, "medium": 0.2, "large": 0.3}.get(gap, 0.2)
            adjusted_ratios = [ratios[0], gap_size, ratios[1]]
            cols = st.columns(adjusted_ratios)
            return cols[0], cols[2]  # Return only the content columns, skip the gap
        else:
            # For other configurations, return as is
            return st.columns(ratios)


def create_columns_with_gap(
    left_ratio: float = 1, right_ratio: float = 1, gap_ratio: float = 0.2
):
    """
    Alternative method: Create two columns with explicit gap control

    Args:
        left_ratio: Width ratio for left column
        right_ratio: Width ratio for right column
        gap_ratio: Width ratio for gap between columns
    """
    # Add margins for medium width layout
    _, center, _ = st.columns([10, 25, 10])

    with center:
        col1, _, col2 = st.columns([left_ratio, gap_ratio, right_ratio])
        return col1, col2


def create_content_container():
    """Create a centered content container"""
    _, center, _ = st.columns([10, 25, 10])  # 1:6:1 ratio
    return center


def add_vertical_space(lines: int = 1):
    """Add vertical spacing"""
    for _ in range(lines):
        st.write("")


def show_divider():
    """Show a horizontal divider"""
    st.markdown("---")
