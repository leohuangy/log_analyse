# coding=utf-8

"""
@version: 1.0
@author: huangyang
@license: personal
@file: run.py
@time: 2018-10-05
"""

import time
import os
from config import globalparam


class Export:
    def __init__(self, report_name=None, file_type=None):
        if not file_type:
            file_type = "xls"
        if not report_name:
            report_path = os.path.join(globalparam.report_path, ('{0}.' + file_type).format(time.strftime('%Y-%m-%d')))
        else:
            report_path = os.path.join(globalparam.report_path,
                                      ('{0}' + '-' + reportname + '.' + file_type).format(time.strftime('%Y-%m-%d')))

        self.report_name = report_path

    def export_to_xls(self, df, sheet_name):
        df.to_excel(self.report_name, sheet_name=sheet_name, index=False)
