#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from typing import NoReturn

import streamlit as st

from streamlit_gallery.views.object_detection.config import CATEGORY_KEY
from streamlit_gallery.views.object_detection.requests import create_store_request


def create_store_area() -> NoReturn:
    """
    创建仓库
    :return: None
    """
    col1, col2, col3, col4, col5, col6, col7,_,_ = st.columns(9)
    with st.container():
        with col1:
            st.write("")
            st.write("")
            st.write("仓库名称：")
        with col2:
            store_name = st.text_input(
                label="placeholder",
                label_visibility="hidden",
                key="store_name"
            )
        with col4:
            st.write("")
            st.write("")
            st.button('提交', on_click=create_store_request, kwargs={'store_name': store_name})

        # 创建仓库请求成功后给出提示
        self_name = create_store_request.__name__
        chain_key = "/".join([CATEGORY_KEY, store_name, self_name])
        response = st.session_state.get(chain_key, dict())

        with col5:
            st.write("")
            st.write("")

            notice = st.empty()
            with notice.empty():
                # todo：使用框架的通知组件
                notice.write(response.get('msg') if response else "")
                time.sleep(2)
                notice.empty()

            # 从状态管理中擦除接口响应
            st.session_state[chain_key] = None

        st.divider()
