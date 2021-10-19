import re
import urllib.error
import urllib.request
from bs4 import BeautifulSoup
import requests

# class Sql(object):
#     conn = pymysql.connect(
#         host='127.0.0.1',
#         port=3306,
#         user='root',
#         passwd='mysql',
#         db='novel',
#         charset='utf8')
#
#     def addnovel(self,sort,sortname,name,imgurl,description,status,author):
#         cur=self.conn.cursor()
#         cur.execute("insert into novel(sort,sortname,name,imgurl,description,status,author) values('%s','%s','%s','%s','%s','%s','%s') "\
#         %(sort,sortname,name,imgurl,description,status,author))
#
#         lastrowid=cur.lastrowid
#         cur.close()#关闭游标
#         self.conn.commit()
#         return lastrowid
#
#     def addchapter(self,novelid,title,content):
#         cur=self.conn.cursor()
#         cur.execute("insert into chapter(novelid,title,content) values('%s','%s','%s')"%(novelid,title,content))
#         cur.close()
#         self.conn.commit()
#
# mysql=Sql()#实例对象


sort_dict = {
    '1': '玄幻魔法',
    '2': '武侠修真',
    '3': '纯爱耽美',
    '4': '都是言情',
    '5': '职场校园',
    '6': '穿越重生',
    '7': '历史军事',
    '8': '网络动漫',
    '9': '恐怖灵异',
    '10': '科幻小说',
    '11': '美文名著',
}


def getChapterContent(url, lastrowid, title):
    html = requests.get(url)
    html.encoding = 'gbk'
    # print(html.text)
    reg = r'style5\(\);</script>(.*?)<script type="text/javascript">style6\(\);</script></div>'
    html = re.findall(reg, html.text, re.S)[0]
    # mysql.addchapter(lastrowid,title,html)


def getChapterList(url, lastroeid):
    html = requests.get(url)
    html.encoding = 'gbk'
    reg = r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>'
    chapterInfo = re.findall(reg, html.text)
    for url, title in chapterInfo:
        # print(url)
        getChapterContent(url, lastroeid, title)


def getNovel(url, sort_id, sort_name):
    html = askUrl(url)
    soup = BeautifulSoup(html, "html.parser")
    context = str(soup)
    # 获取书名
    reg = r'<meta property="og:novel:book_name" content="(.*?)"/>'
    bookname = re.findall(reg, context)[0]
    # 获取描述
    reg = r'<meta property="og:description" content="(.*?)"/>'
    description = re.findall(reg, context, re.S)[0]  # re.S支持换行符
    # 获取图片
    reg = r'<meta property="og:image" content="(.*?)"/>'
    image = re.findall(reg, context)[0]
    # 获取作者
    reg = r'<meta property="og:novel:author" content="(.*?)"/>'
    author = re.findall(reg, context)[0]
    # 获取状态
    reg = r'<meta property="og:novel:status" content="(.*?)"/>'
    status = re.findall(reg, context)[0]
    # 获取章节地址
    reg = r'<a href="(.*?)" class="reader"'
    chapterUrl = re.findall(reg, context)[0]
    print(bookname, author, image, status, chapterUrl)
    # 插入数据
    # lastrowid = mysql.addnovel(sort_id, sort_name, bookname, image, description, status, author)
    # getChapterList(chapterUrl, lastrowid)
    # getChapterList(chapterUrl, "")


def askUrl(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }
    request = urllib.request.Request(url=url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("GBK", "ignore")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

def getList(sort_id, sort_name):
    baseUrl = "http://www.quanshuwang.com/list/%s_1.html" % sort_id
    html = askUrl(baseUrl)
    soup = BeautifulSoup(html, "html.parser")
    # print(html.text)
    reg = r'<a target="_blank" href="(.*?)" class="l mr10">'
    urlList = soup.find_all('a', class_="l mr10")
    # urlList = re.findall(reg, html.text)
    # print(urlList)
    for url in urlList:
        getNovel(url, sort_id, sort_name)


for sort_id, sort_name in sort_dict.items():
    getList(sort_id, sort_name)
