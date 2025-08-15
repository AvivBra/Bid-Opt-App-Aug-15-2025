import streamlit as st
import sys
import os

# Add app directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from ui.layout import apply_custom_css, create_header
from ui.panels.upload_panel import render_upload_panel
from ui.panels.validate_panel import render_validation_panel


def render_page():
    """Main page renderer"""
    # Initialize session state
    initialize_session_state()

    # Apply styling
    apply_custom_css()

    # Header
    create_header()

    # Upload panel
    render_upload_panel()

    # Validation panel - ACTUAL PANEL, NOT PLACEHOLDER
    render_validation_panel()

    # Output panel - still placeholder for now
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


def initialize_session_state():
    """Initialize session state variables"""
    if "current_state" not in st.session_state:
        st.session_state.current_state = "upload"
    if "template_file" not in st.session_state:
        st.session_state.template_file = None
    if "bulk_file" not in st.session_state:
        st.session_state.bulk_file = None
    if "selected_optimizations" not in st.session_state:
        st.session_state.selected_optimizations = ["Zero Sales"]
    if "validation_state" not in st.session_state:
        st.session_state.validation_state = "pending"
