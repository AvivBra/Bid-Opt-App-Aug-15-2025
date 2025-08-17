import streamlit as st


def apply_custom_css():
    """החלת סגנון CSS מותאם אישית - תומך בשני מצבים"""

    # בדוק אם המשתמש רוצה דארק מוד (שמור בsession state)
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True  # ברירת מחדל: דארק מוד

    # הסתרת Toolbar בשני המצבים
    st.markdown(
        """
        <style>
        /* הסתרת הToolbar של Streamlit */
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
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.dark_mode:
        # Dark Mode CSS
        st.markdown(
            """
        <style>
        /* Dark Mode Styles */
        .stApp {
            background-color: #0E1117 !important;
        }
        
        /* כפתורים סגולים/ויולט */
        .stButton > button {
            background-color: #9B6BFF !important;
            color: white !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            font-weight: bold !important;
            border-radius: 4px !important;
        }
        
        .stButton > button:hover {
            background-color: #B589FF !important;
        }
        
        /* כותרות סקציות */
        .section-header {
            border-bottom: 2px solid #9B6BFF !important;
            padding-bottom: 10px !important;
            margin-bottom: 20px !important;
            color: #FAFAFA !important;
            text-align: center !important;
            font-size: 24px !important;
            font-weight: bold !important;
        }
        
        /* פאנלים */
        .section-container {
            margin-bottom: 40px !important;
            padding: 20px !important;
            background-color: #262730 !important;
            border-radius: 8px !important;
            border: 1px solid #333333 !important;
        }
        
        /* Checkbox styling - ויולט */
        .stCheckbox > label > div:first-child {
            border-color: #9B6BFF !important;
        }
        
        input[type="checkbox"]:checked {
            background-color: #9B6BFF !important;
        }
        
        [data-testid="stCheckbox"] > label > div[data-testid="stMarkdownContainer"] {
            color: #FAFAFA !important;
        }
        
        /* Info/Alert boxes - אפור יותר בהיר */
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
        
        /* File uploader - אפור כהה */
        .stFileUploader > div > div {
            background-color: #1A1D23 !important;
            border: 2px dashed #3A3D45 !important;
            color: #FAFAFA !important;
        }
        
        .stFileUploader > div > div:hover {
            background-color: #202329 !important;
            border-color: #9B6BFF !important;
        }
        
        /* Browse files button inside uploader */
        .stFileUploader button {
            background-color: #3A3D45 !important;
            color: #FAFAFA !important;
        }
        
        .stFileUploader button:hover {
            background-color: #4A4D55 !important;
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
        
        /* Download button */
        .stDownloadButton > button {
            background-color: #00D26A !important;
            color: white !important;
        }
        
        .stDownloadButton > button:hover {
            background-color: #00E574 !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
    else:
        # Light Mode CSS (המקורי)
        st.markdown(
            """
        <style>
        /* Light Mode Styles */
        .stApp {
            background-color: #FFFFFF !important;
        }
        
        /* כפתורים סגולים גם בלייט מוד */
        .stButton > button {
            background-color: #9B6BFF !important;
            color: white !important;
            border: none !important;
            padding: 0.5rem 1rem !important;
            font-weight: bold !important;
            border-radius: 4px !important;
        }
        
        .stButton > button:hover {
            background-color: #7E4FE3 !important;
        }
        
        /* כותרות סקציות */
        .section-header {
            border-bottom: 2px solid #9B6BFF !important;
            padding-bottom: 10px !important;
            margin-bottom: 20px !important;
            color: #000000 !important;
            text-align: center !important;
            font-size: 24px !important;
            font-weight: bold !important;
        }
        
        /* פאנלים */
        .section-container {
            margin-bottom: 40px !important;
            padding: 20px !important;
            background-color: #FAFAFA !important;
            border-radius: 8px !important;
            border: 1px solid #EEEEEE !important;
        }
        
        /* Download button ירוק */
        .stDownloadButton > button {
            background-color: #00A050 !important;
            color: white !important;
        }
        
        .stDownloadButton > button:hover {
            background-color: #008040 !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )


def create_header():
    """יצירת כותרת הדף עם כפתור מעבר בין מצבים"""

    # כפתור מעבר בין מצבים בפינה
    col1, col2, col3 = st.columns([8, 1, 1])

    with col3:
        # כפתור מעבר בין מצבים
        mode_label = "☀️" if st.session_state.get("dark_mode", True) else "🌙"
        if st.button(mode_label, key="mode_toggle", help="Toggle Dark/Light Mode"):
            st.session_state.dark_mode = not st.session_state.get("dark_mode", True)
            st.rerun()

    # צבע הכותרת לפי המצב
    text_color = "#FAFAFA" if st.session_state.get("dark_mode", True) else "#000000"
    border_color = "#9B6BFF"  # סגול בשני המצבים

    st.markdown(
        f"""
    <h1 style='text-align: center; color: {text_color}; margin-bottom: 10px;'>
        Bid Optimizer - Bulk File
    </h1>
    <hr style='border: 1px solid {border_color}; margin-bottom: 30px;'>
    """,
        unsafe_allow_html=True,
    )
