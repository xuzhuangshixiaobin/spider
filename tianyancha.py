#coding: UTF-8
from selenium import webdriver
import urllib
from pyquery import PyQuery as pq
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
# import pymongo

# mongoclient = pymongo.MongoClient("localhost",port=27017,connect = False)
# db = mongoclient .AugEleventh
# classname = db.alibaba

browser = webdriver.Chrome()
browser.maximize_window()#将浏览器最大化
wait = WebDriverWait(browser,10)

def move_to_bottom():
    # 将滚动条移动到页面的底部
    # js = "var q=document.documentElement.scrollTop=100000"
    #屏蔽广告--对应的div
    browser.execute_script('$("#tyc_banner_bottom").hide()')

def search(keyword):
    url_keyword = urllib.parse.quote(keyword)  # 中文转码为url格式
    url = 'http://www.tianyancha.com/search/' + url_keyword + '?checkFrom=searchBox'
    driver = webdriver.PhantomJS(
        executable_path='E:\\phantomjs-2.1.1-windows\\bin\\phantomjs')  # phantomjs的绝对路径
    time.sleep(2)
    driver.get(url)
    browser.get(url)

    return url



def get_total_page(url):
    #获取所以页数
    total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#web-content > div > div.container-left > div.search-block > div.result-footer > div:nth-child(1) > ul > li:nth-child(11) > a')))
    get_company_info()
    return total.text

def login():
    try:
        #查找前端样式--一级级查找
        userInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#web-content > div > div > div > div.position-rel.container.company_container > div > div.in-block.vertical-top.float-right.right_content.mt50.mr5.mb5 > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in >div.pb30.position-rel > input')))
        passwordInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#web-content > div > div > div > div.position-rel.container.company_container > div > div.in-block.vertical-top.float-right.right_content.mt50.mr5.mb5 > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in > div.pb40.position-rel > input')))
        userInput.send_keys('15995028879')
        passwordInput.send_keys('19981027lcy')
        changeLoginWay = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#web-content > div > div > div > div.position-rel.container.company_container > div > div.in-block.vertical-top.float-right.right_content.mt50.mr5.mb5 > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in > div.c-white.b-c9.pt8.f18.text-center.login_btn')))
        changeLoginWay.click()
    except TimeoutException:
        login()

def get_company_info():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-block .result-list .search-result-single')))
    #获取页面数据
    html = browser.page_source
    doc = pq(html)
    items = doc('.search-block .result-list .search-result-single').items()
    for item  in items:
        urlInfo=item.find('.name ').attr('href')
        name=item.find('.name').text()
        print(name)
        # company = {
        #     'urlInfo':item.find('.name ').attr('href'),
        #     'name' : item.find('.name').text(),
        #     'LegalRepresentative':item.find('.info .title a').text(),
        #     'registerMoney':item.find('.info .title span').eq(0).text(),
        #     'registerTime':item.find('.info .title span').eq(1).text(),
        #     'tel':item.find('.contact .link-hover-click').eq(0).text(),
        #     'email':item.find('.contact .link-hover-click').eq(1).text(),
        #     'LegalPersonInfo':item.find('.content .match span').eq(1).text()
        # }
        # save_to_mongo(company)

def next_page(page_number):
    print('------------------------------------正在爬取',page_number,'页-----------------------------------------------------------------')
    try:
        if page_number == 2:
            #关闭广告
            closeAdvertisement = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#tyc_banner_close')))
            closeAdvertisement.click()
        move_to_bottom()
        if page_number == 2:
            #获取下一页
            nextPageButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#web-content > div > div.container-left > div.search-block > div.result-footer > div:nth-child(1) > ul > li:nth-child(12) > a')))#nth-child其父元素的第 N 个子元素
            nextPageButton.click()
        if page_number > 2:
            nextPageButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#web-content > div > div.container-left > div.search-block > div.result-footer > div:nth-child(1) > ul > li:nth-child(13) > a')))
            nextPageButton.click()
        get_company_info()
        time.sleep(3)
    except TimeoutException:
        #超时重新请求
        next_page(page_number)

# def save_to_mongo(result):
#     if classname.insert(result):
#         print('存储到mongoDB成功',result)
#     else:
#         print('存储到mongoDb失败')

def main():
    keyword = '百度'
    url = search(keyword)
    print(url)
    login()
    # total_pages = int(get_total_page(url)[-3:])#获取下他的总页数，但是没用，因为不是vip只能爬5页，本来我不是想吧下面那个6换成total_pages 的
    # print(total_pages)
    for page in range(2,6):
        next_page(page)
    browser.close()

if __name__ == '__main__':
    main()

