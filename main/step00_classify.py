# -*- coding: utf-8 -*-
# @Time    : 2019/7/18 
# @Author  : ErichLee ErichLee@qq.com
# @File    : step00_classify.py
# @Comment : 
#            

import sys
import common_spider.telent_util as telnet_util
from sys_gl import *
from bs4 import BeautifulSoup
import os
import re

reload(sys)
sys.setdefaultencoding('utf-8')

global GLB_BATCH


def parse_html():
    lines = open('html_hulianwang.txt', 'r').readlines()
    soup = BeautifulSoup(''.join(lines), 'html5lib')
    a_list = soup.select('a[target="_blank"]')

    rt_msg = []
    for a in a_list:
        rt_msg.append('{} {}'.format(a['href'], a.select_one('strong').text.replace(' ', '')))
        # print a['href'],a.next_sibling.next_sibling.text
    with open('dict_topic_types_bak.txt', 'w') as file_dict:
        file_dict.writelines('\n'.join(rt_msg))


def start_classify():
    '''
    完成某一领域的所有分列
    :return:
    '''
    url = u'https://www.zhihu.com/topics#商业'

    params = {"topic_id": 19800, "offset": 20, "hash_id": "fcc43d9c351c395297d8a6bf6ba52f10"}
    msg = telnet_util.telnet_post(url, params)
    soup = BeautifulSoup(msg, 'html5lib')
    print soup


def init_find_offset():
    source_path = os.path.join(u'source', GLB_TYPE, 'step1')
    if not os.path.exists(source_path):
        os.makedirs(source_path)

    lines = open(os.path.join(source_path, 'dict_topic_types_bak.txt'), 'r').readlines()

    file_out = open(os.path.join(source_path, 'dict_topic_types.txt'), 'w')

    for line in lines:
        line_arr = line.strip().split(' ')
        next_url = 'https://www.zhihu.com{}/newest'.format(line_arr[0])
        # next_url = 'https://www.zhihu.com/topic/19551404/newest'
        msg = telnet_util.telnet_question_ask(next_url)
        # msg = 'ent_count%3B&limit=5&offset=1564393599.0"}'
        print 'telnet', next_url

        try:
            rt = re.search('&offset=([^"]*)\"', msg)
            if rt:
                offset = rt.group(1)
                write_msg = '{} {} {}\n'.format(line_arr[0], line_arr[1], offset)
                file_out.write(write_msg)
                # print write_msg
        except Exception as e:
            print e
            continue
    file_out.close()


# s1 html解析
# parse_html()

# s2 处理文本
init_find_offset()
