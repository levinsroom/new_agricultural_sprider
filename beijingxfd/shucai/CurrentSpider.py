from lxml import etree
import datetime
from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import FirefoxOptions

class CurrentSpider:
    #北京新发地菜市场(蔬菜)
    html = ""
    market_name = "北京新发地菜市场"
    url = "http://www.xinfadi.com.cn/priceDetail.html"

    def getDriver(self):
        firefow_options = Options()
        firefow_options.add_argument(
            'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0')
        firefow_options.add_argument('--no-sandbox')
        firefow_options.add_argument("--headless")
        firefow_options.add_argument("--disable-gpu")
        option = FirefoxOptions()
        driver = webdriver.Firefox(firefox_options=firefow_options, options=option)
        return driver

    def get_Source(self, url):
        #打开网页，即打开第一页
        """发起请求 获得源码"""
        try:
            driver = self.getDriver()
            driver.get(url)
            #指定爬取内容
            driver.find_element_by_xpath('//*[@id="sort1"]/li[1]/a').click()
            time.sleep(0.5)
            self.html = driver.page_source
            return driver
        except:
            raise Exception("wrong")
        return html

    def get_next_page(self, driver):
        #切换到下一页
        print("next page")
        driver.find_element_by_class_name("layui-laypage-next").click()
        time.sleep(5)
        self.html = driver.page_source

    def parse(self, text):
        try:
            dom = etree.HTML(text)
            path = "/html/body/div[2]/div/div/div/div[4]/div[1]/div/table/*"
            ul_text = dom.xpath(path)[1:]
            List1, List2 = [], []
            today = str(datetime.date.today())
            yesterday = str(datetime.date.today() + datetime.timedelta(days=-1))
            for li in ul_text:
                table = li.xpath('./tr/td/text()')
                for i in range(len(table)):
                    List2.append(table[i])
                    #比较日期  == 今天，数据进入List1
                    if table[i] == today:
                        List1.append(List2)
                        List2 = []
                    # 比较日期  == 昨天，说明不需要爬取下一页，告知entermenth没有下一页数据
                    elif table[i] == yesterday:
                        return False
                    else:
                        pass
            print(List1)
            #写入我本地
            with open(r'D:\大数据资源管理系统\metabase部署\测试数据\data.csv', "a+") as f:
                for _ in List1:
                    for i in _:
                        #'蔬菜', '大白菜', '0.8', '1.0', '1.2', '冀鲁辽鄂', '斤', '2022-01-15'
                        f.write(i+",")
                    f.write("\n")

            return True
        except:
            raise Exception("wrong")
        return False


    def enterMethod(self):
        try:
            tf = True
            driver = self.get_Source(self.url)
            while tf:
                tf = self.parse(self.html)
                #判断是否有下一页
                if tf :
                    self.get_next_page(driver)
                else:
                    driver.close()
                    driver.quit()
                    break
        except:
            return False
        return True

c = CurrentSpider()
c.enterMethod()