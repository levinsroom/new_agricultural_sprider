import re
from lxml import etree
from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options

# 无头浏览器（无可视化界面）
firefow_options = Options()
firefow_options.add_argument("--headless")
firefow_options.add_argument("--disable-gpu")
# 不加载图片
firefow_options.add_argument('blink-settings=imagesEnabled=false')


def get_Source(url):
    try:
        driver = webdriver.Firefox(options=firefow_options)
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        driver.quit()
    except:
        return "404"
    return html


def getTime(text):
    try:
        dom = etree.HTML(text)
        title_list = dom.xpath("/html/head/title")
        data = [_.xpath('string(.)') for _ in title_list]
        time = re.findall(r"\d+\.?\d*", data[0])
        return time[0]+"-"+time[1]+"-"+time[2]
    except:
        raise Exception()


def parse(text):
    try:
        dom = etree.HTML(text)
        p_path = "/html/body/div[1]/div[2]/div[1]/div/div[1]/div[3]/p[%s]"
        table_path = "/html/body/div[1]/div[2]/div[1]/div/div[1]/div[3]/table[%s]/tbody/tr"
        list = [str(_) for _ in range(3, 20, 2)]
        for i in range(0, len(list)):
            title = ""
            p_list = dom.xpath(p_path % list[i])
            table_list = dom.xpath(table_path % str(i + 1))
            alltext = [title.xpath('string(.)') for title in p_list]
            if alltext[0] == "":
                for i in range(i, len(list)):
                    list[i] = str(int(list[i]) + 1)
                alltext = [title.xpath('string(.)') for title in dom.xpath(p_path % str(int(list[i])))]
            for _ in alltext[0].split("\xa0"):
                title = title + _
            print(title)  # 市场名字
            # 对应市场价格
            for tr in table_list:
                Alltext = tr.xpath('string(.)')
                food = re.findall(r"\D+\.?\D*", Alltext)
                result = []
                [result.append(x) for x in food if x not in ['-', ",", "."]]
                price = re.findall(r"\d+\.?\d*", Alltext)
                if len(price) == 5:
                    x1 = price[2] if len(price[2]) <= 2 else price[2][0:3] if "." in price[2] else price[2][0:2]
                    x2 = price[4] if len(price[4]) <= 2 else price[4][0:3] if "." in price[4] else price[4][0:2]
                    print({"name": result[0], "min": price[1],
                           "max": x1})
                    print({"name": result[1], "min": price[3],
                           "max": x2})
    except:
        raise Exception("wrong")


def enter():
    # url = input("请输入网址\n")
    url = "https://mp.weixin.qq.com/s/CXDX75o2qxo--9wUL3ScEw"
    text = get_Source(url)
    if text == "404":
        return False
    else:
        print(getTime(text))
        parse(text)
        return True
    return False

enter()
