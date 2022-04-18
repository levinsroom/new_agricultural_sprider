import requests
from lxml import etree
import time
from pyquery import PyQuery as pq

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75"
    }
def get_Source(url,headers):
    r = requests.post(url, headers=headers)
    r.encoding = 'utf8'
    html = r.text
    return html

def jc(text,url):
    doc = pq(text)
    for td in doc("title").items():
        if td.text() == "解除屏蔽":
            print("被屏蔽，解除ing")
            from Agricultural.shangwu.solve.jiechu import Jiechu
            if Jiechu().solve("https://price.21food.cn/guoshu/shuiguo/"):
                return get_Source(url,headers)
            else:
                Jiechu().solve("https://price.21food.cn/guoshu/shuiguo/")
                return get_Source(url, headers)
        else:
            return text
def parse(url,crawl):
    for i in url:
        text = jc(get_Source(i,headers),i)
        dom = etree.HTML(text)
        path = "/html/body/div[2]/div[3]/div/div[2]/div[1]/div[2]/div[2]/ul/*"
        ul_text = dom.xpath(path)
        for li in ul_text:
            name = li.xpath('./table/tr/td[1]/a/text()')[0]
            market_name = li.xpath('./table/tr/td[2]/a/text()')[0]
            max = li.xpath('./table/tr/td[3]/span/text()')[0]
            min = li.xpath('./table/tr/td[4]/span/text()')[0]
            avg = li.xpath('./table/tr/td[5]/span/text()')[0]
            report = li.xpath('./table/tr/td[6]/span/text()')[0]
            if report == crawl:
                print(name, market_name, max, min, avg,report,crawl)
            else:
                break
        time.sleep(5)
    return False
#
# text = get_Source("https://price.21food.cn/guoshu/",headers)
# parse(text,"2021-03-06")
