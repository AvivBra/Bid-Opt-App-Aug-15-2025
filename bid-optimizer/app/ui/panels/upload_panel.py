import streamlit as st
import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ui.components.file_uploader import render_file_uploaders
from ui.components.checklist import render_optimization_checklist
from data.template_generator import TemplateGenerator


def render_upload_panel():
    """Render the upload panel"""

    st.markdown(
        """
    <div class='section-container'>
        <h2 class='section-header'>Upload Files</h2>
    """,
        unsafe_allow_html=True,
    )

    # Download template button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Generate template file
        generator = TemplateGenerator()
        template_file = generator.create_empty_template()

        # Direct download button
        st.download_button(
            label="Download Template",
            data=template_file,
            file_name="template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_template_btn",
            use_container_width=True,
            help="Download an empty template with required columns",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # File upload areas
    render_file_uploaders()

    st.markdown("<br>", unsafe_allow_html=True)

    # Optimization checklist
    st.markdown("### Select Optimizations")
    render_optimization_checklist()

    # Close div
    st.markdown("</div>", unsafe_allow_html=True)

    # Display file status
    display_file_status()


def display_file_status():
    """Display status of uploaded files"""

    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.get("template_file"):
            file = st.session_state.template_file
            size_kb = len(file.getvalue()) / 1024
            st.success(f"Template: {file.name} ({size_kb:.1f} KB)")
        else:
            st.info("Template: Not uploaded")

    with col2:
        if st.session_state.get("bulk_file"):
            file = st.session_state.bulk_file
            size_mb = len(file.getvalue()) / (1024 * 1024)
            st.success(f"Bulk: {file.name} ({size_mb:.1f} MB)")
        else:
            st.info("Bulk: Not uploaded")
