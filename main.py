from selenium import webdriver  #导入Selenium
import requests
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import os  #导入os模块
import time
from selenium.webdriver.common.keys import Keys  #导入Keys
import urllib.parse
import json
import re

class BeautifulPicture():

    def __init__(self):  #类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'https://bcy.net/u/25285/post/'  #要访问的网页地址
        self.folder_path = 'D:\\BeautifulPicture\\'  #设置图片要存放的文件目录

    def get_pic(self):
        print('开始网页get请求')
        # 使用selenium通过PhantomJS来进行网络请求
        driverOptions = webdriver.ChromeOptions()
        driverOptions.add_argument(r"uuser-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data")
        driverOptions.add_argument("headless")
        driverOptions.add_argument("--start-maximized")
        #driverOptions.add_argument(r"executable_path='E:\Projects\Self\SelfPython\chromedriver\chromedriver.exe'")
        #driver = webdriver.Chrome(executable_path=r'D:\phython\chromedriver.exe',user-data-dir=r'user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data')
        driver = webdriver.Chrome(r"chromedriver\chromedriver.exe",0,driverOptions)
        driver.maximize_window()
        driver.get(self.web_url)
        #time.sleep(20)
        # 删除第一次建立连接时的cookie
        driver.delete_all_cookies()
        with open('d:\\cookies.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        for cookie in listCookies:
            driver.add_cookie(cookie)
        print('已重新设置登录信息，正在重新跳转。。。')
        driver.get(self.web_url)
        username = driver.find_element_by_class_name("fz18")
        usernamestr=username.text
        self.folder_path+=usernamestr

        print('开始创建文件夹')
        is_new_folder = self.mkdir(self.folder_path)  #创建文件夹，并判断是否是新创建
        print('开始切换文件夹')
        os.chdir(self.folder_path)   #切换路径至上面创建的文件夹

        #pagescount = driver.find_element_by_class_name("pager__item")
        #print(pagescount.text+'\n')
        #pagetotalcount = re.sub("\D", "", pagescount.text)
        #print(pagetotalcount)
        #pagetotalcount=1
        totalCount = 2
        #round(int(pagetotalcount)/35+0.5)
        CurCount=0
        CurPage=1
        while CurPage<=totalCount:
            driver.get(self.web_url+'?&p='+str(CurPage))

            listCards = driver.find_elements_by_class_name("db")

            #self.scroll_down(driver=driver, times=1)  #执行网页下拉到底部操作，执行3次
            print('开始获取所有Cards')
            all_a = BeautifulSoup(driver.page_source, 'lxml').find_all('li', class_='js-smallCards')  #获取网页中的class为cV68d的所有a标签
            

            everypagecount = len(all_a)
            print("img标签的数量是：", everypagecount)   #这里添加一个查询图片标签的数量，来检查我们下拉操作是否有误
            file_names = self.get_files(self.folder_path)  #获取文件家中的所有文件名，类型是list
            i=1
            for a in listCards: #循环每个标签，获取标签中图片的url并且进行网络请求，最后保存图片
                
                print('\n开始第'+str(CurPage)+'页中的第'+str(i)+'篇，一共'+str(CurCount+1)+'篇')
                
                # 新开一个窗口，通过执行js来新开一个窗口
                strtemp = a.get_attribute('href')
                print(strtemp)
                if strtemp==None:
                    i+=1
                    CurCount+=1
                    print('出现问题，已跳过')
                    continue
                js='window.open("'+strtemp+'");'
                driver.execute_script(js)
                #a.click()
                driver.switch_to_window(driver.window_handles[1])
                all_img_a = BeautifulSoup(driver.page_source, 'lxml').find_all('a', attrs={"data-lightbox": "lightbox"})  #获取网页中的class为cV68d的所有a标签
                for _a in all_img_a:
                    img_str = _a['href'] #a标签中完整的style字符串
                    print('a标签的img_str内容是：', img_str)
                    #print('a标签的data-imgurl内容是：', img_str)
                    first_pos = img_str.index('url=') + 4
                    #second_pos = img_str.index('.jpg')+4
                    img_url = urllib.parse.unquote(img_str[first_pos:-7]) #使用Python的切片功能截取双引号之间的内容
                    print('a标签的data-imgurl内容是：', img_url)
                    # 注：为了尽快看到下拉加载的效果，截取高度和宽度部分暂时注释掉，因为图片较大，请求时间较长。
                    #获取高度和宽度的字符在字符串中的位置
                    # width_pos = img_url.index('&w=')
                    # height_pos = img_url.index('&q=')
                    # width_height_str = img_url[width_pos : height_pos]
                    # #使用切片功能截取高度和宽度参数，后面用来将该参数替换掉
                    # print('高度和宽度数据字符串是：', width_height_str)
                    # img_url_final = img_url.replace(width_height_str, '')
                    # #把高度和宽度的字符串替换成空字符
                    # print('截取后的图片的url是：', img_url_final)

                    #截取url中参数前面、网址后面的字符串为图片名
                    name_start_pos = img_url.index('.com/') + 5  #通过找.com/的位置，来确定它之后的字符位置
                    img_name = usernamestr + img_url[name_start_pos : ] 
                    img_name = img_name.replace('/','')  #把图片名字中的斜杠都去掉

                    if is_new_folder:
                        self.save_img(img_url, img_name)  # 调用save_img方法来保存图片
                    else:
                        if img_name not in file_names:
                            self.save_img(img_url, img_name)  # 调用save_img方法来保存图片
                        else:
                            print("该图片已经存在：", img_name, "，不再重新下载。")
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
                i+=1
                CurCount+=1
            CurPage+=1

    def save_img(self, url, file_name): ##保存图片
        print('开始请求图片地址，过程会有点长...')
        img = self.request(url)
        print('开始保存图片')
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name,'图片保存成功！')
        f.close()

    def request(self, url):  #返回网页的response
        r = requests.get(url)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        return r

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
            return True
        else:
            print(path, '文件夹已经存在了，不再创建')
            return False

    def scroll_down(self, driver, times):
        for i in range(times):
            print("开始执行第", str(i + 1),"次下拉操作")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  #执行JavaScript实现网页下拉倒底部
            print("第", str(i + 1), "次下拉操作执行完毕")
            print("第", str(i + 1), "次等待网页加载......")
            time.sleep(5)  # 等待30秒，页面加载出来再执行下拉操作

    def get_files(self, path):
        pic_names = os.listdir(path)
        return pic_names

beauty = BeautifulPicture()  #创建类的实例
beauty.get_pic()  #执行类中的方法
