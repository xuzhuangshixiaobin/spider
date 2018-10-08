import requests,time
import json
from lxml import etree
import pypinyin
import pymysql
db = pymysql.connect("101.200.157.254", "xuxiaobin", "xuxiaobin123", "cralwer", charset='utf8')

cursor = db.cursor()

create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

class jwdGet():

        def getlnglat(self,address):
                """根据传入地名参数获取经纬度"""
                url = 'http://api.map.baidu.com/geocoder/v2/'
                output = 'json'  # 输出结果可以是json也可以是其他类型
                ak = 'zkr9VpvpWLXaMmy05AI6TGYMaG4j2pSG'

                add = str(address)

                uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak

                maxNum=5
                for tries in range(maxNum):
                    try:
                        req= requests.get(uri,timeout=30)#设置timeout30秒，防止百度屏蔽,如果被屏蔽就等30秒
                    except:
                        if tries < (maxNum - 1):
                            time.sleep(10)
                            continue
                        else:
                            print("Has tried %d times, all failed!", maxNum)
                            break

                res = req.content.decode()
                answer=json.loads(res)
                lon = float(answer['result']['location']['lng'])
                lat = float(answer['result']['location']['lat'])
                return lon,lat

        def getInfo(self, page, city, citypy):
                url = 'https://' + citypy + '.anjuke.com/community/p' + str(page) + '/'
                print(url)
                headers = {# 由于安居客网站的反爬虫，这里必须要设置header
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                            'Accept-Language': 'zh-CN,zh;q=0.8',
                            # ':authority': 'ty.anjuke.com',
                            # 'Referer': 'https: // wuhan.anjuke.com / sale /?from=navigation',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
                        }
                resp = requests.get(url, headers=headers, timeout=30)
                response=resp.content.decode()
                html=etree.HTML(response)
                div_list=html.xpath("//div[@class='li-itemmod']")
                print(len(div_list))


                for div in div_list:


                        title=div.xpath("./a/@title")[0]
                        dizhi=div.xpath(".//address/text()")[0]
                        addr=dizhi.replace(" ","").replace("\n","")
                        price=div.xpath("./div[@class='li-side']/p[1]//text()")
                        price=(",".join(price)).replace(" ","").replace(",","").replace("\n","")
                        address = city + addr
                        print(address)

                        try:
                                lat, lng = result.getlnglat(address)
                                sql = 'select * from getlnglat_info where title="%s"' % title

                                cursor.execute(sql)
                                num = len(cursor.fetchall())

                                if num == 0:
                                        n = cursor.execute(
                                                "REPLACE INTO getlnglat_info(title, address, price,lng,lat,create_time)" \
                                                " VALUES(%s,%s,%s,%s,%s,%s)", \
                                                (title, address, price,lng,lat,create_time))

                                        db.commit()
                                        time.sleep(3)

                                                    # strip()是去掉每行后面的换行符，只有str类型才能用strip()
                        except:#处理未知异常
                            print("Get AError")






if __name__ == '__main__':

        print( "开始爬数据，请稍等...")
        start_time = time.time()

        # tup1 = [#设置元组，循环取元组中的元素
        #     '广州','深圳', '佛山', '东莞', '珠海', '中山', '惠州', '肇庆', '江门', '清远', '汕头','梅州', '河源',
        #      '揭阳', '潮州', '汕尾', '韶关', '阳江', '茂名', '湛江', '云浮'
        # ];

        tup1 = [  # 设置元组，循环取元组中的元素
                '北京'
        ];
        #汉字转换拼音格式
        for i in tup1:
                city=str(i)
                res = pypinyin.pinyin(i, style=pypinyin.NORMAL)
                citypy = res[0][0] + res[1][0]

                for page in range(20,50):

                        result=jwdGet()
                        result.getInfo(page, city, citypy)
                        time.sleep(5)
        end_time = time.time()
        print("数据爬取完毕，用时%.2f秒" % (end_time - start_time))