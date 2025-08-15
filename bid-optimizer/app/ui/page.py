import streamlit as st
from ui.layout import apply_custom_css, create_header, create_sections


def render_page():
    """רינדור העמוד הראשי"""
    # החלת עיצוב
    apply_custom_css()

    # כותרת
    create_header()

    # יצירת 3 הסקציות
    create_sections()


def initialize_session_state():
    """אתחול משתני סשן בסיסיים"""
    if "current_state" not in st.session_state:
        st.session_state.current_state = "upload"
    if "template_file" not in st.session_state:
        st.session_state.template_file = None
    if "bulk_file" not in st.session_state:
        st.session_state.bulk_file = None
