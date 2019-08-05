# -*- coding: utf-8 -*-
# @Time    : 2019/7/12
# @Author  : ErichLee ErichLee@qq.com
# @File    : hot_list.py
# @Comment :
#

import json
# import math
import math
import os
import re
import sys

from bs4 import BeautifulSoup

import common_spider.telent_util as telnet_util
import util.file_check_util as file_util
import tool.email_util as email_util
from sys_gl import *
import socket

reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 20
socket.setdefaulttimeout(timeout)
url_query_question_answers = 'https://www.zhihu.com/api/v4/questions/{question_id}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={offset}&platform=desktop&sort_by=default'

flag_counter = 0


def find_answers(question_id, url, question_content, output_root):
    # ASK ANSWER
    # 具体问题
    # question_id = 333784019
    # url = 'https://www.zhihu.com/question/333280072'
    # url = 'https://www.zhihu.com/question/333784019'
    msg_question = telnet_util.telnet_question_ask(url)
    # print msg_question
    # find total_answers
    soup = BeautifulSoup(msg_question, 'html5lib')
    if not soup:
        return
    file_answers = open(u'{}/{}.txt'.format(output_root, question_id), 'w')
    try:
        tag_span = soup.select_one('div.Card.AnswersNavWrapper span')
        if not tag_span:
            global flag_counter
            if flag_counter > 10:
                # 发送邮件
                email_util.little_msg()
                print input("手动验证码:")
                flag_counter = 0
            else:
                flag_counter += 1
                print 'ERROR , not found', url
                return

        msg_total = tag_span.text
        page_total = int(re.sub('[^0-9]', '', msg_total))

        counter = 1
        print question_content

        file_answers.write('QUESTION:{}\n'.format(question_content))
        page_limit = 5
        page_size = int(math.ceil(1.0 * page_total / page_limit))
        for page_index in range(0, page_size):
            page_offset = page_index * page_limit
            print page_total, page_offset

            # page_offset = 5
            url = url_query_question_answers.format(question_id=question_id, offset=page_offset)
            msg_answers = telnet_util.telnet_question_ask(url)
            # print msg_question
            rt_list = parse_get_answers(msg_answers)
            for answer_info, answers_content in rt_list:
                # print answer_info, answers_content
                file_answers.write('ANSWERS_INFO_{:0>4d}\t{}\n'.format(counter, answer_info))
                file_answers.write('ANSWERS_CONT_{:0>4d}:\n{}\n'.format(counter, answers_content))

                counter += 1
    except Exception as e:
        print e
    finally:
        if file_answers:
            file_answers.close()


def parse_get_answers(line):
    # lines = open('source/d1.txt', 'a+')
    # for line in lines:
    js = json.loads(line)

    rt_list = []
    if 'data' in js:
        data = js['data']
        for each in data:
            content = each['content']
            soup = BeautifulSoup(content, 'html5lib')
            p_list = soup.select('p')
            if p_list:
                p_msg = [p.text for p in p_list]
            else:
                p_msg = [soup.text]

            answers_info = '{}\t{}\t{}\t{}\t{}'.format(each['id'], each['author'].get('name'),
                                                       each['author'].get('url_token'),
                                                       each['created_time'], each['updated_time'])
            answers_content = "\n".join(p_msg)

            rt_list.append((answers_info, answers_content))

    return rt_list


def start_download():
    source_path = u'source/download'

    url_list = []
    questions = open(u'source/download/url_questions.txt').readlines()
    for question in questions:
        qt_qrr = question.split('\t')
        url = qt_qrr[3]
        url_list.append(url)
    url_list_new = list(set(url_list))
    for url_telnet in url_list_new:
        print 'telnet', url_telnet
        question_id = re.sub('.*/', '', url_telnet).strip()
        find_answers(question_id, url_telnet)


def start_download2():
    # source_path = u'source_finance_simple/{}'.format(GLB_BATCH)
    # output_source = u'source_finance_download/{}'.format(GLB_BATCH)
    source_path = os.path.join(u'source', GLB_TYPE, 'step2', GLB_BATCH)
    output_source = os.path.join(u'source', GLB_TYPE, 'step3', GLB_BATCH)

    file_list = file_util.get_all_files_path_name_endswith(source_path, '.txt')
    for file_name, file_path, file_root in file_list:
        print file_name, file_path, file_root
        output_root = file_root.replace(source_path, output_source)
        if not os.path.exists(output_root):
            os.makedirs(output_root)

        questions = open(file_path, 'r').readlines()

        for question in questions:
            try:
                qt_arr = question.strip().split('\t')
                question_id, url_telnet, question_content = qt_arr[0].replace('QUESTION ', ''), qt_arr[3], qt_arr[4]
                find_answers(question_id, url_telnet, question_content, output_root)
            except Exception as e:
                print e
                continue


def url_test():
    questions = open(u'source/finance/url_telnet_log.log').readlines()
    # print len(questions)
    for q in questions:
        print re.sub('.*offset=', '', q.strip())


start_download2()
