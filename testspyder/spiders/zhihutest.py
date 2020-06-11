
import json
#import re
import base64
import scrapy
import time
#from urllib import parse  hashlib
import hmac
import hashlib

class ZhihuLoginSpider(scrapy.Spider):
    name = 'zhihutest'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    ##声明相应字段
    client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    grant_type = 'password'
    timestamp = str(round(time.time() * 1000))
    source = 'com.zhihu.web'
    captcha = ""
    lang = 'en'
    ref_source = "homepage"
    utm_source = ""
    #注意header 要加authorization
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
        "authorization": f"oauth {client_id}"
    }
   #获得相应的signature
    def get_signature(self):
        hm = hmac.new(b'd1b964811afb40118a12068ff74a12f4', None, hashlib.sha1)
        hm.update(self.grant_type.encode())
        hm.update(self.client_id.encode())
        hm.update(self.source.encode())
        hm.update(self.timestamp.encode())
        return hm.hexdigest()

    def parse(self, response):
        pass

    #重写start_requests方法，要它先get https://www.zhihu.com/api/v3/oauth/captcha?lang=en 拿到 capsion_ticket 的cookie，不然没有这个cookie无法登陆
    def start_requests(self):

#        return [scrapy.Request(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en', callback=self.call_data,headers=self.header)]
        yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',headers=self.header,callback=self.call_captcha, meta={'cookiejar': 1},)  # meta={'cookiejar':1}



    def call_captcha(self, response):
        # 判断是否需要验证码
        need_cap=json.loads(response.body)['show_captcha']
        print(need_cap)
        if need_cap:
            print('需要验证码')
            yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',headers=self.header,callback=self.call_data,method='PUT', meta={'cookiejar': response.meta['cookiejar']})

        else:
            print('不需要验证码')

   ##正式模拟登陆，post相应字段
    def call_data(self, response):
        try:
            img = json.loads(response.body)['img_base64']
        except ValueError:
            print('获取img_base64值失败！')
        else:
            img = img.encode('utf8')
            img_data = base64.b64decode(img)

            with open('zhihu.gif', 'wb') as f:
                f.write(img_data)
                f.close()
        captcha = input('请输入验证码：')

        post_data = {
            'client_id': self.client_id,
            'grant_type': self.grant_type,
            'timestamp': self.timestamp,
            'source': self.source,
            'captcha': self.captcha,
            'signature': self.get_signature(),
            'username': '18756967802',
            'password': '18756967802wang',
            'lang': self.lang,
            'ref_source': self.ref_source,
            'utm_source': self.utm_source
        }

        return scrapy.FormRequest(url='https://www.zhihu.com/api/v3/oauth/sign_in', formdata=post_data,
                                  headers=self.header, callback=self.login_callback)
   #登陆成功后直接访问知乎首页，登陆状态下有相应数据返回
    def login_callback(self, response):
        return Request(url='http://www.zhihu.com', headers=self.header, callback=self.login_callback1)
  #数据返回在这的response
    def login_callback1(self, response):
        pass
