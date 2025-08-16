# LOCKED - Phase A4 Complete
import streamlit as st
from datetime import datetime
from io import BytesIO
import pandas as pd


def generate_filename(file_type: str) -> str:
    """
    Generate filename with current date and time

    Args:
        file_type: 'Working' or 'Clean'

    Returns:
        Formatted filename string
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M")
    return f"Auto Optimized Bulk | {file_type} | {date_str} | {time_str}.xlsx"


def create_mock_excel_file(file_type: str) -> BytesIO:
    """
    Create a mock Excel file for download

    Args:
        file_type: 'Working' or 'Clean'

    Returns:
        BytesIO object containing Excel file
    """
    # Create mock data
    mock_data = pd.DataFrame(
        {
            "Product": ["ASIN123", "ASIN456", "ASIN789"],
            "Entity": ["Keyword", "Product Targeting", "Keyword"],
            "Operation": ["Update", "Update", "Update"],
            "Campaign ID": ["1234567890", "1234567890", "1234567890"],
            "Ad Group ID": ["9876543210", "9876543210", "9876543210"],
            "Bid": [0.02, 0.02, 0.02],  # Updated bids
            "Sales": [0, 0, 0],
            "Impressions": [1500, 3000, 2000],
            # Add more columns as needed for demo
        }
    )

    # Create BytesIO object
    output = BytesIO()

    # Write to Excel with appropriate sheets
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        if file_type == "Working":
            # Working file has 2 sheets per optimization
            mock_data.to_excel(writer, sheet_name="Clean Zero Sales", index=False)
            mock_data.to_excel(writer, sheet_name="Working Zero Sales", index=False)
        else:
            # Clean file has 1 sheet per optimization
            mock_data.to_excel(writer, sheet_name="Clean Zero Sales", index=False)

    output.seek(0)
    return output


def render_download_buttons():
    """Render download buttons for Working and Clean files"""

    col1, col2 = st.columns(2)

    with col1:
        render_working_download()

    with col2:
        render_clean_download()


def render_working_download():
    """Render Working File download button"""

    # Check if we have real files in session state
    if st.session_state.get("output_files", {}).get("working"):
        # Use real file from session state
        file_data = st.session_state.output_files["working"]
        filename = st.session_state.output_files.get(
            "working_filename", generate_filename("Working")
        )

        # Get file size
        if isinstance(file_data, bytes):
            file_size = len(file_data) / 1024  # KB
        else:
            file_size = len(file_data.getvalue()) / 1024  # KB
    else:
        # Fallback to mock file
        filename = generate_filename("Working")
        file_data = create_mock_excel_file("Working")
        file_size = len(file_data.getvalue()) / 1024  # KB

    # Display file info
    st.markdown(f"**Working File**")
    st.markdown(
        f"<small>Size: {file_size:.1f} KB | 2 sheets</small>", unsafe_allow_html=True
    )

    # Download button
    st.download_button(
        label="Download Working File",
        data=file_data,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_working_file",
        use_container_width=True,
        type="primary",
    )


def render_clean_download():
    """Render Clean File download button"""

    # Check if we have real files in session state
    if st.session_state.get("output_files", {}).get("clean"):
        # Use real file from session state
        file_data = st.session_state.output_files["clean"]
        filename = st.session_state.output_files.get(
            "clean_filename", generate_filename("Clean")
        )

        # Get file size
        if isinstance(file_data, bytes):
            file_size = len(file_data) / 1024  # KB
        else:
            file_size = len(file_data.getvalue()) / 1024  # KB
    else:
        # Fallback to mock file
        filename = generate_filename("Clean")
        file_data = create_mock_excel_file("Clean")
        file_size = len(file_data.getvalue()) / 1024  # KB

    # Display file info
    st.markdown(f"**Clean File**")
    st.markdown(
        f"<small>Size: {file_size:.1f} KB | 1 sheet</small>", unsafe_allow_html=True
    )

    # Download button
    st.download_button(
        label="Download Clean File",
        data=file_data,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_clean_file",
        use_container_width=True,
        type="primary",
    )


def render_reset_button():
    """Render reset button"""

    if st.button(
        "Reset",
        key="reset_output_btn",
        use_container_width=True,
        help="Clear all data and start over",
    ):
        # Clear session state
        for key in list(st.session_state.keys()):
            if key not in ["current_state"]:
                del st.session_state[key]
        st.session_state.current_state = "upload"
        st.rerun()
