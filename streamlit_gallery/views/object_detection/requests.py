#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import json
import os.path
import time
from io import BytesIO

import requests
import streamlit as st
from PIL import Image

from app import BASE_PATH
from streamlit_gallery.views.object_detection.config import USERNAME, CATEGORY, CATEGORY_KEY
from streamlit_gallery.views.decorators import update_kwargs
from streamlit_gallery.routers.object_detection import CREATE_STORE_URL, STORES_URL, UPLOAD_ZIP_URL, START_TRAIN_URL, \
    START_INFERENCE_URL, DETECTED_IMAGE_URL, UPDATE_TRAIN_IMAGES_URL
from streamlit_gallery.status_code import Status
from streamlit_gallery.text_collector import Btn, Msg


@update_kwargs(USERNAME, CATEGORY)
def create_store_request(**kwargs):
    """
    发送创建仓库的请求
    :param kwargs: 参数
    :return: None
    """
    # todo: 更换状态key
    response = requests.post(url=CREATE_STORE_URL, json=kwargs)
    # if response.json().get("code") == Status.OK.code:
    # 请求成功后记录响应
    self_name = create_store_request.__name__
    chain_key = "/".join([CATEGORY_KEY, kwargs['store_name'], self_name])
    if self_name not in st.session_state:
        st.session_state[chain_key] = response.json()


@update_kwargs(USERNAME, CATEGORY)
def get_stores(**kwargs):
    """
    获取仓库列表
    :param kwargs: 参数
    :return: 仓库列表
    """
    store_list = list()
    response = requests.get(url=STORES_URL, params=kwargs)
    # if response.json().get("code") == Status.OK.code:
    store_list = response.json().get("data", list())

    return store_list


@update_kwargs(USERNAME, CATEGORY)
def upload_file_request(file, **kwargs):
    """
    上传文件
    :param file: 文件
    :param kwargs: 参数
    :return: bool
    """
    response = requests.post(url=UPLOAD_ZIP_URL, files={"file": file}, data=kwargs)
    if response.json().get("code") == Status.OK.code:
        return True
    return False


@update_kwargs(USERNAME, CATEGORY)
def check_images_request(*args, **kwargs):
    """
    查看图片
    :param args: st容器
    :param kwargs: 参数
    :return: None
    """
    show_img = args[0]
    btn = kwargs["btn"]
    index = kwargs.get("image_info", dict()).get("image_index", 0)
    image_index_key = kwargs["image_index_key"]

    if not btn:
        pass
    elif btn == Btn.previous:
        index -= 1
    elif btn == Btn.next:
        index += 1
    kwargs.update({"index": index})
    response = requests.get(url=DETECTED_IMAGE_URL, params=kwargs)
    if response.json().get("code") == Status.OK.code:

        # 展示图片
        image_base64 = response.json().get("data").get("image_base64")
        index = response.json().get("data").get("index")
        total = response.json().get("data").get("total")
        image_name = response.json().get("data").get("image_name")
        image_byte = base64.b64decode(image_base64)

        st.session_state[image_index_key] = {"image_index": int(index), "image_name": image_name}

        image = Image.open(BytesIO(image_byte))
        with show_img:
            show_img.image(image, caption=image_name)

    else:
        show_img.warning(response.json().get("msg"))


@update_kwargs(USERNAME, CATEGORY)
def train_or_inference_clicked(*args, **kwargs):
    """
    点击启动训练或启动推理按钮的回调函数
    :param args: st的容器参数
    :param kwargs: 请求参数
    :return: None
    """
    container = args[0]
    btn = kwargs["btn"]
    if btn == Btn.train:
        url = START_TRAIN_URL
        # 启动训练时，将本地记录的图片审核状态更新到服务端
        images_status_path = os.path.join(BASE_PATH, "detected_images_status.json")
        with open(images_status_path, 'r') as f:
            status_str = f.read()
        if status_str:
            requests.post(UPDATE_TRAIN_IMAGES_URL, data={"images_status": status_str})

        # 清空本地图片审核状态
        with open(images_status_path, 'w') as f:
            f.write('')
    else:
        url = START_INFERENCE_URL
    response = requests.get(url, params=kwargs)
    # 给出提示，sleep结束后关闭
    notice = container.empty()
    if response.json().get("code") == Status.OK.code:
        notice.success(Msg.add_task_success)

    else:
        notice.warning(Msg.add_task_failed)
    time.sleep(2)
    notice.empty()


def update_detected_image_status(status_column, **kwargs):
    """
    更新图片的本地状态
    :param status_column: st容器
    :param kwargs: 参数
    :return: None
    """
    image_name = kwargs.get("image_info", dict()).get("image_name", None)
    btn_str = kwargs.get("btn", "")
    image_status = "Success" if btn_str == Btn.pass_one else "Failed"
    success_msg = "**:green[图片合格]**。\n\n将会用于后续的模型训练"
    failed_msg = "**:red[图片不合格]**。\n\n不会用于后续的模型训练"
    # 修改本地文件记录的图片状态
    images_status_path = os.path.join(BASE_PATH, "detected_images_status.json")
    image_status_dict = dict()
    with open(images_status_path) as f:
        f_read = f.read()
        if f_read:
            image_status_dict = json.loads(f_read)

    image_status_dict[image_name] = image_status

    with open(images_status_path, 'w') as f:
        json.dump(image_status_dict, f)

        # 将修改后的状态展示到状态栏
        status_column.write('')
        status_column.write('')
        status_column.markdown(success_msg if btn_str == Btn.pass_one else failed_msg)
    pass
