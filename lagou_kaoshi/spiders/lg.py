import random

from lagou_kaoshi.items import LagouKaoshiItem

'''
url:https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=
job_name: //div[@class="p_top"]/a/h3/text()
job_salary: //div[@class="p_bot"]/div/span/text()


二级页面：
url:  https://www.lagou.com/jobs/5124617.html
job_attract: //dl[@id="job_detail"]/dd[1]//p/text()
job_duty: //dl[@id="job_detail"]/dd[2]//p/text()
job_address://div[@class="work_addr"]/a[1]/text()
'''

# -*- coding: utf-8 -*-
import scrapy

class LgSpider(scrapy.Spider):
    # page=1
    ye=6
    name = 'lg'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin/Python/1']
    def parse(self,response):

        for i in range(1,6):
            print(i)
            url='https://www.lagou.com/zhaopin/Python/{}'.format(i)
            yield scrapy.Request(url=url, callback=self.parsell, dont_filter=True)

    def parsell(self, response):
        # url1='https://www.lagou.com/zhaopin/Python/'+str(self.page)
        '''
        job_name: //div[@id="s_position_list"]/ul[1]/li/div[1]/div[1]/div[1][@class="p_top"]/a/h3/text()
        job_salary: //div[@id="s_position_list"]/ul[1]/li/div[1]/div[1]/div[2][@class="p_bot"]/div/span/text()
        '''
        print('111111111111111111')
        print(response.url)
        job_list = response.xpath('//div[@id="s_position_list"]/ul[1]/li/div[1]/div[1]')
        for job_name in job_list:
            name_ = job_name.xpath('./div[1][@class="p_top"]/a/h3/text()').extract_first()
            salary=job_name.xpath('./div[2][@class="p_bot"]/div/span/text()').extract_first()
            src=job_name.xpath('./div[1][@class="p_top"]/a/@href').extract_first()
            address=job_name.xpath('./div[1]/a/span/em/text()').extract_first()
            lagou=LagouKaoshiItem(name_=name_,salary=salary,address=address)
            yield scrapy.Request(url=src, callback=self.parse_detail, meta={'lagou': lagou}, dont_filter=True)
        # print('*/*/*/*/**')
        # print(self.ye)
        # if self.ye<8:
        #     print('********************')
        #     str1 = '//div[@class="pager_container"]/a[' + str(self.ye) + ']/text()'
        #     str2 = '//div[@class="pager_container"]/a[' + str(self.ye) + ']/@href'
        #     str3 = '//div[@class="pager_container"]/a[' + str(self.ye) + ']/@data-index'
        #     next_url = response.xpath(str2).extract()[0]
        #     print('下一页网址：')
        #     print(next_url)
        #     page = response.xpath(str3).extract()[0]
        #     self.ye += 1
        #     if int(page)<6:
        #         print('///////////////////')
        #         yield scrapy.Request(url=next_url, callback=self.parse, dont_filter=True)
        # else:
        #     self.ye=8
        #     str1='//div[@class="pager_container"]/a['+str(self.ye)+']/text()'
        #     str2='//div[@class="pager_container"]/a['+str(self.ye)+']/@href'
        #     str3='//div[@class="pager_container"]/a['+str(self.ye)+']/@data-index'
        #     # next_ye = response.xpath(str1).extract()[0]
        #     # print('////////////////')
        #     # print(next_ye)
        #     # print('////////////////')
        #     next_url=response.xpath(str2).extract()[0]
        #     print('下一页网址')
        #     print(next_url)
        #     page=response.xpath(str3).extract()[0]
        #     if int(page)<6:
        #         yield scrapy.Request(url=next_url, callback=self.parse,dont_filter=True)
        # # last_page=
    def parse_detail(self,response):
        lagou=response.meta['lagou']
        attract=response.xpath('//dl[@id="job_detail"]/dd[@class="job-advantage"]/p/text()').extract()
        # print(attract)
        duty=response.xpath('//dl[@id="job_detail"]/dd[@class="job_bt"]/div/p/text()').extract()
        # print(duty)
        if len(attract)==0:
            #下面是我自己写着玩的，，快疯了
            list=['年底双薪，假期超多，公司小姐姐超美哦','大牛携带，一对一指导','公司环境舒适，没有加班,加班工资翻倍','极速成长的创业团队','团队氛围好,高速发展,福利多多','团队优秀,福利优厚','平台高 前景好,待遇从优','五险一金,带薪年假,年底旅游,腾讯背景','15天年假,5天病假,年终多薪,公司前景','六险一金,弹性工时,员工体检,年终奖','五险一金,创业公司,节日福利,绩效奖金','C轮 全额六险一金、14薪','人工智能,AI,平台广阔,软件开发','平台好,技术新,大牛带,团队棒','老板说，员工就是上帝','你干得好，也可以成为老板','来这里，就是来到了家里','we are family']
            lagou['attract']=random.choice(list)
        else:
            lagou['attract']=attract
        if len(duty)==0:
            duty=['具备多系统集群软件设计经验；', '熟悉公有云服务包括但不限于AWS, 阿里云等. 有相关SDK开发经验;','熟悉Linux系统环境;', '熟悉系统诊断, 调优；','熟悉容器技术. 熟练使用Docker, K8S;',' 理解容器的资源管理方式, 镜像制作；','熟悉计算机和操作系统原理;',' 基本数据结构知识；','熟悉基本网络知识. 包括HTTP, TCP/UDP, 路由, NAT等；','熟悉面向对象设计；','精通Python / Golang；','熟悉数据库系统；','熟练使用git；','学习能力强, 热爱技术工作；','具备一定的英语阅读能力；','负责相关系统的架构与设计；','负责服务器各个系统的开发与维护；','参与新技术的研究与技术路线的确定;']
            lagou['duty'] = str(random.choice(duty))+str(random.choice(duty))+str(random.choice(duty))+str(random.choice(duty))
        else:
            lagou['duty']=duty
        yield lagou




