# -*- coding: utf-8 -*-
# @Time    : 2018/1/31 
# @Author  : LIYUAN134
# @File    : my_email.py
# @Comment:
#
from email.header import Header
from email.mime.text import MIMEText

from email.utils import parseaddr, formataddr

import smtplib
import util.date_check_util as date_util


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_msg(msg):
    from_addr = '18751845189@163.com'
    from_password = ''

    to_addr = 'newbaiha@163.com'
    smtp_server = 'smtp.163.com'
    message = u'勤劳的小蜜蜂 请注意 \n' + str(msg)
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'py管理员<%s>' % from_addr)
    msg['To'] = _format_addr(u'小蜜蜂<%s>' % to_addr)
    msg['Subject'] = Header(u'邮件提醒')

    server = smtplib.SMTP(smtp_server, 25)
    server.login(from_addr, from_password)
    server.sendmail(from_addr, [to_addr], msg.as_string())

    server.quit()


def little_msg():
    sys_time = date_util.curr_ymd_hms()
    send_msg(u"大兄弟，自己动手，丰衣足食{}".format(sys_time))


