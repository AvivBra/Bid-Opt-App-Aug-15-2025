import streamlit as st


def apply_custom_css():
    """החלת סגנון CSS מותאם אישית"""
    st.markdown(
        """
    <style>
    /* רקע לבן */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* כפתורים אדומים */
    .stButton > button {
        background-color: #FF0000;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border-radius: 4px;
    }
    
    .stButton > button:hover {
        background-color: #CC0000;
    }
    
    /* כותרות סקציות */
    .section-header {
        border-bottom: 2px solid #FF0000;
        padding-bottom: 10px;
        margin-bottom: 20px;
        color: #000000;
    }
    
    /* מרווחים בין סקציות */
    .section-container {
        margin-bottom: 40px;
        padding: 20px;
        background-color: #FAFAFA;
        border-radius: 8px;
        border: 1px solid #EEEEEE;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def create_header():
    """יצירת כותרת הדף"""
    st.markdown(
        """
    <h1 style='text-align: center; color: #000000; margin-bottom: 10px;'>
        Bid Optimizer - Bulk File
    </h1>
    <hr style='border: 1px solid #FF0000; margin-bottom: 30px;'>
    """,
        unsafe_allow_html=True,
    )


def create_sections():
    """יצירת 3 הסקציות הריקות"""

    # Upload Section
    st.markdown(
        """
    <div class='section-container'>
        <h2 class='section-header'>Upload Files</h2>
        <p style='color: #666666; text-align: center; padding: 40px 0;'>
            Upload section - Coming soon
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Validation Section
    st.markdown(
        """
    <div class='section-container'>
        <h2 class='section-header'>Validation Results</h2>
        <p style='color: #666666; text-align: center; padding: 40px 0;'>
            Validation section - Coming soon
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Output Section
    st.markdown(
        """
    <div class='section-container'>
        <h2 class='section-header'>Output Files</h2>
        <p style='color: #666666; text-align: center; padding: 40px 0;'>
            Output section - Coming soon
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
