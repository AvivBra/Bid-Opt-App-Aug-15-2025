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

    # DEBUG MODE
    print(f"🔍 DEBUG [upload_tab.py] render() function started")
    # DEBUG MODE

    # Initialize session state
    SessionManager.initialize()

    # DEBUG MODE
    print(f"🔍 DEBUG [upload_tab.py] SessionManager initialized")
    # DEBUG MODE

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
            # DEBUG MODE
            print(
                f"🔍 DEBUG [upload_tab.py] Template file detected: {template_file.name}"
            )
            print(
                f"🔍 DEBUG [upload_tab.py] Template file size: {template_file.size} bytes"
            )
            print(
                f"🔍 DEBUG [upload_tab.py] Saving template to session state with key: {SessionKeys.TEMPLATE_FILE}"
            )
            # DEBUG MODE

            st.session_state[SessionKeys.TEMPLATE_FILE] = template_file
            messages.show_success(SUCCESS_MESSAGES["TEMPLATE_UPLOADED"])

            # DEBUG MODE
            print(
                f"🔍 DEBUG [upload_tab.py] Template saved to session. Value is None: {st.session_state.get(SessionKeys.TEMPLATE_FILE) is None}"
            )
            # DEBUG MODE

        layout.add_vertical_space(1)

        # Bulk file upload
        bulk_file = widgets.file_uploader(
            label=BULK_UPLOAD_LABEL,
            key="bulk_upload",
            help_text=f"Upload your Amazon Ads Bulk file (max {MAX_FILE_SIZE_MB}MB)",
        )

        if bulk_file:
            # DEBUG MODE
            print(f"🔍 DEBUG [upload_tab.py] Bulk file detected: {bulk_file.name}")
            print(f"🔍 DEBUG [upload_tab.py] Bulk file size: {bulk_file.size} bytes")
            print(
                f"🔍 DEBUG [upload_tab.py] Saving bulk to session state with key: {SessionKeys.BULK_FILE}"
            )
            # DEBUG MODE

            st.session_state[SessionKeys.BULK_FILE] = bulk_file
            messages.show_success(SUCCESS_MESSAGES["BULK_UPLOADED"])

            # DEBUG MODE
            print(
                f"🔍 DEBUG [upload_tab.py] Bulk saved to session. Value is None: {st.session_state.get(SessionKeys.BULK_FILE) is None}"
            )
            # DEBUG MODE

    # Right column - Optimization selection
    with col2:
        st.subheader("Optimization Selection")

        # Optimization checkboxes
        selected_optimizations = widgets.optimization_selector()

        # DEBUG MODE
        print(
            f"🔍 DEBUG [upload_tab.py] Selected optimizations: {selected_optimizations}"
        )
        print(
            f"🔍 DEBUG [upload_tab.py] Saving optimizations to session with key: {SessionKeys.SELECTED_OPTIMIZATIONS}"
        )
        # DEBUG MODE

        st.session_state[SessionKeys.SELECTED_OPTIMIZATIONS] = selected_optimizations

        layout.add_vertical_space(2)

        # Validation status
        st.subheader("Validation Status")

        # Check if all requirements are met
        has_template = st.session_state.get(SessionKeys.TEMPLATE_FILE) is not None
        has_bulk = st.session_state.get(SessionKeys.BULK_FILE) is not None
        has_optimization = len(selected_optimizations) > 0

        # DEBUG MODE
        print(f"🔍 DEBUG [upload_tab.py] Validation check:")
        print(f"🔍 DEBUG [upload_tab.py]   - has_template: {has_template}")
        print(f"🔍 DEBUG [upload_tab.py]   - has_bulk: {has_bulk}")
        print(f"🔍 DEBUG [upload_tab.py]   - has_optimization: {has_optimization}")
        # DEBUG MODE

        # Show status messages
        if not has_template:
            messages.show_info("Upload Template file to continue")
        elif not has_bulk:
            messages.show_info("Upload Bulk file to continue")
        elif not has_optimization:
            messages.show_info("Select at least one optimization type")
        else:
            # DEBUG MODE
            print(
                f"🔍 DEBUG [upload_tab.py] All requirements met! Setting current step to 2"
            )
            # DEBUG MODE

            messages.show_success(SUCCESS_MESSAGES["FILES_VALIDATED"])
            st.session_state[SessionKeys.CURRENT_STEP] = 2

            # DEBUG MODE
            print(
                f"🔍 DEBUG [upload_tab.py] Current step in session: {st.session_state.get(SessionKeys.CURRENT_STEP)}"
            )
            print(
                f"🔍 DEBUG [upload_tab.py] Can proceed to step 2: {SessionManager.can_proceed_to_step(2)}"
            )
            print(f"🔍 DEBUG [upload_tab.py] Session state keys present:")
            print(
                f"🔍 DEBUG [upload_tab.py]   - {SessionKeys.TEMPLATE_FILE}: {SessionKeys.TEMPLATE_FILE in st.session_state}"
            )
            print(
                f"🔍 DEBUG [upload_tab.py]   - {SessionKeys.BULK_FILE}: {SessionKeys.BULK_FILE in st.session_state}"
            )
            print(
                f"🔍 DEBUG [upload_tab.py]   - {SessionKeys.SELECTED_OPTIMIZATIONS}: {SessionKeys.SELECTED_OPTIMIZATIONS in st.session_state}"
            )
            # DEBUG MODE

    # DEBUG MODE
    print(f"🔍 DEBUG [upload_tab.py] render() function completed")
    print(f"🔍 DEBUG [upload_tab.py] ========================================")
    # DEBUG MODE

    # Debug info (only in mockup)
    layout.add_vertical_space(2)
    with st.expander("Debug Info (Mockup Only)", expanded=False):
        st.write("Session State Keys:")
        st.write(
            f"TEMPLATE_FILE in session: {SessionKeys.TEMPLATE_FILE in st.session_state}"
        )
        st.write(f"BULK_FILE in session: {SessionKeys.BULK_FILE in st.session_state}")
        st.write(
            f"SELECTED_OPTIMIZATIONS in session: {SessionKeys.SELECTED_OPTIMIZATIONS in st.session_state}"
        )
        st.write("")
        st.write("Values:")
        st.write(
            f"Template: {st.session_state.get(SessionKeys.TEMPLATE_FILE) is not None}"
        )
        st.write(f"Bulk: {st.session_state.get(SessionKeys.BULK_FILE) is not None}")
        st.write(
            f"Optimizations: {st.session_state.get(SessionKeys.SELECTED_OPTIMIZATIONS)}"
        )
        st.write(f"Current Step: {st.session_state.get(SessionKeys.CURRENT_STEP)}")
        st.write("")
        st.write("Can Proceed to Step 2:", SessionManager.can_proceed_to_step(2))
        st.write("Can Proceed to Step 3:", SessionManager.can_proceed_to_step(3))
