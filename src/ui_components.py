import pandas as pd
import streamlit as st


def section_intro(title: str, copy: str) -> None:
    st.header(title)
    st.caption(copy)


def empty_state(tab_name: str) -> None:
    st.info(f"No demo rows are currently available for {tab_name.replace('_', ' ')}.")


def safe_table(frame: pd.DataFrame, tab_name: str, columns: list[str] | None = None) -> None:
    if frame.empty:
        empty_state(tab_name)
        return
    selected = [column for column in (columns or list(frame.columns)) if column in frame.columns]
    st.dataframe(frame[selected], width="stretch", hide_index=True)


def money(value) -> str:
    return f"${value:,.0f}" if pd.notna(value) else "-"


def number(value) -> str:
    return f"{value:,.0f}" if pd.notna(value) else "-"


def percent(value) -> str:
    return f"{value:.1%}" if pd.notna(value) else "-"
