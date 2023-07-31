#!/usr/bin/env python
# -*- coding: utf-8 -*-
import streamlit as st

from streamlit_gallery.views.object_detection.create_store import create_store_area
from streamlit_gallery.views.object_detection.header import page_title_area
from streamlit_gallery.views.object_detection.store import store_area


def main():
    # 标题区域
    page_title_area('目标检测')

    # 创建仓库区域
    create_store_area()

    # 仓库列表区域
    store_area()

    st.write("This is outside the container")


if __name__ == "__main__":
    main()
