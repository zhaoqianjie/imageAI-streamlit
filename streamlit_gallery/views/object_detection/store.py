#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from typing import NoReturn, Tuple
import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from streamlit_gallery.views.object_detection.requests import get_stores, upload_file_request, \
    check_images_request, train_or_inference_clicked, \
    update_detected_image_status
from streamlit_gallery.text_collector import Btn


def click_btn(**kwargs):
    """
    更新点击状态
    :param kwargs: 参数
    :return: None
    """
    store_line = kwargs.get('store_line', None)
    btn = kwargs.get('btn', None)
    # todo： 添加互斥，其他btn状态修改为False
    st.session_state[store_line][btn]["status"] = True


def report(text=""):
    """

    :param text:
    :return:
    """
    st.write(text)


def store_line(line_area: DeltaGenerator, store: str, btn_tuple: Tuple) -> NoReturn:
    """
    一行仓库的内容
    :param line_area: 仓库区域
    :param store: 仓库名
    :param btn_tuple: 上传按钮
    :param n: 第n行store
    :return: None
    """
    btn_num = len(btn_tuple)
    st_columns = line_area.columns(btn_num + 1)
    btn_id = dict((i, {'id': store + i + "btn", "status": False}) for i in btn_tuple)

    # 保存点击状态
    self_name = store_line.__name__ + str(store)
    if self_name not in st.session_state:
        st.session_state[self_name] = btn_id

    with line_area:
        with st_columns[0]:
            st.subheader(store)

        for index, btn in enumerate(btn_tuple):
            # 上传文件
            if btn == Btn.upload:
                upload_column = st_columns[index + 1]
                with upload_column:
                    upload_column.write('')
                    # 更新点击状态
                    upload_column.button(btn, key=btn_id[btn]['id'], on_click=click_btn,
                                         kwargs={"store_line": self_name, "btn": btn})

                    if st.session_state[self_name][btn]["status"]:
                        upload_container = line_area.empty()
                        success_notice = line_area.empty()
                        # key 不要用uuid
                        file = upload_container.file_uploader("上传ZIP压缩文件", key=store + 'upload')

                        # 上传成功给出提示，并销毁资源
                        if file and upload_file_request(file, store=store):
                            success_notice.success("上传成功")
                            st.session_state[self_name][btn]["status"] = False
                            time.sleep(2)
                            success_notice.empty()
                            upload_container.empty()
            # 启动训练
            elif btn == Btn.train:
                start_train_column = st_columns[index + 1]
                with start_train_column:
                    start_train_column.write('')
                    start_train_column.button(btn,
                                              on_click=train_or_inference_clicked,
                                              args=(line_area,),
                                              kwargs={"store": store, "btn": btn}
                                              )

            # 查看模型报告
            elif btn == Btn.report:
                upload_column = st_columns[index + 1]
                with upload_column:
                    upload_column.write('')
                    upload_column.button(btn)

            # 检视图片
            elif btn == Btn.check:
                check_images_column = st_columns[index + 1]
                with check_images_column:
                    check_images_column.write('')
                    check_images_column.button(btn, key=btn_id[btn]['id'], on_click=click_btn,
                                               kwargs={"store_line": self_name, "btn": btn}
                                               )

                    if st.session_state[self_name][btn]["status"]:
                        image_index_key = store + "image_index"
                        if image_index_key not in st.session_state:
                            st.session_state[image_index_key] = {"image_name": None, "image_index": 0}

                        image_info = st.session_state[image_index_key]
                        line_area.divider()
                        col1, col2, col3, col4 = line_area.columns([0.5, 0.1, 0.2, 0.2])
                        show_img = col1.empty()
                        check_images_request(show_img, btn=None, image_info=image_info, store=store,
                                             image_index_key=image_index_key)
                        # 上一张
                        col4.button(Btn.previous, on_click=check_images_request, args=(show_img,),
                                    kwargs={"btn": Btn.previous, "image_info": image_info,
                                            "image_index_key": image_index_key, "store": store})
                        # 不通过
                        col4.button(Btn.not_pass, on_click=update_detected_image_status, args=(col3,),
                                    kwargs={"btn": Btn.not_pass, "image_info": image_info,
                                            "image_index_key": image_index_key, "store": store})
                        # 通过
                        col4.button(Btn.pass_one, on_click=update_detected_image_status, args=(col3,),
                                    kwargs={"btn": Btn.pass_one, "image_info": image_info,
                                            "image_index_key": image_index_key, "store": store})
                        # 下一张
                        col4.button(Btn.next, on_click=check_images_request, args=(show_img,),
                                    kwargs={"btn": Btn.next, "image_info": image_info,
                                            "image_index_key": image_index_key, "store": store})

            # 启动推理
            elif btn == Btn.inference:
                start_inference_column = st_columns[index + 1]
                with start_inference_column:
                    start_inference_column.write('')
                    start_inference_column.button(btn,
                                                  on_click=train_or_inference_clicked,
                                                  args=(line_area,),
                                                  kwargs={"store": store, "btn": btn}
                                                  )

            # 下载报告
            elif btn == Btn.down_report:
                with st_columns[index + 1]:
                    st.write('')
                    st.button(btn, key=btn_id[btn]['id'])

        st.divider()


def store_area():
    """
    仓库列表区域
    :return: None
    """

    # 获取仓库列表
    store_list = get_stores()
    selected = st.selectbox(
        "请选择仓库",
        tuple(store_list)
    )

    st.write('选择的仓库为:', selected)
    st.divider()
    actions_area = st.container()
    store_line(actions_area, selected, (Btn.upload, Btn.train, Btn.report, Btn.check, Btn.inference, Btn.down_report))
