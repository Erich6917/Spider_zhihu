# -*- coding: utf-8 -*-
# @Time    : 2019/7/12
# @Author  : ErichLee ErichLee@qq.com
# @File    : step02_simple_topic_list.py
# @Comment :
#

import os
import sys

import util.file_check_util as file_util
from sys_gl import *
import socket

timeout = 20
socket.setdefaulttimeout(timeout)

reload(sys)
sys.setdefaultencoding('utf-8')
'''
    针对下载的连接去重
    
'''
global GLB_BATCH


def start_simple_list():
    source_path = u'source_finance/{}'.format(GLB_BATCH)
    output_path = u'source_finance_simple/{}'.format(GLB_BATCH)

    source_path = os.path.join(u'source', GLB_TYPE, 'step1', GLB_BATCH)
    output_path = os.path.join(u'source', GLB_TYPE, 'step2', GLB_BATCH)

    file_list = file_util.get_all_files_path_name_endswith(source_path, 'url_questions.txt')

    for filename, path, root in file_list:
        print filename, path, root
        lines = open(path, 'r').readlines()
        write_msg = []
        qt_list = []
        for line in lines:
            question = line.strip().split('\t')[0]
            if question not in qt_list:
                write_msg.append(line)
                qt_list.append(question)
        # 输出
        print len(lines), len(write_msg)

        output_root = root.replace(source_path, output_path)
        if not os.path.exists(output_root):
            os.makedirs(output_root)
        with open(os.path.join(output_root, filename), 'a+') as output_file:
            output_file.writelines(write_msg)


start_simple_list()
