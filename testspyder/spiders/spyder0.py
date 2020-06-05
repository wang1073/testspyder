
import scrapy

class weibohotrank(scrapy.Spider):
    name = "weibohot" # 定义蜘蛛名
    def start_requests(self): # 由此方法通过下面链接爬取页面
        # 定义爬取的链接
        urls = [
            'https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) #爬取到的页面如何处理？提交给parse方法处理

    def parse(self, response):

        '''
        start_requests已经爬取到页面，那如何提取我们想要的内容呢？那就可以在这个方法里面定义。
        这里的话，并木有定义，只是简单的把页面做了一个保存，并没有涉及提取我们想要的数据，后面会慢慢说到
        也就是用xpath、正则、或是css进行相应提取，这个例子就是让你看看scrapy运行的流程：
        1、定义链接；
        2、通过链接爬取（下载）页面；.xpath("@href")
        3、定义规则，然后提取数据；.css('td-02')
        就是这么个流程，似不似很简单呀？
        '''

        affair=response.xpath('//td[@class="td-02"]/a/text()')
        rank=response.xpath('//td[@class="td-01 ranktop"]/text()')
        view=response.xpath('//td[@class="td-02"]/span/text()')

        top=affair[0]
        affair=affair[1:]
        print(len(affair))
        print(top.root)
        topstr=top.root
        filename = 'weibohot.txt'
        with open(filename, 'w') as f:
            f.write(top.root+'\n')
            for classnum in range(len(affair)):
                f.write(rank[classnum].root+' ')
                f.write(affair[classnum].root+' ')
                f.write(view[classnum].root+'\n')
            f.close()
        self.log('保存文件: %s' % filename)