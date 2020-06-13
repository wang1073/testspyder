
import scrapy
import json

class WeiSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    # start_urls = ['http://weibo.cn/']
    # start_urls放入调度器后，会调取下载器发起get请求，现在需发送post请求，要把start_url注释
    myusername=''
    mypassword=''

    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        # 'Host': 'passport.weibo.cn', # 这个主机名必须注释掉，当请求头中主机名指定为某个值的时候，后面每一次发起请求都会把url的主机名重定向该主机名下面
        'Origin': 'https://passport.weibo.cn',
        'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F%3Fluicode%3D20000174&backTitle=%CE%A2%B2%A9&vt='
    }


    def start_requests(self):
        login_url = "https://passport.weibo.cn/sso/login" # post请求的接口url
        
        self.myusername = input('请输入微博账号：')
        self.mypassword = input('请输入微博密码：')
        # post提交的数据
        data = {
            'username': self.myusername,
            'password': self.mypassword,
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

        yield scrapy.FormRequest(url=login_url,formdata=data,headers=self.headers,callback=self.parse_login)

    def parse_login(self, response):

        if json.loads(response.text)["retcode"] == 20000000:
            print("登录成功！")
            # 访问主页
            main_url = "https://weibo.cn/?since_id=0&max_id=H0moBsJrC&prev_page=1&page=1"
            yield scrapy.Request(url=main_url,callback=self.parse_info)

        else:
            print("登录失败！")

    def parse_info(self, response):
        print(response.text)
