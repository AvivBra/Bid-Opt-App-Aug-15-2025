# LOCKED - Phase A4 Complete
import streamlit as st
import time


def render_progress_bar(progress: float = 0.0, text: str = "Processing..."):
    """
    Render a progress bar with text

    Args:
        progress: Progress value between 0.0 and 1.0
        text: Text to display above progress bar
    """
    progress_bar = st.progress(progress)
    st.markdown(
        f"<p style='text-align: center; color: #FAFAFA;'>{text}</p>",
        unsafe_allow_html=True,
    )
    return progress_bar


def animate_progress(duration: float = 3.0, steps: list = None):
    """
    Animate progress bar through processing steps

    Args:
        duration: Total animation duration in seconds
        steps: List of (progress, text) tuples
    """
    if steps is None:
        steps = [
            (0.1, "Initializing optimizations..."),
            (0.3, "Applying Zero Sales optimization..."),
            (0.5, "Processing data..."),
            (0.7, "Generating Working file..."),
            (0.9, "Generating Clean file..."),
            (1.0, "✓ Processing complete!"),
        ]

    progress_placeholder = st.empty()

    for progress, text in steps:
        with progress_placeholder.container():
            st.progress(progress)
            if progress < 1.0:
                st.markdown(
                    f"<p style='text-align: center; color: #FAFAFA;'>{text} ({int(progress * 100)}%)</p>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<p style='text-align: center; color: #00D26A; font-weight: bold;'>{text}</p>",
                    unsafe_allow_html=True,
                )
        time.sleep(duration / len(steps))

    return progress_placeholder


def render_processing_status(status: str, progress_value: float = None):
    """
    Render processing status with optional progress

    Args:
        status: Status message
        progress_value: Optional progress value (0.0 to 1.0)
    """
    if progress_value is not None:
        st.progress(progress_value)
        percentage = int(progress_value * 100)
        st.markdown(
            f"<p style='text-align: center; color: #FAFAFA;'>{status} ({percentage}%)</p>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<p style='text-align: center; color: #FAFAFA;'>{status}</p>",
            unsafe_allow_html=True,
        )
