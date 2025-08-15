import streamlit as st


def render_file_uploaders():
    """Render file upload areas"""

    col1, col2 = st.columns(2)

    with col1:
        render_template_uploader()

    with col2:
        render_bulk_uploader()


def render_template_uploader():
    """Template file upload area"""

    st.markdown("**Template File**")
    st.markdown(
        "<small>Portfolio Name | Base Bid | Target CPA</small>", unsafe_allow_html=True
    )

    template_file = st.file_uploader(
        "Upload Template",
        type=["xlsx", "csv"],
        key="template_uploader",
        label_visibility="collapsed",
        help="Upload your template file with portfolio base bids",
    )

    if template_file:
        # Check file size
        if len(template_file.getvalue()) > 40 * 1024 * 1024:
            st.error("File exceeds 40MB limit")
            st.session_state.template_file = None
        else:
            st.session_state.template_file = template_file


def render_bulk_uploader():
    """Bulk file upload area"""

    st.markdown("**Bulk File**")
    st.markdown(
        "<small>Must contain 'Sponsored Products Campaigns' sheet</small>",
        unsafe_allow_html=True,
    )

    bulk_file = st.file_uploader(
        "Upload Bulk",
        type=["xlsx", "csv"],
        key="bulk_uploader",
        label_visibility="collapsed",
        help="Upload your Amazon Bulk file",
    )

    if bulk_file:
        # Check file size
        if len(bulk_file.getvalue()) > 40 * 1024 * 1024:
            st.error("File exceeds 40MB limit")
            st.session_state.bulk_file = None
        else:
            st.session_state.bulk_file = bulk_file
