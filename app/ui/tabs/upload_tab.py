"""
Upload tab UI implementation - No emojis or icons
"""

import streamlit as st
from app.ui import widgets, messages, layout
from app.state.session import SessionManager
from config.ui_text import *
from config.constants import MAX_FILE_SIZE_MB
from config.settings import SessionKeys
from core.io import readers


def render():
    """Render the upload tab"""

    # Initialize session state
    SessionManager.initialize()

    # Tab header
    st.header(UPLOAD_HEADER)

    # Create two columns with gap
    col1, col2 = layout.create_columns([1, 1], gap="medium")

    # Left column - Files
    with col1:
        st.subheader("Files")

        # Download template button
        template_data = widgets.create_empty_template()
        widgets.download_button(
            label=TEMPLATE_DOWNLOAD_BUTTON,
            data=template_data,
            filename="template.xlsx",
            key="download_template",
        )

        layout.add_vertical_space(1)

        # Template upload
        template_file = widgets.file_uploader(
            label=TEMPLATE_UPLOAD_LABEL,
            key="template_upload",
            help_text=f"Upload your completed template file (max {MAX_FILE_SIZE_MB}MB)",
        )

        if template_file:
            # Read and validate template file
            template_df = readers.read_template_file(template_file)

            if template_df is not None:
                st.session_state[SessionKeys.TEMPLATE_FILE] = template_file
                st.session_state["template_df"] = (
                    template_df  # Store DataFrame for processing
                )
                messages.show_success(SUCCESS_MESSAGES["TEMPLATE_UPLOADED"])
            else:
                # Error already shown by readers
                st.session_state[SessionKeys.TEMPLATE_FILE] = None
                st.session_state["template_df"] = None

        layout.add_vertical_space(1)

        # Bulk file upload
        bulk_file = widgets.file_uploader(
            label=BULK_UPLOAD_LABEL,
            key="bulk_upload",
            help_text=f"Upload your Amazon Ads Bulk file (max {MAX_FILE_SIZE_MB}MB)",
        )

        if bulk_file:
            # Read and validate bulk file
            bulk_df = readers.read_bulk_file(bulk_file)

            if bulk_df is not None:
                st.session_state[SessionKeys.BULK_FILE] = bulk_file
                st.session_state["bulk_df"] = bulk_df  # Store DataFrame for processing
                messages.show_success(SUCCESS_MESSAGES["BULK_UPLOADED"])
            else:
                # Error already shown by readers
                st.session_state[SessionKeys.BULK_FILE] = None
                st.session_state["bulk_df"] = None

    # Right column - Optimization selection
    with col2:
        st.subheader("Optimization Selection")

        # Optimization checkboxes
        selected_optimizations = widgets.optimization_selector()
        st.session_state[SessionKeys.SELECTED_OPTIMIZATIONS] = selected_optimizations

        layout.add_vertical_space(2)

        # Validation status
        st.subheader("Validation Status")

        # Check if all requirements are met
        has_template = st.session_state.get(SessionKeys.TEMPLATE_FILE) is not None
        has_bulk = st.session_state.get(SessionKeys.BULK_FILE) is not None
        has_optimization = len(selected_optimizations) > 0

        # Show status messages
        if not has_template:
            messages.show_info("Upload Template file to continue")
        elif not has_bulk:
            messages.show_info("Upload Bulk file to continue")
        elif not has_optimization:
            messages.show_info("Select at least one optimization type")
        else:
            messages.show_success(SUCCESS_MESSAGES["FILES_VALIDATED"])
            st.session_state[SessionKeys.CURRENT_STEP] = 2

            # Show instruction to proceed
            layout.add_vertical_space(2)
            st.info(
                "✅ All files validated! Click the **Validate** tab above to continue."
            )
