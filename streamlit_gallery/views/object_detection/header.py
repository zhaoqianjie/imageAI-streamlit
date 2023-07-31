#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import NoReturn
import streamlit as st


def page_title_area(title: str) -> NoReturn:
    """
    标题栏内容
    :param title: 标题名称
    :return: None
    """
    col1, _, _, col4 = st.columns(4)
    title_container = st.container()
    with title_container:
        with col1:
            st.title(title)

        st.divider()


