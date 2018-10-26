# QunaSpider

- 目标网站：http://hotel.qunar.com
- 说明：使用Selenium+PhantomJS爬取去哪儿网酒店信息，并保存到本地TXT文件。本次爬取的信息：入住日期为当前日期后5天，离店日期为当前日期后10天，目的地为上海。
- 代码解析：
    - 设置PhantomJs请求头User-Agent，防止针对PhantomJs的反爬虫
    ```
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = (
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0')
    ```
    - 设置入住时间和离店时间
    ```
    # 入住时间设置为当前日期加5天
    self.goday = datetime.date.today() + datetime.timedelta(days=5)
    # 离店时间设置为当前日期加10天
    self.leaveday = datetime.date.today() + datetime.timedelta(days=5 + 5)
    ```
    - 网站使用Ajax技术，不能确定网页元素什么时候被完全加载。执行js脚本，把网页拉到底部加载全部网页元素。等待网页元素加载有显式等待和隐式等待。
    ```
    js = 'window.scrollTo(0,document.body.scrollHeight);'
    driver.execute_script(js)
    ```
    - 显式等待——条件触发式的等待，指定某一特定条件直到其成立才继续执行，可以设置超时时间，超时条件仍未成立会抛出异常。
    ```
    # 显式等待是否存在目的地10s
    # WebDriverWait默认500ms检测一次元素是否存在
    WebDriverWait(driver, 10).until(
    EC.title_contains(unicode(to_city))
    )
    
    # 显式等待“下一页”按钮10s
    # WebDriverWait默认500ms检测一次元素是否存在
    next_page = WebDriverWait(driver, 10).until(
        EC.visibility_of(driver.find_element_by_xpath("//span[@class='icon icon-btn-next-2']"))
    )
    ```
    - 隐式等待——尝试发现某个元素时，若未能及时发现，就等待固定时间，默认为0s，类似socket超时。作用范围为整个Webdriver实例整个生命周期，即Webdriver执行每条命令的超时时间都是隐式等待时间。
    ```
    # 隐式等待3s
    # 控制间隔时间，等待浏览器反映
    driver.implicitly_wait(3)
    ```
    - 数据清洗与存储，把爬取下来的酒店信息按照自己想要的格式存储到本地TXT文件。酒店信息中的' '和'\t'和'\n'全部替换为'-->'。
    ```
    content = info.text.replace(" ", "-->").replace("\t", "-->").replace("\n", "-->")
    ```
- 效果图
    - 在pycharm运行后截图
    ![image](https://raw.githubusercontent.com/LZC6244/QunaSpider/master/images_demo/1.png)
    - 去哪网截图验证爬取信息
    ![image](https://raw.githubusercontent.com/LZC6244/QunaSpider/master/images_demo/2.png)
