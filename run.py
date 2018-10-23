#!/usr/local/bin/python2
# -*- coding: UTF-8 -*-
# 自动化测试框架

"""
@version: 1.0
@author: huangyang
@license: personal
@file: run.py
@time: 2018-10-03
"""

import unittest
import HTMLTestRunner
import datetime
from config import globalparam


def run():
    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " 开始执行 \n"

    test_dir = './testcase'
    suite = unittest.defaultTestLoader.discover(start_dir=test_dir, pattern='test*.py')

    reportname = globalparam.report_path + '\\' + 'TestResult' + now + '.html'
    with open(reportname, 'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=f,
            title='测试报告',
            description='Test the import testcase'
        )
        runner.run(suite)

    print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " 结束执行 \n"


if __name__ == '__main__':
    run()
