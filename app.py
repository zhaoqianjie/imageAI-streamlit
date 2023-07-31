import os

import streamlit as st

from streamlit_gallery import views, readme
from streamlit_gallery.utils.page import page_group

page = page_group("p")
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def main():
    with st.sidebar:
        st.title("🎈 balloon")

        with st.expander("🧩 类别", True):
            page.item("ReadMe", readme.gallery, default=True)
            page.item("目标检测", views.object_detection)

    page.show()


if __name__ == "__main__":
    st.set_page_config(page_title="Streamlit Gallery by Okld", page_icon="?", layout="wide")

    main()
