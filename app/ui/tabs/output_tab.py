"""
Output tab UI implementation - No emojis or icons
"""

import streamlit as st
import pandas as pd
import time
from io import BytesIO
from app.ui import widgets, messages, layout
from app.state.session import SessionManager
from config.ui_text import *
from config.settings import SessionKeys, ProcessingStates
from config.constants import MIN_BID, MAX_BID


def render():
    """Render the output tab"""

    # Check if user can access this tab
    if not SessionManager.can_proceed_to_step(3):
        messages.show_error(
            "Please complete Step 2 (Validate) before proceeding to output"
        )
        return

    # Tab header
    st.header(OUTPUT_HEADER)

    # Get or set processing state
    processing_state = SessionManager.get(SessionKeys.PROCESSING_STATE)

    # If not yet processed, start processing
    if processing_state != ProcessingStates.COMPLETED:
        process_optimizations()
    else:
        show_results()


def process_optimizations():
    """Simulate processing optimizations"""

    # Show processing message
    with messages.show_spinner(PROCESSING_MESSAGE):
        # Simulate processing time
        progress_bar = st.progress(0, text="Initializing...")

        steps = [
            (0.2, "Reading files..."),
            (0.4, "Cleaning data..."),
            (0.6, "Applying optimizations..."),
            (0.8, "Generating output files..."),
            (1.0, "Finalizing..."),
        ]

        for progress, text in steps:
            time.sleep(0.5)  # Simulate work
            progress_bar.progress(progress, text=text)

        time.sleep(0.5)
        progress_bar.empty()

    # Mark as completed
    SessionManager.set(SessionKeys.PROCESSING_STATE, ProcessingStates.COMPLETED)

    # Generate mock output files
    generate_mock_files()

    # Show completion message
    messages.show_success(SUCCESS_MESSAGES["PROCESSING_COMPLETE"])

    # Rerun to show results
    st.rerun()


def generate_mock_files():
    """Generate mock output files"""

    # Create mock data
    mock_data = pd.DataFrame(
        {
            "Campaign": ["Campaign 1", "Campaign 2", "Campaign 3"],
            "Ad Group": ["Ad Group A", "Ad Group B", "Ad Group C"],
            "Keyword": ["keyword1", "keyword2", "keyword3"],
            "Bid": [0.50, 0.75, 1.00],
            "Status": ["Active", "Active", "Active"],
        }
    )

    # Create Working File
    working_buffer = BytesIO()
    with pd.ExcelWriter(working_buffer, engine="openpyxl") as writer:
        mock_data.to_excel(writer, index=False, sheet_name="Clean Zero Sales")
        mock_data.to_excel(writer, index=False, sheet_name="Working Zero Sales")
    working_buffer.seek(0)

    # Create Clean File
    clean_buffer = BytesIO()
    with pd.ExcelWriter(clean_buffer, engine="openpyxl") as writer:
        mock_data.to_excel(writer, index=False, sheet_name="Clean Zero Sales")
    clean_buffer.seek(0)

    # Store in session
    SessionManager.set(
        SessionKeys.OUTPUT_FILES, {"working": working_buffer, "clean": clean_buffer}
    )


def show_results():
    """Show processing results and download options"""

    # Get output files
    output_files = SessionManager.get(SessionKeys.OUTPUT_FILES, {})

    # Show any calculation notices (mockup)
    st.subheader("Processing Summary")

    # Mock calculation errors
    show_calculation_notices()

    layout.add_vertical_space(1)
    layout.show_divider()

    # Download section
    st.subheader("Download Output Files")

    col1, col2, col3 = st.columns(3)

    with col1:
        if "working" in output_files:
            widgets.download_button(
                label=DOWNLOAD_WORKING_FILE,
                data=output_files["working"],
                filename=widgets.generate_filename("Working File"),
                key="download_working",
            )

    with col2:
        if "clean" in output_files:
            widgets.download_button(
                label=DOWNLOAD_CLEAN_FILE,
                data=output_files["clean"],
                filename=widgets.generate_filename("Clean File"),
                key="download_clean",
            )

    with col3:
        if widgets.action_button(
            NEW_PROCESSING_BUTTON, key="new_processing", button_type="secondary"
        ):
            # Reset everything
            SessionManager.reset_for_new_processing()

    layout.add_vertical_space(2)

    # Statistics section
    show_statistics()


def show_calculation_notices():
    """Show calculation errors and warnings (mockup)"""

    # Mock data for demonstration
    calculation_errors = 7
    high_bids = 3
    low_bids = 2

    # Pink notice for calculation errors
    if calculation_errors > 0:
        message = WARNING_MESSAGES["CALCULATION_ERRORS"].format(
            count=calculation_errors, optimization_type="Zero Sales"
        )
        messages.show_pink_notice(message)

    # Info about out-of-range bids
    if high_bids > 0 or low_bids > 0:
        message = WARNING_MESSAGES["BIDS_OUT_OF_RANGE"].format(
            high_count=high_bids, max_bid=MAX_BID, low_count=low_bids, min_bid=MIN_BID
        )
        messages.show_info(message)


def show_statistics():
    """Show processing statistics"""

    st.subheader("Processing Statistics")

    col1, col2, col3, col4 = st.columns(4)

    # Mock statistics
    with col1:
        st.metric("Total Rows Processed", "1,234")

    with col2:
        st.metric("Optimizations Applied", "856")

    with col3:
        st.metric("Average Bid Change", "+15%")

    with col4:
        st.metric("Processing Time", "2.3s")

    # Additional details in expander
    with st.expander("Detailed Statistics", expanded=False):
        st.write("**Optimization Breakdown:**")
        st.write("• Zero Sales: 856 rows modified")
        st.write("• Skipped rows: 378 (invalid data)")
        st.write("")
        st.write("**Bid Distribution:**")
        st.write(f"• Below {MIN_BID}: 2 rows")
        st.write(f"• Within range: 1,229 rows")
        st.write(f"• Above {MAX_BID}: 3 rows")
        st.write("")
        st.write("**File Information:**")
        st.write("• Working File: 2 sheets")
        st.write("• Clean File: 1 sheet")
        st.write("• Total file size: ~245 KB")
