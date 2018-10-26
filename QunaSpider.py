# coding=utf-8
import codecs
import datetime
import time
import random
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# 处理中文编码
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

'''
使用Firefox(应该是被反爬了)
1.日期传不进去，其他无问题(本来可传)
2.编码乱码或者为空

改用phantomjs----(2)ok!
'''


class QunaSpider(object):
    def get_hotel(self, driver, to_city, from_date, to_date):
        # 目的地
        toCity = driver.find_element_by_xpath("//input[@id='toCity']")
        # 入住时间
        fromDate = driver.find_element_by_xpath("//form[@id='mainlandForm']//input[@id='fromDate']")
        # 离店时间
        toDate = driver.find_element_by_xpath("//form[@id='mainlandForm']//input[@id='toDate']")
        # 搜索按钮
        search = driver.find_element_by_xpath("//a[@class='search-button js_btnsearch']")

        toCity.clear()
        toCity.send_keys(to_city)
        # 打印目的地
        print to_city.encode('utf8')

        fromDate.clear()
        fromDate.send_keys(from_date)
        # 打印入住时间
        print from_date

        toDate.clear()
        toDate.send_keys(to_date)
        # 打印离店时间
        print to_date

        # 点击搜索按钮
        search.click()
        page_num = 1

        print 'Crawl start.'
        # print 'quna.txt open satrt.'
        f = codecs.open(u'quna2.txt', 'a', 'utf-8')
        # print 'quna.txt open end.'
        f.write(u'爬取时间：' + datetime.date.today().strftime('%Y-%m-%d') + '\r\n')
        f.write(u'目的地：' + str(to_city) + '\r\n' + u'离店时间：' + str(self.goday) + '\r\n' + u'离店时间：' + str(self.leaveday) + '\r\n')

        while True:
            # 显式等待是否存在目的地10s
            # WebDriverWait默认500ms检测一次元素是否存在
            try:
                WebDriverWait(driver, 10).until(
                    EC.title_contains(unicode(to_city))
                )
            except Exception, e:
                print 'no title.'
                print e
                break

            time.sleep(random.randint(3, 5))
            # 执行js脚本，把网页拉到底部
            js = 'window.scrollTo(0,document.body.scrollHeight);'
            driver.execute_script(js)
            time.sleep(random.randint(1, 3))

            # 数据清洗与存储，把爬取下来的酒店信息按照自己想要的格式存储到本地TXT文件
            infos = driver.find_elements_by_xpath("//div[@class='item_hotel_info']")
            print 'Write file start--%s.' % page_num
            f.write('-' * 30 + str(page_num) + '-' * 30 + '\r\n')
            for info in infos:
                content = info.text.replace(" ", "-->").replace("\t", "-->").replace("\n", "-->")
                f.write(content + '\r\n\n')
            print 'Write file end--%s.' % page_num

            try:
                # 显式等待“下一页”按钮10s
                # WebDriverWait默认500ms检测一次元素是否存在
                next_page = WebDriverWait(driver, 10).until(
                    EC.visibility_of(driver.find_element_by_xpath("//span[@class='icon icon-btn-next-2']"))
                )
                next_page.click()
                page_num += 1
                time.sleep(random.randint(1, 3))

                # 设置爬取前十页
                if page_num == 11:
                    print 'TEST: Crawl 10 pages end.'
                    driver.quit()
                    break
            except Exception, e:
                print 'Crawl end.'
                driver.quit()
                break
        f.close()

    def crawl(self, url, to_city):
        # 入住时间设置为当前日期加5天
        self.goday = datetime.date.today() + datetime.timedelta(days=5)
        self.goday = self.goday.strftime('%Y-%m-%d')
        # 离店时间设置为当前日期加10天
        self.leaveday = datetime.date.today() + datetime.timedelta(days=5 + 5)
        self.leaveday = self.leaveday.strftime('%Y-%m-%d')
        # print self.leaveday

        # 设置PhantomJs请求头User-Agent，防止针对PhantomJs的反爬虫
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = (
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0')
        driver = webdriver.PhantomJS()

        # driver = webdriver.Firefox()
        # 网页加载超时时间
        driver.set_page_load_timeout(30)
        # 打开URL
        driver.get(url)
        # 最大化浏览器
        driver.maximize_window()
        # 隐式等待3s
        # 控制间隔时间，等待浏览器反映
        driver.implicitly_wait(3)
        self.get_hotel(driver, to_city, self.goday, self.leaveday)


if __name__ == '__main__':
    spider = QunaSpider()
    spider.crawl('http://hotel.qunar.com/', u'上海')
