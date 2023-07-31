import streamlit as st

from pathlib import Path


def main():
    st.markdown((Path(__file__).parents[2]/"README.md").read_text(encoding='utf-8'))


if __name__ == "__main__":
    main()
