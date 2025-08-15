import streamlit as st


def render_download_template_button():
    """Download template button"""

    return st.button(
        "Download Template",
        key="download_template_btn",
        use_container_width=True,
        help="Download an empty template with required columns",
    )


def render_process_button():
    """Process files button"""

    # Check if button can be enabled
    can_process = (
        st.session_state.get("template_file")
        and st.session_state.get("bulk_file")
        and st.session_state.get("validation_result", {}).get("is_valid", False)
        and len(st.session_state.get("selected_optimizations", [])) > 0
    )

    return st.button(
        "Process Files",
        key="process_btn",
        disabled=not can_process,
        use_container_width=True,
        type="primary",
        help="Start processing with selected optimizations",
    )


def render_upload_new_template_button():
    """Upload new template button"""

    return st.button(
        "Upload New Template",
        key="upload_new_template_btn",
        use_container_width=True,
        type="primary",
        help="Upload a corrected template file",
    )


def render_reset_button():
    """Reset button"""

    if st.button(
        "Reset",
        key="reset_btn",
        use_container_width=True,
        help="Clear all data and start over",
    ):
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.current_state = "upload"
        st.rerun()


def render_download_working_button():
    """Download Working File button"""

    if st.session_state.get("output_files", {}).get("working"):
        working_file = st.session_state.output_files["working"]
        filename = st.session_state.output_files.get("working_filename", "working.xlsx")

        st.download_button(
            label="Download Working File",
            data=working_file,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_working",
            use_container_width=True,
        )


def render_download_clean_button():
    """Download Clean File button"""

    if st.session_state.get("output_files", {}).get("clean"):
        clean_file = st.session_state.output_files["clean"]
        filename = st.session_state.output_files.get("clean_filename", "clean.xlsx")

        st.download_button(
            label="Download Clean File",
            data=clean_file,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_clean",
            use_container_width=True,
        )
