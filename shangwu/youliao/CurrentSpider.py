import requests
from pyquery import PyQuery as pq
import re
import datetime

class CurrentSpider:
    # 食品商务网-食价搜油料
    market_name = "食品商务网-食价搜"
    url = "https://price.21food.cn/liangyou/youliao/"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75"
    }
    def get_Source(self, url):
        """发起请求 获得源码"""
        try:
            r = requests.post(url, headers=self.headers)
            r.encoding = 'utf8'
            html = r.text
        except:
            raise Exception("wrong")
        return html

    def getNumber(self, text):
        number = 0
        try:
            doc = pq(text)
            tds_number = doc("div.top_cent_erg font").items()
            for td in tds_number:
                number = td.text()[1:]
                span = re.search("\d*", number).span()
                number = int(number[span[0]:span[1]]) * 5 + 1
            return number
        except:
            raise Exception("wrong")

    def parse(self, text, time):
        doc = pq(text)
        food = []
        try:
            tds = doc("ul li table tr td").items()
            number = self.getNumber(text)
            i = 1
            j = 1
            for td in tds:
                if i == number:
                    break
                elif i % 5 == 0 :
                    j = 1
                    i += 1
                    continue
                elif j == 4 :
                    i += 1
                    j += 1
                    continue
                else:
                    food.append(td.text())
                    i += 1
                    j += 1
            for i in range(0,len(food),3):
                if food[i+2] == time:
                    print("name", food[i], "min", food[i+1], "max", food[i+1],
                          "avg", food[i+1], "reporting", time,"crawl",food[i+2],
                          "maket", self.market_name)
                else:
                    break
        except:
            raise Exception("wrong")

    def enterMethod(self):
        try:
            text = self.get_Source(self.url)
            today = datetime.datetime.now()
            re_date = today.strftime('%Y-%m-%d')
            self.parse(text, re_date)
        except:
            return False

c = CurrentSpider()
c.enterMethod()