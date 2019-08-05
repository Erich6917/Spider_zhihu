# -*- coding: utf-8 -*-
# @Time    : 2019/7/12
# @Author  : ErichLee ErichLee@qq.com
# @File    : step02_simple_topic_list.py
# @Comment :
#

import os
import sys

import shutil

import util.file_check_util as file_util
from sys_gl import *

reload(sys)
sys.setdefaultencoding('utf-8')
'''
    数据过滤
    
'''


def start_clean_data():
    # source_path = u'source_finance_download/{}'.format(GLB_BATCH)
    # output_path = u'source_finance_commit/{}'.format(GLB_BATCH)

    source_path = os.path.join(u'source', GLB_TYPE, 'step3', GLB_BATCH)
    output_path = os.path.join(u'source', GLB_TYPE, 'step4', GLB_BATCH)

    commit_path = os.path.join(u'source', GLB_TYPE, 'commit', GLB_BATCH)
    if not os.path.exists(commit_path):
        os.makedirs(commit_path)

    file_list = file_util.get_all_files_path_name_endswith(source_path, '.txt')

    for filename, path, root in file_list:
        print filename, path, root
        lines = open(path, 'r').readlines()
        # 只保留文件内容大于一行的数据
        if len(lines) > 1:
            write_msg = []
            for line in lines:
                if not line.startswith('ANSWERS_INFO_'):
                    write_msg.append(line)
            # 输出

            output_root = root.replace(source_path, output_path)
            if not os.path.exists(output_root):
                os.makedirs(output_root)
            output_file = os.path.join(output_root, filename)
            with open(output_file, 'a+') as file_output:
                file_output.writelines(write_msg)

            # cp commit file
            commit_file_path = o    s.path.join(commit_path, filename)
            cp_commit_file(output_file, commit_file_path)


def cp_commit_file(input_path, output_path):
    # print input_path, output_path
    shutil.copyfile(input_path, output_path)


start_clean_data()
