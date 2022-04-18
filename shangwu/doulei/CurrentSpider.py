import requests
from pyquery import PyQuery as pq
import re
import datetime
from new_agricultural.shangwu.Spider import CurrentSpider as spider

class CurrentSpider:
    # 食品商务网-食价搜豆类
    market_name = "食品商务网-食价搜"
    url = "https://price.21food.cn/liangyou/dou/"
    headers = {
        "User-Agent": "请复制自己浏览器"
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

    def parse(self, i, number, time):
        text = self.get_Source(self.url % (i))
        doc = pq(text)
        market_url = []
        try:
            for td in doc("title").items():
                if td.text() == "解除屏蔽":
                    print("被屏蔽2，解除ing")
                    from new_Agricultural.shangwu.solve.jiechu import Jiechu
                    if Jiechu().solve(self.url % (i)):
                        text = self.get_Source(self.url % (i))
                        doc = pq(text)
                    else:
                        Jiechu().solve(self.url % (i))
                        text = self.get_Source(self.url % (i))
                        doc = pq(text)
                else:
                    break
            tds = doc("ul li table tr td").items()
            i = 1
            j = 1
            for td in tds:
                if i == number:
                    break
                elif i % 5 == 0:
                    j = 1
                    i += 1
                    continue
                elif j == 4:
                    i += 1
                    j += 1
                    continue
                else:
                    if j == 1:
                        href = str(td.find("a").attr('href'))
                        a = "https://price.21food.cn" + href
                    if j == 3:
                        if td.text() == time:
                            market_url.append(a)
                        else:
                            return True
                    i += 1
                    j += 1
        except:
            raise Exception("wrong")
        spider.parse(market_url, time)
        return False

    def enterMethod(self):
        today = datetime.datetime.now()
        offset = datetime.timedelta(days=0)
        time = (today + offset).strftime('%Y-%m-%d')
        try:
            for i in self.page:
                number = self.page.get(i) * 5 + 1
                if c.parse(i, number, time):
                    break
                else:
                    time.sleep(10)
        except:
            return False


c = CurrentSpider()
c.enterMethod()
