"""
Reusable UI widgets and components - No emojis or icons
"""

import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from typing import Optional, List, Tuple
from config.constants import TEMPLATE_REQUIRED_COLUMNS


def file_uploader(
    label: str,
    key: str,
    accept_types: List[str] = ["xlsx", "csv"],
    help_text: Optional[str] = None,
) -> Optional[BytesIO]:
    """Create a file uploader widget"""
    uploaded_file = st.file_uploader(label, type=accept_types, key=key, help=help_text)

    if uploaded_file is not None:
        # Show file info
        col1, col2 = st.columns([3, 1])
        with col1:
            st.caption(f"{uploaded_file.name}")
        with col2:
            size_mb = uploaded_file.size / (1024 * 1024)
            st.caption(f"Size: {size_mb:.2f} MB")

    return uploaded_file


def download_button(
    label: str,
    data: bytes or BytesIO,
    filename: str,
    mime_type: str = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    key: Optional[str] = None,
    button_type: str = "primary",
) -> bool:
    """Create a download button"""
    use_container_width = True

    if button_type == "primary":
        return st.download_button(
            label=label,
            data=data,
            file_name=filename,
            mime=mime_type,
            key=key,
            use_container_width=use_container_width,
            type="primary",
        )
    else:
        return st.download_button(
            label=label,
            data=data,
            file_name=filename,
            mime=mime_type,
            key=key,
            use_container_width=use_container_width,
        )


def create_empty_template() -> BytesIO:
    """Create an empty template file"""
    df = pd.DataFrame(columns=TEMPLATE_REQUIRED_COLUMNS)

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Template")

    buffer.seek(0)
    return buffer


def optimization_selector() -> List[str]:
    """Create optimization type selector"""
    st.subheader("Select Optimization Types")

    selected = []

    # In mockup, only one optimization type
    if st.checkbox("Zero Sales", key="opt_zero_sales"):
        selected.append("Zero Sales")

    # Future optimization types (disabled in mockup)
    with st.expander("Future Optimization Types (Coming Soon)", expanded=False):
        st.caption("• Portfolio Bid Optimization")
        st.caption("• Budget Optimization")
        st.caption("• Keyword Optimization")
        st.caption("• Product Targeting Optimization")
        st.caption("• And more...")

    return selected


def show_file_status(template_file: Optional[BytesIO], bulk_file: Optional[BytesIO]):
    """Show status of uploaded files"""
    col1, col2 = st.columns(2)

    with col1:
        if template_file:
            st.info("**Template:** Uploaded")
        else:
            st.info("**Template:** Not uploaded")

    with col2:
        if bulk_file:
            st.info("**Bulk File:** Uploaded")
        else:
            st.info("**Bulk File:** Not uploaded")


def copy_to_clipboard_button(
    text: str, button_label: str = "Copy to Clipboard"
) -> bool:
    """Create a copy to clipboard button"""
    button_clicked = st.button(button_label, use_container_width=True)

    if button_clicked:
        # Note: Actual clipboard functionality requires JavaScript
        # This is a mockup, so we'll just show a success message
        st.success("Copied to clipboard!")

        # Display the text that would be copied
        with st.expander("Copied text:", expanded=True):
            st.code(text, language=None)

    return button_clicked


def action_button(
    label: str,
    key: Optional[str] = None,
    disabled: bool = False,
    button_type: str = "primary",
    use_full_width: bool = True,
) -> bool:
    """Create an action button"""
    if button_type == "primary":
        return st.button(
            label,
            key=key,
            disabled=disabled,
            type="primary",
            use_container_width=use_full_width,
        )
    else:
        return st.button(
            label, key=key, disabled=disabled, use_container_width=use_full_width
        )


def generate_filename(file_type: str) -> str:
    """Generate filename with timestamp"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M")
    return f"Auto Optimized Bulk | {file_type} | {date_str} | {time_str}.xlsx"


def show_step_indicator(current_step: int):
    """Show step progress indicator"""
    steps = ["Upload", "Validate", "Output"]

    # Create progress bar
    progress = (current_step - 1) / (len(steps) - 1)
    st.progress(progress)

    # Show step labels
    cols = st.columns(len(steps))
    for i, (col, step_name) in enumerate(zip(cols, steps), 1):
        with col:
            if i < current_step:
                st.markdown(f"**{i}. {step_name}** [Complete]")
            elif i == current_step:
                st.markdown(f"**{i}. {step_name}** [Current]")
            else:
                st.markdown(f"{i}. {step_name}")
