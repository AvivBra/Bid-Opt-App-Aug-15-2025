"""
Upload tab UI implementation - No emojis or icons
"""

import streamlit as st
from app.ui import widgets, messages, layout
from app.state.session import SessionManager
from config.ui_text import *
from config.constants import MAX_FILE_SIZE_MB
from config.settings import SessionKeys


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
            SessionManager.set(SessionKeys.TEMPLATE_FILE, template_file)
            # Mock validation - in real app this would validate the file
            messages.show_success(SUCCESS_MESSAGES["TEMPLATE_UPLOADED"])

        layout.add_vertical_space(1)

        # Bulk file upload
        bulk_file = widgets.file_uploader(
            label=BULK_UPLOAD_LABEL,
            key="bulk_upload",
            help_text=f"Upload your Amazon Ads Bulk file (max {MAX_FILE_SIZE_MB}MB)",
        )

        if bulk_file:
            SessionManager.set(SessionKeys.BULK_FILE, bulk_file)
            # Mock validation - in real app this would validate the file
            messages.show_success(SUCCESS_MESSAGES["BULK_UPLOADED"])

    # Right column - Optimization selection
    with col2:
        st.subheader("Optimization Selection")

        # Optimization checkboxes
        selected_optimizations = widgets.optimization_selector()
        SessionManager.set(SessionKeys.SELECTED_OPTIMIZATIONS, selected_optimizations)

        layout.add_vertical_space(2)

        # Validation status
        st.subheader("Validation Status")

        # Check if all requirements are met
        has_template = SessionManager.get(SessionKeys.TEMPLATE_FILE) is not None
        has_bulk = SessionManager.get(SessionKeys.BULK_FILE) is not None
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

            # Update session state
            SessionManager.set(SessionKeys.CURRENT_STEP, 2)

            # Show continue instruction
            messages.show_info(
                "All requirements met! Switch to the 'Validate' tab to continue."
            )

    # File status summary at bottom - wrapped in content container
    layout.add_vertical_space(2)
    layout.show_divider()

    # Use content container to match the upper section layout
    with layout.create_content_container():
        st.subheader("Upload Summary")

        # Use the same column layout with gap for the bottom section
        bottom_col1, _, bottom_col2 = st.columns([1, 0.2, 1])  # Added gap column

        with bottom_col1:
            if template_file:
                st.info("**Template:** Uploaded")
            else:
                st.info("**Template:** Not uploaded")

        with bottom_col2:
            if bulk_file:
                st.info("**Bulk File:** Uploaded")
            else:
                st.info("**Bulk File:** Not uploaded")

        # Debug info (only in mockup)
        layout.add_vertical_space(1)
        with st.expander("Debug Info (Mockup Only)", expanded=False):
            st.write("Session State:")
            st.write(
                {
                    "Has Template": has_template,
                    "Has Bulk": has_bulk,
                    "Selected Optimizations": selected_optimizations,
                    "Can Proceed": SessionManager.can_proceed_to_step(2),
                }
            )
