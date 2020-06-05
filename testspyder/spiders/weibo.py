
# -*- coding: utf-8 -*-
import scrapy
import json

class WeiSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    # start_urls = ['http://weibo.cn/']
    # 当引擎把start_urls中的内容放入调度器中以后，会调取下载器发起get请求，现在如果需发送post请求，就需要把start_urls注视掉

    # def parse(self, response):
    #     pass
    # 重写一个方法
    def start_requests(self):
        # 这个方法当下载器开始发起请求之前被调用
        # 在这个方法我们可以把下载器截获，改变其原来的请求方式
        login_url = "https://passport.weibo.cn/sso/login" # post请求的接口url
        # post提交的数据
        data = {
            'username': '18756967802',
            'password': '1771938113wang',
            'savestate': '1',
            'r': 'https://weibo.cn/?luicode=20000174',
            'ec': '0',
            'pagerefer': 'https://weibo.cn/pub/?vt=',
            'entry': 'mweibo',
            'wentry': '',
            'loginfrom': '',
            'client_id': '',
            'code': '',
            'qq': '',
            'mainpageflag': '1',
            'hff': '',
            'hfp': ''
        }

        yield scrapy.FormRequest(url=login_url,formdata=data,callback=self.parse_login)

    def parse_login(self, response):

        # print(response.text)
        # 判断登录是否成功
        if json.loads(response.text)["retcode"] == 20000000:
            print("登录成功！")
            # 访问主页
            main_url = "https://weibo.cn/?since_id=0&max_id=H0moBsJrC&prev_page=1&page=1"
            yield scrapy.Request(url=main_url,callback=self.parse_info)

        else:
            print("登录失败！")

    def parse_info(self, response):
        print(response.text)
