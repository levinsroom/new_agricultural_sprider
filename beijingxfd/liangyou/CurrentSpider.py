import requests
from pyquery import PyQuery as pq
import datetime
import time

class CurrentSpider:
    #北京新发地菜市场(粮油)
    market_name = "北京新发地菜市场"
    url = "http://www.xinfadi.com.cn/marketanalysis/5/list/%s.shtml"

    def get_Source(self, url):
        """发起请求 获得源码"""
        try:
            '''设置header，ip，多个代理ip访问防止拒绝连接'''
            r = requests.get(url)
            r.encoding = 'utf8'
            html = r.text
        except:
            raise Exception("wrong")
        return html

    def parse(self, text):
        try:
            doc = pq(text)
            reporting = datetime.datetime.now().strftime('%Y-%m-%d')
            offset = datetime.timedelta(days=-2)
            re_date = (datetime.datetime.now() + offset).strftime('%Y-%m-%d')
            tds = doc("table.hq_table tr").items()
            i = 0
            for td in tds:
                crawl = td.find('td:nth-child(7)').text()
                if i == 0:
                    i += 1
                    continue
                elif crawl != re_date:
                    return True
                else:
                    name = td.find('td:first-child').text()
                    min = td.find('td:nth-child(2)').text()
                    avg = td.find('td:nth-child(3)').text()
                    max = td.find('td:nth-child(4)').text()
                    print("name", name, "min", min, "max", max,
                          "avg", avg, "reporting", reporting, "crawl", crawl,
                          "maket", self.market_name)
        except:
            raise Exception("wrong")
        return False

    def enterMethod(self):
        try:
           for i in range(1,10):
               text = self.get_Source(self.url % (str(i)))
               if self.parse(text):
                   return True
               else:
                   time.sleep(10)
        except:
            return False
        return True

c = CurrentSpider()
c.enterMethod()