import requests
from pyquery import PyQuery as pq
import re
import datetime
import io

class CurrentSpider:
    #元谋县蔬菜交易市场有限责任公司
    market_name = "元谋县蔬菜交易市场有限责任公司"
    url = "http://www.vipveg.com/market/179/y%sm%sd%sp%s.html"
    url1 = "http://www.vipveg.com/market/179/y%sm%sd%s"

    def get_Source(self, url):
        """发起请求 获得源码"""
        try:
            '''设置header，ip，多个代理ip访问防止拒绝连接'''
            r = requests.get(url)
            r.encoding = 'utf8'
            html = r.text
            if len(html) == 1128:
                return "404"
            elif True:
                title = pq(html)("title")
                for t in title:
                    if t.text == "很抱歉，您访问的页面不存在 - VIP蔬菜网":
                        return "404"
            else:
                return html
        except:
            raise Exception("wrong")
        return html

    def parse(self, text):
        doc = pq(text)
        reporting = datetime.datetime.now()
        tds = doc("div table.m_t_8 tr td.p_l_10 table.m_t_8 tr td table td").items()
        i = 1
        j = 0
        Price = []
        name = []
        for td in tds:
            data = td.text().split(" ")[0].split("\n")
            if 1 <= i <= 8:
                i = i + 1
                continue
            else:
                if 0 <= j < 4:
                    if j > 0:
                        price = data[0][1:len(data[0])]
                        Price.append(price)
                    else:
                        name.append(data[0])
                    j += 1
                else:
                    j = 0
        for i in range(0, len(name)):
            j = i * 3
            print("name", name[i], "min", Price[j], "max", Price[j + 1],
                  "avg", Price[j + 2], "reporting", reporting, "maket", self.market_name)

    def Page(self, text):
        doc = pq(text)
        tds = doc("div.m_b_10 span b").items()
        for td in tds:
            return td.text()

    def readHlog(self):
        postion = "D:\\机器学习\\Agricultural\\hlog\\tonghai\\hlog.txt"
        try:
            file = io.open(postion, "r", encoding='utf8')
            file.seek(0)
            with file as f:
                lines = f.readlines()
            x = lines[len(lines) - 1].strip().split(",")
            return x[len(x) - 2]
        except FileNotFoundError:
            raise Exception("FileNotFoundError")
        except LookupError:
            raise Exception("LookupError")
        except UnicodeDecodeError:
            raise Exception("UnicodeDecodeError")
        except:
            raise Exception("wrong")
        finally:
            if file:
                file.close()

    def writeHlog(self, crawl_time):
        postion = "D:\\机器学习\\Agricultural\\hlog\\tonghai\\hlog.txt"
        try:
            file = open(postion, 'a+', encoding='utf8')
            weekday = crawl_time.weekday()
            crawl_time = crawl_time.strftime('%Y-%m-%d')
            with file as f:
                if weekday == 6:
                    f.write("," + crawl_time + ",1" + "\n")
                else:
                    if weekday == 0:
                        f.write(crawl_time + ",1")
                    else:
                        f.write("," + crawl_time + ",1")
        except FileNotFoundError:
            raise Exception("FileNotFoundError")
        except LookupError:
            raise Exception("LookupError")
        except UnicodeDecodeError:
            raise Exception("UnicodeDecodeError")
        except:
            raise Exception("wrong")
        finally:
            if file:
                file.close()

    def enterMethod(self):
        try:
            time = self.readHlog()
            i = 0
            text = "404"
            today = datetime.datetime.now()
            while (text == "404"):
                i += 1
                offset = datetime.timedelta(days=+i)
                value = datetime.datetime.strptime(time, '%Y-%m-%d')
                re_date = (value + offset)
                craw_time = re_date.strftime('%Y-%m-%d')
                if craw_time == today.strftime('%Y-%m-%d'):
                    return False
                else:
                    x = re.findall('\d+', craw_time)
                    text = self.get_Source(self.url % (x[0], x[1], x[2], 1))
            else:
                self.writeHlog(re_date)
                url = self.url1 % (x[0], x[1], x[2]) + "p%s.html"
                page = c.Page(text)
                for i in range(1, int(page) + 1):
                    print(url % (str(i)))
                    text = self.get_Source(url % (str(i)))
                    self.parse(text)
                return True
        except:
            return False

c = CurrentSpider()
c.enterMethod()