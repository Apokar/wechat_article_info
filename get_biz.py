# -*- coding: utf-8 -*-
# @Time         : 2018/5/7 15:21
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : get_biz.py
# @Software     : PyCharm
# @PROJECT_NAME : wechat_article_info
import random
import re
import time

import requests
import urllib.request
import urllib3

urllib3.disable_warnings()


def get_biz():
    while True:
        try:
            proxy_list = list(urllib.request.urlopen(
                'http://60.205.92.109/api.do?name=3E30E00CFEDCD468E6862270F5E728AF&status=1&type=static').read().decode(
                "utf-8").split('\n'))
            print(proxy_list)

            index = random.randint(0, len(proxy_list) - 1)
            current_proxy = proxy_list[index]
            print("NEW PROXY:\t%s" % current_proxy)
            proxies = {"http": "http://" + current_proxy, "https": "http://" + current_proxy, }

            wechat_name = '人民日报'
            url = 'http://weixin.sogou.com/weixin?type=1&query=' + wechat_name + '&ie=utf8&s_from=input&_sug_=y&_sug_type_='

            headers = {
                'Host': ' mp.weixin.qq.com',
                'Referer': ' http://weixin.sogou.com/weixin?type=1&query=%E4%BA%BA%E6%B0%91%E6%97%A5%E6%8A%A5&ie=utf8&s_from=input&_sug_=y&_sug_type_=',
                'Upgrade-Insecure-Requests': ' 1',
                'User-Agent': ' Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            }

            content = requests.get(url, proxies=proxies)
            # print(content.text)
            if content.text.__contains__(
                    '<link rel="shortcut icon" href="//www.sogou.com/images/logo2014/new/favicon.ico" type="image/x-icon">'):
                print('换个proxy重试')

                continue
            else:
                detail_url = re.findall('href="http:(//mp.weixin.qq.com/profile\?src.*?==)"', content.text)[0].replace(
                    'amp;',
                    '')

                real_url = 'https:' + detail_url

                print(real_url)
                break
        except Exception as e:
            print(e)
            if str(e).find('HTTPSConnectionPool') >= 0:
                time.sleep(3)
                continue
            elif str(e).find('HTTPConnectionPool') >= 0:
                time.sleep(3)
                continue
            else:
                return None
                break

    req = requests.get(real_url)
    print(req.text)
    biz = re.findall('var biz = "(.*?)" \|\| "";', req.text)[0]
    print(biz)
    return biz

    # account = re.findall('var name=".*?"\|\|"(.*?)";', req.text)[0]
    # account_id= re.findall('var name="(.*?)"\|\|".*?";', req.text)[0]
    # head_url= re.findall('<img src="(.*?)">', req.text)[0]
    # qr_code=
    # verify=
    # summary=
    # TIMESTAMP=
    # datestamp=


if __name__ == '__main__':
    get_biz()
