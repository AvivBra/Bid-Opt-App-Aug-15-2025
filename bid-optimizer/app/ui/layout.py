import streamlit as st


def apply_custom_css():
    """החלת סגנון CSS - Dark Mode with Violet Theme"""

    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
        <style>
        /* Import Inter Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Dark Mode Only - Violet Theme */
        
        /* Force Inter Font Everywhere */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }
        
        .stApp, .stApp * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        }
        
        /* Fix checkbox alignment */
        .stCheckbox {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stCheckbox > label {
            display: inline-flex !important;
            align-items: center !important;
            margin: 0 !important;
            padding: 2px 0 !important;
            line-height: 1.5 !important;
        }
        
        .stCheckbox input[type="checkbox"] {
            margin: 0 8px 0 0 !important;
            padding: 0 !important;
            vertical-align: middle !important;
        }
        
        /* Hide Streamlit Elements */
        header[data-testid="stHeader"] {
            background-color: transparent !important;
            height: 0 !important;
            visibility: hidden !important;
        }
        
        .stToolbar {
            display: none !important;
        }
        
        .stDeployButton {
            display: none !important;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Main App Background */
        .stApp {
            background-color: #0E1117 !important;
        }
        
        /* All Text Elements */
        h1, h2, h3, h4, h5, h6, p, span, div, label {
            color: #FAFAFA !important;
        }
        
        /* ALL Buttons - Violet */
        button, .stButton > button {
            background-color: #9B6BFF !important;
            color: white !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            font-weight: bold !important;
            border-radius: 4px !important;
            transition: all 0.2s ease !important;
        }
        
        button:hover, .stButton > button:hover {
            background-color: #B589FF !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(155, 107, 255, 0.3) !important;
        }
        
        button:active, .stButton > button:active {
            background-color: #7E4FE3 !important;
            transform: translateY(0) !important;
        }
        
        /* Section Headers with Violet Border */
        .section-header {
            border-bottom: 2px solid #9B6BFF !important;
            padding-bottom: 10px !important;
            margin-bottom: 20px !important;
            color: #FAFAFA !important;
            text-align: center !important;
            font-size: 24px !important;
            font-weight: bold !important;
        }
        
        /* Dark Card Containers */
        .section-container {
            margin-bottom: 40px !important;
            padding: 20px !important;
            background-color: #262730 !important;
            border-radius: 8px !important;
            border: 1px solid #333333 !important;
        }
        
        /* Checkboxes with Violet */
        input[type="checkbox"] {
            appearance: none !important;
            -webkit-appearance: none !important;
            width: 18px !important;
            height: 18px !important;
            border: 2px solid #4A4D55 !important;
            border-radius: 3px !important;
            background-color: transparent !important;
            cursor: pointer !important;
            margin-right: 8px !important;
            flex-shrink: 0 !important;
            vertical-align: middle !important;
        }
        
        input[type="checkbox"]:checked {
            background-color: #9B6BFF !important;
            border-color: #9B6BFF !important;
            position: relative !important;
        }
        
        input[type="checkbox"]:checked::after {
            content: '✓' !important;
            position: absolute !important;
            top: -2px !important;
            left: 2px !important;
            color: white !important;
            font-size: 14px !important;
            font-weight: bold !important;
        }
        
        input[type="checkbox"]:hover {
            border-color: #9B6BFF !important;
        }
        
        .stCheckbox > label {
            display: flex !important;
            align-items: center !important;
            cursor: pointer !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        .stCheckbox > label > div[data-testid="stMarkdownContainer"] {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stCheckbox > label > div[data-testid="stMarkdownContainer"] > p {
            color: #FAFAFA !important;
            margin: 0 !important;
            padding: 0 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        .stCheckbox:has(input:checked) > label > div[data-testid="stMarkdownContainer"] > p {
            color: #9B6BFF !important;
            font-weight: 500 !important;
        }
        
        /* File Uploader */
        [data-testid="stFileUploaderDropzone"] {
            background-color: #1A1D23 !important;
            border: 2px dashed #3A3D45 !important;
            color: #FAFAFA !important;
            transition: all 0.2s ease !important;
        }
        
        [data-testid="stFileUploaderDropzone"]:hover {
            background-color: #202329 !important;
            border-color: #9B6BFF !important;
        }
        
        .stFileUploader label {
            color: #FAFAFA !important;
        }
        
        .stFileUploader button {
            background-color: #3A3D45 !important;
            color: #FAFAFA !important;
        }
        
        .stFileUploader button:hover {
            background-color: #4A4D55 !important;
        }
        
        /* Progress Bar */
        .stProgress > div > div {
            background-color: #9B6BFF !important;
        }
        
        .stProgress {
            background-color: #2E3138 !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #262730 !important;
            border: 1px solid #333333 !important;
            color: #FAFAFA !important;
        }
        
        .streamlit-expanderContent {
            background-color: #262730 !important;
            border: 1px solid #333333 !important;
            color: #FAFAFA !important;
        }
        
        /* Alerts */
        .stAlert {
            background-color: #2A2D35 !important;
            border: 1px solid #3A3D45 !important;
            color: #FAFAFA !important;
        }
        
        div[data-baseweb="notification"] {
            background-color: #2A2D35 !important;
            border: 1px solid #3A3D45 !important;
        }
        
        div[data-baseweb="notification"] div {
            color: #FAFAFA !important;
        }
        
        /* Input Fields */
        .stTextInput > div > div > input {
            background-color: #262730 !important;
            color: #FAFAFA !important;
            border: 1px solid #333333 !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #9B6BFF !important;
            box-shadow: 0 0 0 2px rgba(155, 107, 255, 0.2) !important;
        }
        
        /* Select Box */
        .stSelectbox > div > div {
            background-color: #262730 !important;
            color: #FAFAFA !important;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #1A1D23 !important;
        }
        
        /* Metrics */
        [data-testid="metric-container"] {
            background-color: #262730 !important;
            border: 1px solid #333333 !important;
            padding: 1rem !important;
            border-radius: 8px !important;
        }
        
        [data-testid="metric-container"] label {
            color: #B0B5BD !important;
        }
        
        [data-testid="metric-container"] [data-testid="stMetricValue"] {
            color: #FAFAFA !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #262730 !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #B0B5BD !important;
            background-color: transparent !important;
        }
        
        .stTabs [aria-selected="true"] {
            color: #9B6BFF !important;
            border-bottom: 2px solid #9B6BFF !important;
        }
        
        /* Data Frame / Tables */
        .stDataFrame {
            background-color: #262730 !important;
        }
        
        .stTable {
            background-color: #262730 !important;
        }
        
        /* Code Blocks */
        .stCodeBlock {
            background-color: #262730 !important;
        }
        
        code {
            background-color: #2E3138 !important;
            color: #9B6BFF !important;
            padding: 2px 4px !important;
            border-radius: 3px !important;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px !important;
            height: 8px !important;
        }
        
        ::-webkit-scrollbar-track {
            background: #1A1D23 !important;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #9B6BFF !important;
            border-radius: 4px !important;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #B589FF !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def create_header():
    """יצירת כותרת הדף - ללא קו תחתון"""

    st.markdown(
        """
    <h1 style='text-align: center; color: #FAFAFA; margin-bottom: 30px;'>
        Bid Optimizer - Bulk File
    </h1>
    """,
        unsafe_allow_html=True,
    )
