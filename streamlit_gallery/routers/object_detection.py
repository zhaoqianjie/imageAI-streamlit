#!/usr/bin/env python
# -*- coding: utf-8 -*-

from streamlit_gallery.routers import BASE_URL

# 创建仓库
CREATE_STORE_URL = BASE_URL + '/creat-store'
# 仓库列表
STORES_URL = BASE_URL + '/stores'
# 上传zip文件
UPLOAD_ZIP_URL = BASE_URL + '/action/upload-zip'
# 启动训练
START_TRAIN_URL = BASE_URL + '/action/start-train'
# 启动推理
START_INFERENCE_URL = BASE_URL + '/action/start-inference'
# 获取一张经过识别的图片
DETECTED_IMAGE_URL = BASE_URL + '/detected-image'
# 更新模型训练的图片集
UPDATE_TRAIN_IMAGES_URL = BASE_URL + '/action/update-train-images'
