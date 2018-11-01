#!/usr/local/bin/python2
# -*- coding: UTF-8 -*-
# 自动化测试框架

"""
@version: 1.0
@author: huangyang
@license: personal
@file: run.py
@time: 2018-10-03
@desc 如需置顶testcase目录，则直接python run.py 11即可，11为testcase下的目录名称，默认情况直接python run.py即可跑所有testcase下面的用例
"""

import unittest
import datetime
import sys


def run(test_case):
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " 开始执行 \n"
    test_dir = './testcase'
    if test_case != 'all':
        test_dir += '/' + test_case

    print test_dir
    suite = unittest.defaultTestLoader.discover(start_dir=test_dir, pattern='test*.py')
    runner = unittest.TextTestRunner()
    runner.run(suite)

    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " 结束执行 \n"


if __name__ == '__main__':
    # print sys.argv
    test_case = sys.argv[1] if len(sys.argv) > 1 else 'all'
    run(test_case)
