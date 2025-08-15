import streamlit as st
from ui.layout import apply_custom_css, create_header
from ui.panels.upload_panel import render_upload_panel


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

    # Temporary placeholders for other panels
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
