# LOCKED - Phase A4 Complete
import streamlit as st
import time
from ui.components.progress_bar import animate_progress
from ui.components.download_buttons import (
    render_download_buttons,
    render_reset_button,
    generate_filename,
)


def render_output_panel():
    """Render the output panel"""

    # Only show if we're in processing or complete state
    current_state = st.session_state.get("current_state", "upload")
    if current_state not in ["processing", "complete"]:
        return

    st.markdown(
        """
    <div class='section-container'>
        <h2 class='section-header'>Output Files</h2>
    """,
        unsafe_allow_html=True,
    )

    if current_state == "processing":
        render_processing_state()
    elif current_state == "complete":
        render_complete_state()

    # Close div
    st.markdown("</div>", unsafe_allow_html=True)


def render_processing_state():
    """Render processing state with progress bar"""

    # Show animated progress bar
    progress_placeholder = animate_progress(duration=3.0)

    # After animation, transition to complete state
    st.session_state.current_state = "complete"
    st.session_state.processing_stats = {
        "rows_processed": 1234,
        "rows_modified": 456,
        "calculation_errors": 7,
        "high_bids": 3,
        "low_bids": 2,
    }
    time.sleep(0.5)
    st.rerun()


def render_complete_state():
    """Render complete state with download buttons"""

    # Success message
    st.markdown(
        """
    <div style='background-color: #d4edda; border: 1px solid #c3e6cb; 
                border-radius: 4px; padding: 12px; margin-bottom: 16px;'>
        <div style='color: #155724; font-weight: bold;'>
            ✓ Processing complete
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Pink notice for calculation errors
    stats = st.session_state.get("processing_stats", {})
    if stats.get("calculation_errors", 0) > 0:
        render_pink_notice(stats["calculation_errors"])

    # Info about bid adjustments
    if stats.get("high_bids", 0) > 0 or stats.get("low_bids", 0) > 0:
        render_bid_info(stats.get("high_bids", 0), stats.get("low_bids", 0))

    # File generation info
    st.markdown("### Files generated:")

    # File details
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
        <div style='background-color: #f8f9fa; padding: 10px; border-radius: 4px;'>
            <strong>Working File:</strong><br>
            • 2.4 MB<br>
            • 2 sheets<br>
            • 1,234 rows
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div style='background-color: #f8f9fa; padding: 10px; border-radius: 4px;'>
            <strong>Clean File:</strong><br>
            • 1.8 MB<br>
            • 1 sheet<br>
            • 1,234 rows
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Download buttons
    render_download_buttons()

    st.markdown("<br>", unsafe_allow_html=True)

    # Reset button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        render_reset_button()

    # Processing statistics
    render_statistics()


def render_pink_notice(error_count: int):
    """Render pink notice box for calculation errors"""

    st.markdown(
        f"""
    <div style='background-color: #FFE4E1; border: 1px solid #FFB6C1;
                border-radius: 4px; padding: 16px; margin: 20px 0;'>
        <div style='color: #8B0000; font-weight: bold; font-size: 14px;'>
            Please note: {error_count} calculation errors in Zero Sales optimization
        </div>
        <div style='color: #8B0000; margin-top: 8px;'>
            These rows were skipped due to missing or invalid data.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_bid_info(high_bids: int, low_bids: int):
    """Render info about bid adjustments"""

    messages = []
    if high_bids > 0:
        messages.append(f"{high_bids} rows with bid >1.25")
    if low_bids > 0:
        messages.append(f"{low_bids} rows with bid <0.02")

    if messages:
        message_text = ", ".join(messages)
        st.markdown(
            f"""
        <div style='background-color: #d1ecf1; border: 1px solid #bee5eb;
                    border-radius: 4px; padding: 12px; margin-bottom: 16px;'>
            <div style='color: #0c5460; font-weight: bold;'>
                ℹ️ Bid adjustments: {message_text}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_statistics():
    """Render processing statistics"""

    stats = st.session_state.get("processing_stats", {})

    st.markdown("### Processing Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Rows Processed", stats.get("rows_processed", 1234))

    with col2:
        st.metric("Rows Modified", stats.get("rows_modified", 456))

    with col3:
        st.metric("Calculation Errors", stats.get("calculation_errors", 7))

    with col4:
        st.metric("Processing Time", "2.3 seconds")
