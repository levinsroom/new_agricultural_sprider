import requests
from pyquery import PyQuery as pq
import re
import datetime
import io

market_url = url = "http://www.vipveg.com/market/%s"


def get_Source(url):
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

def parse(text,Name,craw_time):
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
              "avg", Price[j + 2], "reporting", reporting,"cral",craw_time, "maket", Name)

def Page(text):
    doc = pq(text)
    tds = doc("div.m_b_10 span b").items()
    for td in tds:
        return td.text()

def readHlog(market_id):
    postion = "D:\\机器学习\\new_agricultural\\hlog\\%s.txt"%str(market_id)
    try:
        file = io.open(postion, "r", encoding='utf8')
        file.seek(0)
        with file as f:
            lines = f.readlines()
        x = lines[len(lines) - 1].strip().split(",")
        return x[len(x)-1]
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

def writeHlog(market_id,crawl_time,time):
    postion = "D:\\机器学习\\new_agricultural\\hlog\\%s.txt" % str(market_id)
    try:
        time = datetime.datetime.strptime(time, '%Y-%m-%d')
        file = open(postion, 'a+', encoding='utf8')
        weekday = crawl_time.weekday()
        crawl_time = crawl_time.strftime('%Y-%m-%d')
        with file as f:
            if weekday == 0:
                f.write("\n"+crawl_time)
            else:
                if time.weekday() == 0:
                    f.write("," + crawl_time)
                elif time.weekday() >= weekday:
                    f.write("\n" + crawl_time)
                else:
                    f.write(","+crawl_time)
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

def enterMethod(market_id):
    Market_url = market_url%str(market_id)
    url = Market_url + "/y%sm%sd%sp%s.html"
    url1 = Market_url + "/y%sm%sd%s"
    Market_name = Market_url+".html"
    r = requests.get(Market_name)
    r.encoding = 'utf8'
    tds = pq(r.text)("div.t_a_c h1").items()
    for td in tds:
        name = td.text()
        break
    try:
        time = readHlog(market_id)
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
                text = get_Source(url % (x[0], x[1], x[2], 1))
        else:
            writeHlog(market_id,re_date,time)
            url = url1 % (x[0], x[1], x[2]) + "p%s.html"
            page = Page(text)
            for i in range(1, int(page) + 1):
                print(url % (str(i)))
                text = get_Source(url % (str(i)))
                parse(text,name,craw_time)
            return True
    except:
        return False

