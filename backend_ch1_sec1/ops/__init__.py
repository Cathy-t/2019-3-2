#!/usr/bin/python
# -*-encoding=utf8 -*-

# 自定义过滤器
# 返回 False 即为无用参数

import logging


class TestFilter(logging.Filter):

    # record 即每条日志具体的内容
    def filter(self, record):
        if '----' in record.msg:
            return False
        else:
            return True
