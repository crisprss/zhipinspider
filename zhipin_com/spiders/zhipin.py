import scrapy
import requests
import time
from zhipin_com.items import ZhipinComItem

class ZhipinSpider(scrapy.Spider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['http://zhipin.com/']

    position_url = "https://www.zhipin.com/c101010100/?query=安全工程师"
    cur_page = 1


    headers = {
    ":authority": "www.zhipin.com",
    ":method": "GET",
    ":scheme": "https",
    "accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3",
    "accept - encoding": "gzip, deflate, br",
    "accept - language": "zh - CN, zh;q = 0.9, en;q = 0.8",
    "cache - control": "max - age = 0",
    "cookie":"__zp__pub__=; __zp__pub__=; __c=1595734714; __g=-; _uab_collina=159573471448300453162647; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1595734715; __l=l=%2Fwww.zhipin.com%2F&r=&friend_source=0&friend_source=0; lastCity=100010000; __a=66711608.1595734714..1595734714.40.1.40.40; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1595746456; __zp_stoken__=2321aWCNOfw1VM2seCCIaezcMEDdaTnljWn9rQVUpcHA8Y1cfZTEgYRA%2FR0xSbiIhTztCQCUlbwkTcDomGgc2M3YPflYHNwc8B2xwWDJzY25iXHEoSQNDcz8XCyVnVVxqDQIHPyBEEANRND4%3D",
    "sec - fetch - mode": "navigate",
    "sec - fetch - site": "same - origin",
    "sec - fetch - user": "?1",
    "upgrade - insecure - requests": 1,
    "user - agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }

    def start_requests(self):
        return [self.next_request()]


    def parse(self, response):
        print("request ->"+response.url)
        job_list = response.css("div.job-list > ul > li")
        for job in job_list:
            item = ZhipinComItem()
            job_primary = job.css("div.job-primary")
            item['pid'] = job_primary.css("div.info-primary .job-name a::attr(data-jobid)").extract_first().strip()
            item['jobname'] = job_primary.css("div.info-primary .job-name a::text").extract_first().strip()
            item['salary'] = job_primary.css("div.info-primary .job-limit.clearfix>span::text").extract_first().strip()
            company_info = job_primary.css("div.info-primary .info-company .company-text>p::text").extract()
            if(len(company_info) == 3):
                item['company_industry'] = company_info[0].strip()
                item['company_size'] = company_info[2].strip()
            item['company_name'] = job_primary.css("div.info-primary .info-company .company-text>h3>a::text").extract_first().strip()
            info_primary = job_primary.css("div.info-primary .job-limit.clearfix>p::text").extract()
            item['workyear'] = info_primary[0].strip()
            item['education_need'] = info_primary[1].strip()
            yield item
        self.cur_page += 1
        time.sleep(10)
        yield self.next_request()
    def next_request(self):
        return scrapy.http.FormRequest(self.position_url+"&page={}&ka=page-{}".format(self.cur_page,self.cur_page),headers=self.headers,callback=self.parse)
        pass
