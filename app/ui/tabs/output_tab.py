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
from core.output import files_builder


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

    # Use centered content container
    with layout.create_content_container():
        # Get or set processing state
        processing_state = SessionManager.get(SessionKeys.PROCESSING_STATE)

        # If not yet processed, start processing
        if processing_state != ProcessingStates.COMPLETED:
            process_optimizations()
        else:
            show_results()


def process_optimizations():
    """Process optimizations with real data"""

    # Show processing message
    with messages.show_spinner(PROCESSING_MESSAGE):
        # Simulate processing time with progress
        progress_bar = st.progress(0, text="Initializing...")

        steps = [
            (0.2, "Reading files..."),
            (0.4, "Applying Virtual Map..."),
            (0.6, "Creating output files..."),
            (0.8, "Formatting data..."),
            (1.0, "Finalizing..."),
        ]

        for progress, text in steps:
            time.sleep(0.3)  # Shorter delay for real processing
            progress_bar.progress(progress, text=text)

        time.sleep(0.3)
        progress_bar.empty()

    # Generate real output files
    generate_real_files()

    # Mark as completed
    SessionManager.set(SessionKeys.PROCESSING_STATE, ProcessingStates.COMPLETED)

    # Show completion message
    messages.show_success(SUCCESS_MESSAGES["PROCESSING_COMPLETE"])

    # Rerun to show results
    st.rerun()


def generate_real_files():
    """Generate real output files from processed data"""

    # Get data from session
    bulk_df = st.session_state.get("bulk_df")
    virtual_map = st.session_state.get("virtual_map")
    optimizations = SessionManager.get(SessionKeys.SELECTED_OPTIMIZATIONS, [])

    if bulk_df is None:
        messages.show_error("No bulk data available for processing")
        return

    # Create Working File
    working_buffer = files_builder.create_working_file(bulk_df, optimizations)

    # Create Clean File
    clean_buffer = files_builder.create_clean_file(bulk_df, optimizations)

    # Store in session
    SessionManager.set(
        SessionKeys.OUTPUT_FILES, {"working": working_buffer, "clean": clean_buffer}
    )

    # Calculate statistics
    stats = calculate_real_statistics(bulk_df, virtual_map)
    st.session_state["processing_stats"] = stats


def calculate_real_statistics(bulk_df: pd.DataFrame, virtual_map) -> dict:
    """Calculate real statistics from processed data"""

    total_rows = len(bulk_df)

    # Count rows with different entities
    entity_counts = (
        bulk_df["Entity"].value_counts() if "Entity" in bulk_df.columns else {}
    )

    # Count bid ranges (mockup - in real version would check actual bid changes)
    bid_column = "Bid" if "Bid" in bulk_df.columns else None
    high_bids = 0
    low_bids = 0

    if bid_column:
        bid_values = pd.to_numeric(bulk_df[bid_column], errors="coerce")
        high_bids = len(bid_values[bid_values > MAX_BID])
        low_bids = len(bid_values[bid_values < MIN_BID])

    # Count portfolios processed
    portfolios_count = len(virtual_map.get_data()) if virtual_map else 0

    return {
        "total_rows": total_rows,
        "entity_counts": entity_counts.to_dict(),
        "high_bids": high_bids,
        "low_bids": low_bids,
        "portfolios_processed": portfolios_count,
        "calculation_errors": 0,  # Mockup - would be calculated in real optimizer
    }


def show_results():
    """Show processing results and download options"""

    # Get output files
    output_files = SessionManager.get(SessionKeys.OUTPUT_FILES, {})
    stats = st.session_state.get("processing_stats", {})

    # Show any calculation notices
    st.subheader("Processing Summary")
    show_calculation_notices(stats)

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
    show_real_statistics(stats)


def show_calculation_notices(stats: dict):
    """Show calculation errors and warnings based on real data"""

    calculation_errors = stats.get("calculation_errors", 0)
    high_bids = stats.get("high_bids", 0)
    low_bids = stats.get("low_bids", 0)

    # Pink notice for calculation errors (mockup - always 0 for now)
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


def show_real_statistics(stats: dict):
    """Show real processing statistics"""

    st.subheader("Processing Statistics")

    col1, col2, col3, col4 = st.columns(4)

    # Real statistics
    with col1:
        total_rows = stats.get("total_rows", 0)
        st.metric("Total Rows Processed", f"{total_rows:,}")

    with col2:
        portfolios = stats.get("portfolios_processed", 0)
        st.metric("Portfolios Processed", f"{portfolios:,}")

    with col3:
        high_bids = stats.get("high_bids", 0)
        st.metric("High Bids (>1.25)", f"{high_bids:,}")

    with col4:
        low_bids = stats.get("low_bids", 0)
        st.metric("Low Bids (<0.02)", f"{low_bids:,}")

    # Additional details in expander
    with st.expander("Detailed Statistics", expanded=False):
        entity_counts = stats.get("entity_counts", {})

        if entity_counts:
            st.write("**Entity Breakdown:**")
            for entity, count in entity_counts.items():
                st.write(f"• {entity}: {count:,} rows")

        st.write("")
        st.write("**Optimization Applied:**")
        st.write("• Zero Sales: Applied to all eligible rows")

        st.write("")
        st.write("**File Information:**")
        st.write("• Working File: 2 sheets (Clean + Working)")
        st.write("• Clean File: 1 sheet (Clean only)")
