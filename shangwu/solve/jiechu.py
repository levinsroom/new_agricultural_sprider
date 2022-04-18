from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import FirefoxOptions
from PIL import Image
from 爬虫.Myselenium.yanzhengma import chaojiying

class Jiechu:
    def getDriver(self):
        firefow_options = Options()
        firefow_options.add_argument(
            'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0')
        firefow_options.add_argument('--no-sandbox')
        firefow_options.add_argument("--headless")
        firefow_options.add_argument("--disable-gpu")
        # selenium规避检测
        option = FirefoxOptions()
        driver = webdriver.Firefox(firefox_options=firefow_options, options=option)
        return driver

    def solve(self,url):
        driver = self.getDriver()
        driver.get(url)
        ID = driver.find_element_by_id("delipcode")
        #验证码图片路径
        path = "D:\\机器学习\\Agricultural\\shangwu\\solve\\image\\"
        driver.save_screenshot(path + "01.png")
        time.sleep(2)
        # 定位验证码图片
        code_img_ele = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[2]/form/div[1]/span/img")
        # 定位验证码图片左上角和右下角坐标（裁剪区域确定）
        location = code_img_ele.location  # 左上角坐标x，y
        size = code_img_ele.size  # 长度，宽度
        rangle = (
            int(location['x']), int(location['y']),
            int(location['x'] + size['width']), int(location['y'] + size['height'])
        )
        print("截图")
        # 裁剪
        I = Image.open(path + "01.png")
        code_img_name = 'code.png'
        frame = I.crop(rangle)
        frame.save(path + code_img_name)
        cj = chaojiying.Chaojiying_Client('20340869670126', '647356ybf', '912479')
        # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        im = open(path+code_img_name, 'rb').read()
        data = cj.PostPic(im, 1902)
        ID.send_keys(data['pic_str'])
        time.sleep(2)
        login = driver.find_element_by_class_name("r_min_t_uiu_p")
        login.click()
        time.sleep(5)
        driver.quit()
        print("解除成功")




