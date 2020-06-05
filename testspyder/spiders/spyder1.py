
import scrapy

class mingyan(scrapy.Spider):
    name = "color" # 定义蜘蛛名
    def start_requests(self): # 由此方法通过下面链接爬取页面
        # 定义爬取的链接
        urls = [
            'https://www.qtccolor.com/Color/C-56229.aspx',
        ]
        for num in range(1,110):
            strpath='https://www.qtccolor.com/Color/C-56'+str(229+num)+'.aspx'
            urls.append(strpath)


        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) #爬取到的页面如何处理？提交给parse方法处理

    def parse(self, response):

        rgb=response.xpath('//td//span[@class="cmyk"]/text()')
        strname=response.xpath('//div[@class="ColorCode"]/text()')

        filename = 'skin_rgb.txt'
        with open(filename, 'a+') as f:
            f.write(rgb[0].root+' ')
            f.write(rgb[1].root+' ')
            f.write(rgb[2].root+' ')
            f.write(strname[0].root+'\n')
            f.close()
        self.log('保存文件: %s' % filename)
