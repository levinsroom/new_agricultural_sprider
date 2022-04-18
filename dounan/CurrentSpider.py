import requests
from pyquery import PyQuery as pq
import random
import datetime
import io

class CurrentSpider:
    #昆明市斗南花卉鲜花批发交易市场
    market_name = "昆明市斗南花卉鲜花批发交易市场"
    url = ["http://www.duood.com/GoodsList.aspx?id=1",
            "http://www.duood.com/GoodsList.aspx?id=2",
            "http://www.duood.com/GoodsList.aspx?id=3",
            "http://www.duood.com/GoodsList.aspx?id=4",
            "http://www.duood.com/GoodsList.aspx?id=5",
            "http://www.duood.com/GoodsList.aspx?id=6",
            "http://www.duood.com/GoodsList.aspx?id=7",
            "http://www.duood.com/GoodsList.aspx?id=8"]

    def get_page(self,url):
        """发起请求 获得源码"""
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0;) Gecko/20100101 Firefox/61.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/json',
            'method': 'GET',
            'Accept': 'application/vnd.github.cloak-preview'
        }

        headers['User-Agent'] = random.choice(user_agent_list)
        r = requests.get(url, headers=headers, verify=False)
        r.encoding = 'utf8'
        html = r.text
        return html

    def parse(self,text):
        doc = pq(text)
        reporting = datetime.datetime.now().strftime('%Y-%m-%d')
        # 获得每一行的tr标签
        tds = doc("table td").items()
        i = 0
        name = []
        Price = []
        for td in tds:
            data = td.text()
            if i == 0:
                name.append(data)
            elif 0<i<5:
                i += 1
                continue
            elif 5<=i<=7:
                Price.append(data)
            elif i == 9:
                i = 0
                continue
            i = i + 1
        for i in range(0, len(name)):
            j = i * 3
            print("name", name[i], "min", Price[j], "max", Price[j + 2],
                  "avg", Price[j + 1], "reporting", reporting,"crawl", reporting,
                  "maket", self.market_name)

    def enterMethod(self):
        try:
            today = datetime.datetime.now()
            # 玫瑰花、百合花、康乃馨、菊花、配花类、配叶类、斗南特殊进口、千花
            for url in self.url:
                text = c.get_page(url)
                c.parse(text)
        except:
            return False
        self.writeHlog(today)

c = CurrentSpider()
c.enterMethod()
