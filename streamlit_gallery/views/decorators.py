#!/usr/bin/env python
# -*- coding: utf-8 -*-

def update_kwargs(username, category):
    """
    添加用户名和类别的位置参数
    :param username: 用户名
    :param category: 类别
    :return: func
    """
    def decorator(func):
        def infunc(*args, **kwargs):
            kwargs = dict(**kwargs, **{"username": username, "category": category})
            return func(*args, **kwargs)

        return infunc

    return decorator
