
import os
import re
import json
from PIL import Image
import scrapy, time, hmac, base64
from urllib.parse import urlencode
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from hashlib import sha1
from scrapy import Selector
import execjs
from urllib import parse
import webbrowser


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_url = 'https://www.zhihu.com/'
    rules = (Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),)

    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36 Edg/83.0.478.45'
    headers = {
        'Connection': 'keep-alive',
        'Host': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com/signin',
        'User-Agent': agent
        # 'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
    }
    header1 = {
        'content-type': 'application/x-www-form-urlencoded',
        "x-zse-83": "3_2.0",
        'Referer': 'https://www.zhihu.com/signin',
        'User-Agent': agent,
        'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
    }
    login_headers = {
        'authority': 'www.zhihu.com',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.zhihu.com',
        'referer': 'https://www.zhihu.com/signin?next=%2F',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': agent,
        'x-ab-param': 'li_answer_card=0;pf_foltopic_usernum=50;li_topics_search=0;zr_expslotpaid=1;se_bsi=0;ug_goodcomment_0=1;li_se_section=1;qap_question_author=0;se_dnn_mt_v2=0;top_quality=0;li_answer_test_2=0;li_video_section=0;zw_sameq_sorce=999;zr_slot_training=1;top_test_4_liguangyi=1;qap_question_visitor= 0;zr_intervene=0;se_sug_term=0;pf_noti_entry_num=0;pf_profile2_tab=0;li_training_chapter=0;zr_search_paid=1;se_searchwiki=0;se_v2_highlight=1;li_svip_cardshow=1;li_salt_hot=1;zr_km_answer=open_cvr;se_v038=0;tsp_hotlist_ui=1;zr_training_first=false;se_page_quality=1;se_topic_wei=0;tp_meta_card=0;zr_ans_rec=gbrank;se_multi_images=0;se_entity22=0;pf_creator_card=1;se_click_v_v=0;se_zvideo_bert=1;tp_header_style=1;top_v_album=1;top_root=0;tsp_ios_cardredesign=0;li_viptab_name=0;li_paid_answer_exp=0;se_whitelist=0;se_cardrank_4=1;li_vip_verti_search=0;se_v040=0;tp_topic_style=0;ls_vessay_trans=0;soc_iosweeklynew=2;se_cardrank_2=1;se_clubrank=1;se_oneboxtopic=1;tp_dingyue_video=0;ls_videoad=2;zr_zr_search_sims=0;se_relation_1=2;se_aa_base=0;se_videobox=0;se_video_tab=0;tp_club_entrance=1;se_web0answer=0;se_new_bert=0;se_v043=0;tp_club_feedv3=0;se_content0=1;se_specialbutton=0;se_v039=0;se_mobilecard=0;tp_club_top=0;pf_newguide_vertical=0;li_catalog_card=1;zr_search_sim2=0;se_video_dnn=1;tp_club_flow_ai=0;pf_adjust=0;tp_discover=0;li_answer_test=3;zr_rec_answer_cp=open;se_club_boost=1;se_clarify=0;se_v040_2=0;se_v045=0;tp_club_feed=0;soc_adweeklynew=2;se_hotmore=2;tp_club_qa_entrance=0;qap_labeltype=1;tp_topic_tab_new=0-0-0;soc_notification=1;tsp_ad_cardredesign=0;pf_fuceng=1;ug_follow_topic_1=2;tp_topic_tab=0;zr_training_boost=false;se_topicfeed=0;se_college=default;se_cbert_index=1;tp_move_scorecard=0;ug_newtag=1;li_literature=0;se_adsrank=4;se_backsearch=0;top_ydyq=X;li_panswer_topic=0;zr_test_aa1=0;se_hotsearch=0;soc_feed_intelligent=0;top_universalebook=1;zr_slotpaidexp=1;se_relationship=1;se_multianswer=2;tp_movie_ux=0;ls_recommend_test=0;li_yxzl_new_style_a=1;zr_art_rec=base;zr_search_sims=0;se_searchvideo=3;se_cardrank_3=0;top_hotcommerce=1;ls_fmp4=0;li_car_meta=0;zr_rel_search=base;se_merger_v2=1;se_col_boost=0;se_colorfultab=1;se_ffzx_jushen1=0;tp_score_1=a;zr_search_topic=0;se_expired_ob=0;se_new_cbert=0;se_video_dnn_2=0;tp_m_intro_re_topic=1;top_ebook=0;li_svip_tab_search=1;se_hotsearch_2=1;se_billboardsearch=0;se_v044=0;tp_club__entrance2=0;tp_sft=a;tp_topic_entry=0;ls_video_commercial=0;li_ebook_gen_search=0;se_bert_eng=0;tp_club_reactionv2=0',
        'x-requested-with': 'fetch',
        'x-xsrftoken': 'MBpVnZn4055nSWDbdHJBYWsjiLuQynf3',
        'x-zse-83': '3_2.0'
        }


    client_id='c3cef7c66a1843f8b3a9e6a1e3160e20'
    grant_type= 'password'
    source='com.zhihu.web'
    timestamp = str(int(time.time() * 1000))
    timestamp2 = str(time.time() * 1000)
    followee_ids = []
    ref_source = "homepage"
    captcha = ''
    myusername=''
    mypassword=''

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
        self.myusername = input('请输入知乎账号：')
        self.mypassword = input('请输入知乎密码：')
        yield scrapy.Request('https://www.zhihu.com/api/v3/oauth/captcha?lang=en',headers=self.headers,callback=self.start_login, meta={'cookiejar': 1},)  # meta={'cookiejar':1}

    def start_login(self,response):
        # 判断是否需要验证码
        need_cap=json.loads(response.body)['show_captcha']
        print(need_cap)
        if need_cap:
            print('正在生成验证码')
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
                'username': self.myusername,
                'password': self.mypassword,
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
        
        fp = open('zhihu.gif','rb')
        img = Image.open(fp)
        img.show()
        self.captcha = input('请输入验证码：')

        #继续发起一个post请求，验证码识别是否正确
        yield scrapy.FormRequest(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en',
                                 callback=self.parse_post_captcha,
                                 formdata={
                                     'input_text':str(self.captcha)
                                     }, meta={'cookiejar': response.meta['cookiejar']})



    def parse_post_captcha(self,response):
        '''
        解析验证码的post请求，获取验证码的识别结果，输入的验证码是错误还是正确。
        '''
        result=json.loads(response.text).get("success",'')
        if result =='':
            print('验证码输入错误')
        if result:
            print('验证码输入正确')
            #访问这个sign_in这个url进行登录
            login_param={
                'client_id': self.client_id,
                'grant_type': self.grant_type,
                'source': self.source,
                'username':self.myusername,
                'password':self.mypassword,
                'lang': 'en',
                'ref_source': 'other_https://www.zhihu.com/signin',
                'utm_source': '',
                'captcha': '',
                'timestamp': self.timestamp,
                'signature': self.get_signnature(self.grant_type, self.client_id, self.source, self.timestamp)
                }
            data = parse.urlencode(login_param)
            str0 = open('str0.html','r',encoding="utf-8")
            str0read = str0.read()
            str1 = open('str1.html','r',encoding="utf-8")
            str1read = str1.read()
            encoderhtml = str0read+data+str1read
            with open('encodersave.html', 'wb') as f:
                f.write(encoderhtml.encode())
                f.close()
            webbrowser.open_new_tab('encodersave.html')

            post_data = input('请输入浏览器中的密钥：')
            yield scrapy.FormRequest(
                    url='https://www.zhihu.com/api/v3/oauth/sign_in',
                    formdata=post_data,
                    callback=self.request_homepage,
                    headers=self.login_headers,
                    meta={'cookiejar': response.meta['cookiejar']}
                )




    def request_homepage(self, response):

        yield scrapy.Request(
                url='https://www.zhihu.com',
                callback=self.check_login,
                headers=self.login_headers,
                meta={'cookiejar': response.meta['cookiejar']}
            )


    def check_login(self, response):
        if response.status == 200:
            print("登录成功")
            print(response.text)

        else:
            print("登录失败")



