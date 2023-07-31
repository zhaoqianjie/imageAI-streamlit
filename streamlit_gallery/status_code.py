#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class Status(Enum):
    OK = {200: "成功"}
    SUCCESS = {1: "成功"}
    FAIL = {0: "失败"}
    PARAM_IS_NULL = {2: "请求参数为空"}
    PARAM_ILLEGAL = {3: "请求参数非法"}
    JSON_PARSE_FAIL = {4: "JSON转换失败"}
    REPEATED_COMMIT = {5: "重复提交"}
    SQL_ERROR = {6: "数据库异常"}
    NOT_FOUND = {7: "无记录"}
    NETWORK_ERROR = {15: "网络异常"}
    UNKNOWN_ERROR = {99: "未知异常"}

    @property
    def code(self):
        """
        根据枚举名称取状态码code
        :return: 状态码code
        """
        return list(self.value.keys())[0]

    @property
    def msg(self):
        """
        根据枚举名称取状态说明message
        :return: 状态说明message
        """
        return list(self.value.values())[0]
