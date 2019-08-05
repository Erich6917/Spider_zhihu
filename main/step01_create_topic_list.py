# -*- coding: utf-8 -*-
# @Time    : 2019/7/12
# @Author  : ErichLee ErichLee@qq.com
# @File    : hot_list.py
# @Comment :
#

import json
import math
import os
import re
import sys
from sys_gl import *

from bs4 import BeautifulSoup

import common_spider.telent_util as telnet_util

reload(sys)
sys.setdefaultencoding('utf-8')

global GLB_BATCH

url_query_question_answers = 'https://www.zhihu.com/api/v4/questions/{question_id}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={offset}&platform=desktop&sort_by=default'


def example_find_answers():
    # ASK ANSWER
    # 具体问题
    question_id = 333784019
    url = 'https://www.zhihu.com/question/333280072'
    url = 'https://www.zhihu.com/question/333784019'
    msg_question = telnet_util.telnet_question_ask(url)
    # print msg_question
    # find total_answers
    soup = BeautifulSoup(msg_question, 'html5lib')
    # print soup
    # print soup.select('meta[itemprop="zhihu:followerCount"]')
    msg_total = soup.select_one('div.Card.AnswersNavWrapper span').text
    page_total = int(re.sub('[^0-9]', '', msg_total))
    print page_total

    page_limit = 5
    page_size = int(math.ceil(1.0 * page_total / page_limit))
    for page_index in range(0, page_size):
        page_offset = page_index * page_limit
        print page_total, page_offset

        # page_offset = 5
        url = url_query_question_answers.format(question_id=question_id, offset=page_offset)
        msg_answers = telnet_util.telnet_question_ask(url)
        # print msg_question
        parse_get_answers(msg_answers)
        if True:
            return


def parse_get_answers(line):
    # lines = open('source/d1.txt', 'a+')
    # for line in lines:
    js = json.loads(line)
    if 'data' in js:
        data = js['data']
        for each in data:
            content = each['content']
            soup = BeautifulSoup(content, 'html5lib')
            p_list = soup.select('p')
            p_msg = [p.text for p in p_list]
            print each['id'], each['author'].get('name'), each['author'].get('url_token'), each[
                'created_time'], each['updated_time'], "\n".join(p_msg)


def parse_get_finance(line):
    # lines = open('source/d1.txt', 'a+')
    # for line in lines:
    js = json.loads(line)
    next_url = ''
    msg_write = []
    # print js
    if 'data' in js:
        data = js['data']

        for each in data:
            target = each.get('target')
            if target:
                question = target.get('question')
                if question:
                    question_id = question.get('id')
                    question_title = question.get('title')
                    question_created = question.get('created')
                    updated_time = question.get('created')
                    question_url = 'https://www.zhihu.com/question/{}'.format(question_id)
                    print_msg = 'QUESTION {}\t{}\t{}\t{}\t{}\n'.format(question_id, question_created,
                                                                       updated_time, question_url, question_title)
                    msg_write.append(print_msg)
                    # print print_msg
    else:
        print '未查询到内容.....'
        return

    if 'paging' in js:
        paging = js['paging']
        next_url = paging.get('next').strip()

    return (next_url, msg_write)


url_init = 'https://www.zhihu.com/api/v4/topics/{}/feeds/timeline_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=5&offset={}'


def main_start_tops_finance(topic_id, title_name, offset):
    # url_main = 'https://www.zhihu.com/topics'
    # 金融 》 金融
    # url_finance = u'https://www.zhihu.com/topic/19609455/hot'
    # url = u'https://www.zhihu.com/topic/19609455/newest'
    # source_path = u'source_finance'
    # next_url = open(u'source/finance/url_start.txt').readline()

    output_path = os.path.join(u'source', GLB_TYPE, 'step1', GLB_BATCH, title_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    url_telnet_log = open(os.path.join(output_path, u'url_telnet_log.log'), 'w')
    url_questions = open(os.path.join(output_path, u'url_questions.txt'), 'w')

    next_url = url_init.format(topic_id, offset)

    while (next_url):
        print 'telnet:', test_get_offset(next_url)
        msg = telnet_util.telnet_question_ask(next_url)
        if msg:
            next_url, msg_write = parse_get_finance(line=msg)
            if not next_url:
                print 'The End.... ', next_url
                return
            else:
                # print test_get_offset(next_url)
                if '0' == test_get_offset(next_url):
                    return
                url_telnet_log.write('{}\n'.format(test_get_offset(next_url)))
                url_telnet_log.flush()
                url_questions.writelines(msg_write)
                url_questions.flush()
        else:
            print msg
            return



def test_get_offset(msg):
    return re.sub('.*&offset=', '', msg)


def start_create_topic_list():
    '''
    #   读取 dict_topic_types.txt
        生成对应目录文件，生成问题列表
    '''
    source_path = os.path.join(u'source', GLB_TYPE, 'step1')
    if not os.path.exists(source_path):
        os.makedirs(source_path)

    source_filename = u'dict_topic_types.txt'
    lines = open(os.path.join(source_path, source_filename), 'a+').readlines()
    for line in lines:
        line_arr = line.strip().split(' ')
        topic_id = re.sub('.*/', '', line_arr[0])
        url, title_name, offset = 'https://www.zhihu.com{}/newest'.format(line_arr[0]), line_arr[1], line_arr[2]

        # target_path = os.path.join(source_path, title_name)
        # if not os.path.exists(target_path):
        #     os.makedirs(target_path)

        print url, title_name, offset
        main_start_tops_finance(topic_id, title_name, offset)


# s2 下载
start_create_topic_list()
