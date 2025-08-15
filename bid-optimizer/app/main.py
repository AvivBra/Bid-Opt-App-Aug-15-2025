import streamlit as st
from ui.page import render_page


def main():
    """נקודת כניסה ראשית לאפליקציה"""
    st.set_page_config(
        page_title="Bid Optimizer - Bulk File",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    render_page()


if __name__ == "__main__":
    main()
