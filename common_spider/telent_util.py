# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 
# @Author  : ErichLee ErichLee@qq.com
# @File    : telent_util.py
# @Comment : 
#            

import sys
import requests
import chardet
import brotli
import util.logger_util as logger
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

hd = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://www.zhihu.com/hot?list=sport',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    'cookie': 'q_c1=3cd59f3a0ab14c2f96533f82bec6be57|1504496132000|1504496132000; _zap=e341a08e-8090-4874-9320-f3e689743033; d_c0="AGDCon512gyPTnZNmOxLBc796eV8vLgijHs=|1513598963"; _ga=GA1.2.1986270710.1517902222; __DAYU_PP=BIZ3RuRybjAqUz2UFivrffffffffef01ac6cb022; _xsrf=D5T4yc66pxVUxqW14FQgvGSAg38V7it3; __gads=ID=6aedb8b1c666d1dd:T=1554716511:S=ALNI_MZ0Y_ExucCdSlne2L3UuzvbhXSs8g; q_c1=3cd59f3a0ab14c2f96533f82bec6be57|1562550202000|1504496132000; l_cap_id="ZDY3YzNkZDkwZGJiNGU3N2E5NjZhNWFkOGI5YTNhYWE=|1563421993|4eb1d3baf912b9c80241b60af77595101e304c50"; r_cap_id="ODI5Y2RkOTgyMjc1NDlmNWFjZGJjYmNlMWRiMjY1NzI=|1563421993|efc53932ef4d3703431376b8bbba4d2fb5ce3fcc"; cap_id="NzA5MGYyNjQxZjJlNGIwYjkzY2I2NDFkNWM4MWZiYTQ=|1563421993|082bc10e99110b150463acbbc1c3555103d89d11"; capsion_ticket="2|1:0|10:1563421995|14:capsion_ticket|44:MmRlZjExMjljZTk1NGEzNTk1MzAyMTk5YjE0OGI5Nzk=|09bcbb58cbfbffb167c919a165396a3308b08065d89847f49e43bc58da84bcff"; z_c0="2|1:0|10:1563421997|4:z_c0|92:Mi4xV0xJbUF3QUFBQUFBWU1LaWZuWGFEQ1lBQUFCZ0FsVk5MVHNkWGdCbGJtV1hPdHlGdzhha1F6ckVHRlluZDhGWnlB|70370189ebc3ef736599d4eab890ddcb186b1c60ba941584428d5a4359b9fc68"; __utmv=51854390.100-1|2=registration_date=20160617=1^3=entry_date=20160617=1; __utma=51854390.1986270710.1517902222.1563417975.1563428835.6; __utmz=51854390.1563428835.6.5.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; tst=h; tshl=film; anc_cap_id=06ef1c5c6a8d42e68ad47e403c682111; tgw_l7_route=116a747939468d99065d12a386ab1c5f'
}

hd_type2 = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://www.zhihu.com/explore',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'cookie':'q_c1=3cd59f3a0ab14c2f96533f82bec6be57|1504496132000|1504496132000; _zap=e341a08e-8090-4874-9320-f3e689743033; d_c0="AGDCon512gyPTnZNmOxLBc796eV8vLgijHs=|1513598963"; _ga=GA1.2.1986270710.1517902222; __DAYU_PP=BIZ3RuRybjAqUz2UFivrffffffffef01ac6cb022; _xsrf=D5T4yc66pxVUxqW14FQgvGSAg38V7it3; __gads=ID=6aedb8b1c666d1dd:T=1554716511:S=ALNI_MZ0Y_ExucCdSlne2L3UuzvbhXSs8g; q_c1=3cd59f3a0ab14c2f96533f82bec6be57|1562550202000|1504496132000; l_cap_id="ZDY3YzNkZDkwZGJiNGU3N2E5NjZhNWFkOGI5YTNhYWE=|1563421993|4eb1d3baf912b9c80241b60af77595101e304c50"; r_cap_id="ODI5Y2RkOTgyMjc1NDlmNWFjZGJjYmNlMWRiMjY1NzI=|1563421993|efc53932ef4d3703431376b8bbba4d2fb5ce3fcc"; cap_id="NzA5MGYyNjQxZjJlNGIwYjkzY2I2NDFkNWM4MWZiYTQ=|1563421993|082bc10e99110b150463acbbc1c3555103d89d11"; capsion_ticket="2|1:0|10:1563421995|14:capsion_ticket|44:MmRlZjExMjljZTk1NGEzNTk1MzAyMTk5YjE0OGI5Nzk=|09bcbb58cbfbffb167c919a165396a3308b08065d89847f49e43bc58da84bcff"; z_c0="2|1:0|10:1563421997|4:z_c0|92:Mi4xV0xJbUF3QUFBQUFBWU1LaWZuWGFEQ1lBQUFCZ0FsVk5MVHNkWGdCbGJtV1hPdHlGdzhha1F6ckVHRlluZDhGWnlB|70370189ebc3ef736599d4eab890ddcb186b1c60ba941584428d5a4359b9fc68"; __utmv=51854390.100-1|2=registration_date=20160617=1^3=entry_date=20160617=1; tshl=sport; __utmz=51854390.1564208883.14.10.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/account/https%3A%2F%2Fwww.zhihu.com%2Faccount%2Funhuman%3Ftype%3Dunhuman%26message%3D%25E7%25B3%25BB%25E7%25BB%259F%25E7%259B%2591%25E6%25B5%258B%25E5%2588%25B0%25E6%2582%25A8%25E7%259A%2584%25E7%25BD%2591%25E7%25BB%259C%25E7%258E%25AF%25E5%25A2%2583%25E5%25AD%2598%25E5%259C%25A8%25E5%25BC%2582%25E5%25B8%25B8%25EF%25BC%258C%25E4%25B8%25BA%25E4%25BF%259D%25E8%25AF%2581%25E6%2582%25A8%25E7%259A%2584%25E6%25AD%25A3%25E5%25B8%25B8%25E8%25AE%25BF%25E9%2597%25AE%25EF%25BC%258C%25E8%25AF%25B7%25E8%25BE%2593%25E5%2585%25A5%25E9%25AA%258C%25E8%25AF%2581%25E7%25A0%2581%25E8%25BF%259B%25E8%25A1%258C%25E9%25AA%258C%25E8%25AF%2581%25E3%2580%2582%26need_login%3Dfalse; tst=f; __utmc=51854390; anc_cap_id=a1b4fc6cb1d34bae85aef3dc43001864; __utma=51854390.1986270710.1517902222.1564454707.1564456927.17; tgw_l7_route=66cb16bc7f45da64562a077714739c11'

}


def telnet_post(url, params):
    try:
        req = requests.get(url, params=params,
                           headers=hd_type2)  # , headers=hd
        # rt.encoding = 'utf-8'
        key = 'Content-Encoding'
        if (key in req.headers and req.headers['Content-Encoding'] == 'br'):
            data = brotli.decompress(req.content)
            data1 = data.decode('utf-8')
            # print(data1)
            return data1

    except Exception as e:
        logger.errors('访问失败！{}'.format(e))


def telnet_question_ask(url):
    try:
        req = requests.get(url, headers=hd_type2)  # , headers=hd
        # rt.encoding = 'utf-8'
        key = 'Content-Encoding'
        if (key in req.headers and req.headers['Content-Encoding'] == 'br'):
            data = brotli.decompress(req.content)
            data1 = data.decode('utf-8')
            # print(data1)
            return data1

    except Exception as e:
        logger.errors('访问失败！{}'.format(e))


def telnet(url):
    try:
        req = requests.get(url, headers=hd_type2)  # , headers=hd
        # rt.encoding = 'utf-8'
        key = 'Content-Encoding'
        if (key in req.headers and req.headers['Content-Encoding'] == 'br'):
            data = brotli.decompress(req.content)
            data1 = data.decode('utf-8')
            print(data1)

        html = req.text
        # print rt_msg.decode('gbk').encode('utf-8')
        # print type(html)
        # print html
        # html_new =  html.encode('utf-8')
        # print type(html_new)
        #
        # print len(html_new)
        # print html_new

        print '======================='
        print '======================='
        print '======================='
        # return BeautifulSoup(rt.text, 'html5lib')
        # return rt.text
    except Exception as e:
        logger.errors('访问失败！{}'.format(e))


url = 'https://www.zhihu.com/commercial_api/banners_v3/question_up?question_token=334517175'
url = 'https://www.zhihu.com/explore'
url = 'https://www.zhihu.com/commercial_api/banners_v3/answer_up?question_token=333280072&answer_token=742959518'
url = 'https://www.zhihu.com/question/57321901/answers/updated'
url = 'https://www.zhihu.com/commercial_api/banners_v3/question_up?question_token=57321901'

url = 'https://www.zhihu.com/api/v4/search/preset_words?w='
url = 'https://www.zhihu.com/api/v4/search/top_search'

url = 'https://www.zhihu.com/search?type=content&q=%E6%9D%AD%E5%B7%9E%E5%A4%B1%E8%81%94%E5%A5%B3%E7%AB%A5'

url = 'https://www.zhihu.com/node/ExploreAnswerListV2?params=%7B%22offset%22%3A5%2C%22type%22%3A%22day%22%7D'
url = 'https://www.zhihu.com/api/v4/questions/333280072/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&offset=3&limit=5&sort_by=default&platform=desktop'

# url = 'https://www.zhihu.com/question/23509644'
# telnet(url)
