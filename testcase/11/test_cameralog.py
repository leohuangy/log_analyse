#!/usr/local/bin/python2
# -*- coding: UTF-8 -*-
# 自动化测试框架

"""
@author: huangyang
@license: (C) Copyright
@contact: leohuang0112@gmail.com
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
    """照相机自动化测试--日志分析"""

    @classmethod
    def setUpClass(cls):
        print " 用例集合开始执行 \n"
        # 数据日志文件存放路径
        cls.logdir = os.path.join(globalparam.data_path, '20181023')
        # 存放统计所需的日志相关字段
        cls.logger = Log()
        cls.reporter = Export()

    """
    case1
    测试用例-热启动
    需要定义指标列的参照
    """

    def test_reqidong(self):
        """筛选log的开始和结束关键词"""
        log_file = "reqidong.log"  # 日志文件名
        report_name = "reqidong"  # 报表sheet的名称
        star_act = ['CAM_QuickActivity:', 'START', 'onStart:']  # 开始
        end_act1 = ['CAM_RoundedThumbnailVie:', 'END', '---']  # 结束1
        end_act2 = ['CAM_RoundedThumbnailVie:', 'set', 'END']  # 结束2
        rp_title = ["Num", "Used-Times(mecroseconds)"]  # 报表列名

        self.run_log(log_file, report_name, star_act, end_act1, end_act2, rp_title)

    """
    case2
    测试用例-正常拍照(没找到日志)
    需要定义指标列的参照
    """

    def _test_zhengchangpaizhao(self):
        """筛选log的开始和结束关键词"""
        log_file = "zhengchangpaizhao.log"  # 日志文件名
        report_name = "zhengchangpaizhao"  # 报表sheet的名称
        star_act = ['CAM_ShutterButton:', 'ShutterButton', 'performClick']  # 开始
        end_act1 = ['CAM_RoundedThumbnailVie:', 'END', '---']  # 结束1
        end_act2 = ['CAM_RoundedThumbnailVie:', 'set', 'END']  # 结束2
        rp_title = ["Num", "Used-Times(mecroseconds)"]  # 报表列名

        self.run_log(log_file, report_name, star_act, end_act1, end_act2, rp_title)

    """
    case3
    测试用例-DC切DV(日志开始指标和结束次数不符)
    需要定义指标列的参照
    """

    def _test_dcqiedv(self):
        """筛选log的开始和结束关键词"""
        log_file = "dcqiedv.log"  # 日志文件名
        report_name = "dcqiedv"  # 报表sheet的名称
        star_act = ['CAM_CameraActivity', 'Drea:', 'switchMode']  # 开始
        end_act1 = ['CAM_RoundedThumbnailVie:', 'END', '---']  # 结束1
        end_act2 = ['CAM_RoundedThumbnailVie:', 'set', 'END']  # 结束2
        rp_title = ["Num", "Used-Times(mecroseconds)"]  # 报表列名

        self.run_log(log_file, report_name, star_act, end_act1, end_act2, rp_title)

    @classmethod
    def tearDownClass(cls):
        print "用例集合结束执行 \n"

    """特殊形式日期计算差值"""

    def str2time(self, start_str, end_str):
        start_list = start_str.split('.')
        start_time_second = float(time.mktime(time.strptime(start_list[0], "%Y-%m-%d %H:%M:%S")))  # 秒级数字
        start_time_mcrosec = float(start_list[1]) / 1000  # 毫秒级数字

        end_list = end_str.split('.')
        end_time_second = float(time.mktime(time.strptime(end_list[0], "%Y-%m-%d %H:%M:%S")))  # 秒级数字
        end_time_mcrosec = float(end_list[1]) / 1000  # 毫秒级数字
        # print end_time_second - start_time_second
        # print end_time_mcrosec - start_time_mcrosec

        _time = ((end_time_second - start_time_second) + (end_time_mcrosec - start_time_mcrosec)) * 1000

        return int(_time)

    """取平均数"""

    def averagenum(self, num):
        nsum = 0
        for i in range(len(num)):
            nsum += num[i]
        return nsum / len(num)

    """读取日志中的数据源并处理平均时间"""

    def run_log(self, log_file, report_name, star_act, end_act1, end_act2, rp_title):
        columns = ["ids", "date", "time", "id1", "id2", "type", "act0", "act1", "act2", "act3", "other1", "other2"]
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
                print "Iteration is stopped."

        df = pd.concat(chunks)
        # print df
        target1 = df.loc[
            (df['act0'] == star_act[0]) & (df['act1'] == star_act[1]) & (df['act2'] == star_act[2])]
        target2 = df.loc[(df['act0'] == end_act1[0]) & (df['act2'] == end_act1[1]) & (df['act3'] == end_act1[2])]
        target3 = df.loc[(df['act0'] == end_act2[0]) & (df['act2'] == end_act2[1]) & (df['act3'] == end_act2[2])]
        # print target1
        # print target2
        # print target3

        time_used_list = []
        df = pd.DataFrame(columns=rp_title)
        for i in range(0, len(target1)):
            time_start_str = '2018-' + target1.iloc[i]['date'] + ' ' + target1.iloc[i]['time']
            time_end_str1 = '2018-' + target2.iloc[i]['date'] + ' ' + target2.iloc[i]['time']
            time_end_str2 = '2018-' + target3.iloc[i]['date'] + ' ' + target3.iloc[i]['time']
            time_use1 = self.str2time(time_start_str, time_end_str1)
            time_use2 = self.str2time(time_start_str, time_end_str2)
            time_use = time_use1 if time_use1 > time_use2 else time_use2
            time_used_list.append(time_use)
            df = df.append({rp_title[0]: i + 1, rp_title[1]: time_use}, ignore_index=True)
            # print '开始', time_start_str
            # print '结束1', time_end_str1
            # print '结束2', time_end_str2
            # print time_use1
            # print time_use2
            # print '用时：', time_use, '毫秒'

        time_avg = self.averagenum(time_used_list)
        df = df.append({rp_title[0]: 'avg', rp_title[1]: time_avg}, ignore_index=True)
        # print df

        """打印指标和结果到log"""
        # self.logger.debug(target1[use_columns])  # 指标1
        # self.logger.debug(target2[use_columns])  # 指标2
        # self.logger.debug(target3[use_columns])  # 指标3
        # self.logger.debug(df)  # 用时报表

        """输出结果到excel"""
        self.reporter.export_to_xls(df, report_name)


if __name__ == '__main__':
    unittest.main()
