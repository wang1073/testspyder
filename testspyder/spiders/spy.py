
import os
import re
import json

import scrapy, time, hmac, base64
from urllib.parse import urlencode
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from hashlib import sha1
from scrapy import Selector
import execjs
from urllib import parse


class ZhihuSpider(scrapy.Spider):
    name = 'zhihut'
    allowed_domains = ['zhihu.com']
    start_url = 'https://www.zhihu.com/'
    rules = (Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),)

    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/signin',
        'User-Agent': agent
        # 'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
    }

    client_id='c3cef7c66a1843f8b3a9e6a1e3160e20'
    grant_type= 'password'
    source='com.zhihu.web'
    timestamp = str(int(time.time() * 1000))
    timestamp2 = str(time.time() * 1000)
    followee_ids = []
    ref_source = "homepage"
    captcha = ''



    # 处理签名
    def get_signnature(self,grant_type,client_id,source,timestamp):
        """
        通过 Hmac 算法计算签名
        固定字符串+时间戳
        """
        hm=hmac.new(b'd1b964811afb40118a12068ff74a12f4',None,sha1)
        hm.update(str.encode(grant_type))
        hm.update(str.encode(client_id))
        hm.update(str.encode(source))
        hm.update(str.encode(timestamp))
        return str(hm.hexdigest())

    def start_requests(self):
        yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',headers=self.headers,callback=self.start_login, meta={'cookiejar': 1},)  # meta={'cookiejar':1}

    def start_login(self,response):
        # 判断是否需要验证码
        need_cap=json.loads(response.body)['show_captcha']
        print(need_cap)
        if need_cap:
            print('需要验证码')
            yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',headers=self.headers,callback=self.capture,method='PUT', meta={'cookiejar': response.meta['cookiejar']})

        else:
            print('不需要验证码')
            post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
            post_data ={
                'client_id': self.client_id,
                'grant_type': self.grant_type,
                'timestamp': self.timestamp,
                'source': self.source,
                'signature': self.get_signnature(self.grant_type, self.client_id, self.source, self.timestamp),
                'username': '账号',
                'password': '密码',
                'captcha': '',
                # 改为'cn'是倒立汉字验证码
                'lang': 'en',
                'ref_source': 'other_',
                'utm_source': ''}
            yield scrapy.FormRequest(url=post_url, formdata=post_data, headers=self.headers, meta={'cookiejar': response.meta['cookiejar']},)

    def capture(self,response):

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
        self.captcha = input('请输入验证码：')

        #继续发起一个post请求，获取验证码识别的是否正确
        yield scrapy.FormRequest(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
                                 callback=self.parse_post_captcha,
                                 formdata={
                                     'input_text':str(self.captcha)
                                     }, meta={'cookiejar': response.meta['cookiejar']})


    def parse_post_captcha(self,response):
        '''
        解析验证码的post请求，获取验证码的识别结果，输入的验证码是错误还是正确。
        :param response:
        :return:
        '''
        result=json.loads(response.text).get("success",'')
        if result:
            print('验证码输入正确')
            #访问这个sign_in这个url进行登录
            login_param={
                'client_id': self.client_id,
                'grant_type': self.grant_type,
                'timestamp': self.timestamp,
                'source': self.source,
                'signature': self.get_signnature(self.grant_type, self.client_id, self.source, self.timestamp),
                'username':'18756967802',
                'password':'18756967802wang',
                'captcha': self.captcha,
                # 改为'cn'是倒立汉字验证码
                'lang': 'en',
                'ref_source': 'other_',
                'utm_source': '',
                }

            post_data = self.myencrypt(login_param)


    	    #此时，需要现在settings.py文件中添加scrapy允许处理的状态码(即添加HTTPERROR_ALLOWED_CODES=[400,600])，因为scrapy默认只处理[200,300]之间的状态码。
            yield scrapy.FormRequest(
                    url='https://www.zhihu.com/api/v3/oauth/sign_in',
                    formdata=post_data,
                    callback=self.after_login,
                    headers=self.headers,
                    meta={'cookiejar': response.meta['cookiejar']}
                )

    def myencrypt(self, data: dict):
        data = parse.urlencode(data)
        with open("Testjs2.js", "r", encoding='UTF-8') as f:
            js_code = f.read()
        ctx = execjs.compile(js_code)
        res = ctx.call("Myb", data)
        return res;



    def after_login(self, response):
        if response.status == 200:
            print("登录成功")

            return [scrapy.Request(
                self.start_url,
                headers=self.headers,
                meta={'cookiejar': response.meta['cookiejar']},
                callback=self.parse_people,
            )]
        else:
            print("登录失败")



    def parse_people(self, response):
        """
        解析用户主页
        """

        if "need_login=true" in response.url:
            with open('need_login.html', 'w', encoding="utf8") as f:
                f.write(response.text)
        selector = Selector(response)

        try:
            zhihu_id = os.path.split(response.url)[-1]
            userlinks = selector.xpath('//script[@id="js-initialData"]/text()').extract_first()
            userlinks = json.loads(userlinks)
            userlinks = userlinks['initialState']['entities']['users'][zhihu_id]
            nickname = userlinks['name']

            try:
                # 位置
                location = userlinks['locations'][0]['name']
            except (KeyError, IndexError) as e:
                # log.WARNING('未找到位置'+str(e))
                location = "未知"
            try:
                # 公司
                employment = userlinks['employments'][0]['company']['name']
                # # 职位
                position = userlinks['employments'][0]['job']['name']
            except (KeyError, IndexError) as e:
                employment = '未知'
                position = '未知'
            try:
                # 行业
                business = userlinks['business'][0]['name']
            except (KeyError, IndexError) as e:
                business = "未知"
            try:
                # 学校名字
                school_name = userlinks['educations'][0]['school']['name']
                log.logger.info(school_name)
                # 专业
                major = userlinks['educations'][0]['major']['name']
                # 1高中及以下，2大专，3本科， 4硕士，5博士及以上
                edu = userlinks['educations'][0]['diploma']
                if edu == 1:
                    education = '高中及以下'
                elif edu == 2:
                    education = '大专'
                elif edu == 3:
                    education = '本科'
                elif edu == 4:
                    education = '硕士'
                elif edu == 5:
                    education = '博士及以上'
                else:
                    education = '未知'
            except (KeyError, IndexError) as e:
                school_name = "未知"
                major = "未知"
                education = "未知"
            try:
                gender = userlinks['gender']
                gender = '男' if gender == 1 else '女'
            except IndexError as e:
                gender = '未知'
            image_url = selector.xpath(
                '//div[@class="UserAvatar ProfileHeader-avatar"]/img/@src'
            ).extract_first('')[0:-3]
            follow_urls = selector.xpath(
                '//div[@class="NumberBoard FollowshipCard-counts NumberBoard--divider"]/a/@href'
            ).extract()
            followee_count = userlinks['followingCount']
            follower_count = userlinks['followerCount']
            item = ZhihuPeopleItem(
                nickname=nickname,
                zhihu_id=zhihu_id,
                location=location,
                business=business,
                gender=gender,
                employment=employment,
                position=position,
                education=education,
                school_name=school_name,
                major=major,
                followee_count=followee_count,
                follower_count=follower_count,
                image_url=image_url + 'jpg',
            )
            yield item
        except Exception as e:
            log.logger.error('当前用户不存在' + str(e))
