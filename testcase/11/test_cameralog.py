#!/usr/local/bin/python2
# -*- coding: UTF-8 -*-
# 自动化测试框架

"""
@author: chunyuzhang
@license: (C) Copyright
@contact: chunyu.zhang@unisoc.com
@file: test_carmeralog.py
@time: 2018/10/5 下午5:48
@desc: 相机时延测试日志分析
"""

import unittest
import os
import pandas as pd
import time
from config import globalparam
from libs.common.log import Log
from libs.common.export import Export


class TestCameraLog(unittest.TestCase):
    data_list = pd.DataFrame(columns=["date", "time", "type", "act0", "act1", "act2", "act3"])  # 重要指标数据
    report_name = 'xiangjiceshi'  # sheet名称
    report_columns = ['case', 'time1', 'time2', 'time3', 'avg']  # 报表表头
    report_data = {"case": [], "time1": [], "time2": [], "time3": [], "avg": []}  # 报表数据字典

    """照相机自动化测试--日志分析"""

    @classmethod
    def setUpClass(cls):
        print " 用例集合开始执行 \n"
        # 数据日志文件存放路径
        cls.logdir = os.path.join(globalparam.data_path, '20181211')
        # 存放统计所需的日志相关字段
        cls.logger = Log()
        cls.reporter = Export()

    """
    case1
    测试用例-热启动
    User版本暂无相关关键字，后续关注
    """

    def _test_reqidong(self):
        """筛选log的开始和结束关键词"""
        log_file = "reqidong.log"  # 日志文件名
        case_name = "reqidong"  # 报表sheet的名称
        star_act = ['CAM_QuickActivity:', 'START', 'onStart:']  # 开始
        end_act1 = ['CAM_RoundedThumbnailVie:', 'END', '---']  # 结束1
        end_act2 = ['CAM_RoundedThumbnailVie:', 'set', 'END']  # 结束2

        df = self.read_log(log_file) if self.data_list.empty is True else self.data_list
        # dataframe对象
        target1 = df.loc[(df['act0'] == star_act[0]) & (df['act1'] == star_act[1]) & (df['act2'] == star_act[2])]
        target2 = df.loc[(df['act0'] == end_act1[0]) & (df['act2'] == end_act1[1]) & (df['act3'] == end_act1[2])]
        target3 = df.loc[(df['act0'] == end_act2[0]) & (df['act2'] == end_act2[1]) & (df['act3'] == end_act2[2])]

        self.save_data(case_name, target1, target2, target3)

    """
    case2
    测试用例-正常拍照
    """

    def test_zhengchangpaizhao(self):
        """筛选log的开始和结束关键词"""
        log_file = "zhengchangpaizhao.log"  # 日志文件名
        cese_name = "zhengchangpaizhao"  # 报表sheet的名称
        star_act = ['CAM_ShutterButton:', 'ShutterButton', 'performClick']  # 开始
        end_act1 = ['CAM_RoundedThumbnailVie:', 'END', '---']  # 结束1
        end_act2 = ['CAM_RoundedThumbnailVie:', 'set', 'END']  # 结束2
        ignore_log_line = [1]  # 忽略的日志行数

        df = self.read_log(log_file) if self.data_list.empty is True else self.data_list
        # dataframe对象
        target1 = df.loc[(df['act0'] == star_act[0]) & (df['act1'] == star_act[1]) & (df['act2'] == star_act[2])]
        target2 = df.loc[(df['act0'] == end_act1[0]) & (df['act2'] == end_act1[1]) & (df['act3'] == end_act1[2])]
        target3 = df.loc[(df['act0'] == end_act2[0]) & (df['act2'] == end_act2[1]) & (df['act3'] == end_act2[2])]
        target1.index = range(1, len(target1) + 1)
        target2.index = range(1, len(target2) + 1)
        target3.index = range(1, len(target3) + 1)
        # print target1
        # print target2
        # print target3
        # print "start--------------------"
        target2.drop(ignore_log_line, inplace=True)
        target3.drop(ignore_log_line, inplace=True)
        # print "end--------------------"

        self.save_data(cese_name, target1, target2, target3)

    """
    case3
    测试用例-DC切DV
    """

    def test_dcqiedv(self):
        """筛选log的开始和结束关键词"""
        log_file = "dcqiedv.log"  # 日志文件名
        case_name = "dcqiedv"  # 报表sheet的名称
        star_act = ['CAM_CameraActivity', 'Drea:', 'switchMode']  # 开始
        end_act1 = ['CAM_ModeTransView:', 'hideImageCover']  # 结束1
        ignore_log_line = [2, 4, 6]  # 忽略的日志行数
        # end_act2 = ['CAM', 'ModeTransView', 'hideImageCover']# 结束2

        df = self.read_log(log_file) if self.data_list.empty is True else self.data_list
        # dataframe对象
        target1 = df.loc[(df['act0'] == star_act[0]) & (df['act1'] == star_act[1]) & (df['act2'] == star_act[2])]
        target2 = df.loc[(df['act0'] == end_act1[0]) & (df['act1'] == end_act1[1])]
        target1.index = range(1, len(target1) + 1)
        target2.index = range(1, len(target2) + 1)
        # print "start--------------------"
        target1.drop(ignore_log_line, inplace=True)
        target2.drop(ignore_log_line, inplace=True)
        # print "end--------------------"
        # print target1
        # print target2
        # exit(0)

        self.save_data1(case_name, target1, target2)

    """
    case4
    测试用例-美颜拍照
    """

    def test_meiyan(self):
        """筛选log的开始和结束关键词"""
        log_file = "meiyan.log"  # 日志文件名
        case_name = "meiyan"  # 报表sheet的名称
        star_act = ['CAM_ShutterButton:', 'ShutterButton', 'performClick']  # 开始
        end_act1 = ['CAM_RoundedThumbnailVie:', 'END', '---']  # 结束1
        end_act2 = ['CAM_RoundedThumbnailVie:', 'set', 'END']  # 结束2

        df = self.read_log(log_file) if self.data_list.empty is True else self.data_list

        target1 = df.loc[(df['act0'] == star_act[0]) & (df['act1'] == star_act[1]) & (df['act2'] == star_act[2])]
        target2 = df.loc[(df['act0'] == end_act1[0]) & (df['act2'] == end_act1[1]) & (df['act3'] == end_act1[2])]
        target3 = df.loc[(df['act0'] == end_act2[0]) & (df['act2'] == end_act2[1]) & (df['act3'] == end_act2[2])]
        # print target1
        # print target2
        # print target3

        self.save_data(case_name, target1, target2, target3)

    @classmethod
    def tearDownClass(cls):
        """输出结果到excel"""
        # print cls.report_data
        cls.reporter.export_to_xls(pd.DataFrame(cls.report_data, columns=cls.report_columns), cls.report_name)
        print "用例集合结束执行 \n"

    """特殊形式日期计算差值"""

    @staticmethod
    def str2time(start_str, end_str):
        start_list = start_str.split('.')
        start_time_second = float(time.mktime(time.strptime(start_list[0], "%Y-%m-%d %H:%M:%S")))  # 秒级数字
        start_time_mcrosec = float(start_list[1]) / 1000  # 毫秒级数字

        end_list = end_str.split('.')
        end_time_second = float(time.mktime(time.strptime(end_list[0], "%Y-%m-%d %H:%M:%S")))  # 秒级数字
        end_time_mcrosec = float(end_list[1]) / 1000  # 毫秒级数字

        _time = ((end_time_second - start_time_second) + (end_time_mcrosec - start_time_mcrosec)) * 1000

        return int(_time)

    """取平均数"""

    @staticmethod
    def average_num(num):
        nsum = 0
        for i in range(len(num)):
            nsum += num[i]
        return nsum / len(num)

    """读取日志中的数据源"""

    def read_log(self, log_file):
        columns = ["id1", "date", "time", "id2", "id3", "type", "act0", "act1", "act2", "act3", "other1", "other2",
                   "other3"]
        use_columns = ["date", "time", "type", "act0", "act1", "act2", "act3"]
        logfile = os.path.join(self.logdir, log_file)
        # 将统计的字段读入到dataframe中
        reader = pd.read_table(logfile, sep='\s+', engine='c', names=columns,
                               usecols=use_columns,
                               header=None,
                               iterator=True)
        loop = True
        chunksize = 100000
        chunks = []
        while loop:
            try:
                chunk = reader.get_chunk(chunksize)
                chunks.append(chunk)
            except StopIteration:
                loop = False
                # print "Iteration is stopped."

        df = pd.concat(chunks)
        if self.data_list.empty is True:
            self.data_list = df
        return df

    """处理正常拍照平均时间"""

    def save_data(self, case_name, target1, target2, target3):
        time_used_list = []
        self.report_data['case'].append(case_name)
        for i in range(0, len(target1)):
            time_start_str = '2018-' + target1.iloc[i]['date'] + ' ' + target1.iloc[i]['time']
            time_end_str1 = '2018-' + target2.iloc[i]['date'] + ' ' + target2.iloc[i]['time']
            time_end_str2 = '2018-' + target3.iloc[i]['date'] + ' ' + target3.iloc[i]['time']
            time_use1 = self.str2time(time_start_str, time_end_str1)
            time_use2 = self.str2time(time_start_str, time_end_str2)
            time_use = time_use1 if time_use1 > time_use2 else time_use2
            time_used_list.append(time_use)
            _time = 'time' + str(i + 1)
            self.report_data[_time].append(time_use)
            # print '开始', time_start_str
            # print '结束1', time_end_str1
            # print '结束2', time_end_str2
            # print time_use1
            # print time_use2
            # print '用时：', time_use, '毫秒'

        time_avg = self.average_num(time_used_list)
        self.report_data['avg'].append(time_avg)

        """打印指标和结果到log"""
        # self.logger.debug(target1[use_columns])  # 指标1
        # self.logger.debug(target2[use_columns])  # 指标2
        # self.logger.debug(target3[use_columns])  # 指标3
        # self.logger.debug(df)  # 用时报表

    """处理DC切DV平均时间"""

    def save_data1(self, case_name, target1, target2):
        time_used_list = []
        self.report_data['case'].append(case_name)
        for i in range(0, len(target1)):
            time_start_str = '2018-' + target1.iloc[i]['date'] + ' ' + target1.iloc[i]['time']
            time_end_str1 = '2018-' + target2.iloc[i]['date'] + ' ' + target2.iloc[i]['time']
            time_use = self.str2time(time_start_str, time_end_str1)
            time_used_list.append(time_use)
            _time = 'time' + str(i + 1)
            self.report_data[_time].append(time_use)
            # print '开始', time_start_str
            # print '结束1', time_end_str1
            # print '结束2', time_end_str2
            # print time_use1
            # print time_use2
            # print '用时：', time_use, '毫秒'

        time_avg = self.average_num(time_used_list)
        self.report_data['avg'].append(time_avg)

        """打印指标和结果到log"""
        # self.logger.debug(target1[use_columns])  # 指标1
        # self.logger.debug(target2[use_columns])  # 指标2
        # self.logger.debug(target3[use_columns])  # 指标3
        # self.logger.debug(df)  # 用时报表


if __name__ == '__main__':
    unittest.main()
