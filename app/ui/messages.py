"""
Message display utilities - No emojis or icons
"""

import streamlit as st
from typing import Optional


def show_error(message: str):
    """Display error message"""
    st.error(message)


def show_success(message: str):
    """Display success message"""
    st.success(message)


def show_warning(message: str):
    """Display warning message"""
    st.warning(message)


def show_info(message: str):
    """Display info message"""
    st.info(message)


def show_pink_notice(message: str):
    """Display pink notice for calculation errors"""
    st.markdown(
        f"""
        <div class="pink-notice">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_portfolio_list(portfolios: list, title: str = "Portfolios"):
    """Display a list of portfolios in a formatted box"""
    if not portfolios:
        return

    portfolio_text = "\n".join([f"• {p}" for p in portfolios])

    st.markdown(
        f"""
        <div class="portfolio-list">
            <strong>{title} ({len(portfolios)}):</strong><br>
            <pre>{portfolio_text}</pre>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_metric(label: str, value: str or int, delta: Optional[str] = None):
    """Display a metric with optional delta"""
    st.metric(label=label, value=value, delta=delta)


def show_custom_metric(label: str, value: str or int):
    """Display a custom styled metric"""
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def clear_messages():
    """Clear all messages from the page"""
    # This is handled by session state
    pass


def show_spinner(message: str = "Processing..."):
    """Show a loading spinner with message"""
    return st.spinner(message)


def show_progress(value: int, max_value: int = 100, text: str = "Progress"):
    """Show a progress bar"""
    progress = value / max_value
    st.progress(progress, text=f"{text}: {value}/{max_value}")
