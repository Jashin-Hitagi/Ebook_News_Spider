import requests
import re
from lxml import etree

str1 = input("请输入资源名称：")

def getUrls():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }
    url = 'http://www.yunxs.com/' + str1
    response = requests.get(url=url, headers=headers)
    print(response.encoding,'22',response.apparent_encoding)

    response.encoding = response.apparent_encoding
    data = etree.HTML(response.text)
    a_list = data.xpath('//div[@class="list_box"]//ul/li/a')
    print(a_list)
    a_urls = []
    for a in a_list:
        a_url = url+a.xpath('./@href')[0]
        a_urls.append(a_url)
    return a_urls


def get_text(url):
    response = requests.get(url)
    print(response.encoding, '22', response.apparent_encoding)
    response.encoding = response.apparent_encoding
    content = response.text

    clear = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
    t = clear.sub('', content)
    t = re.sub('<br>', '\r',t)
    data = etree.HTML(t)
    text1 = data.xpath('//div[@class="box_box"]')[0].xpath('string(.)')
    print(text1)
    return text1

def write_to_my():
    a_urls = getUrls()
    book = ''
    for url in a_urls:
        book = book + (get_text(url))
        # print(get_text(url))
    with open(r".\daai.doc", 'w', encoding="utf-8") as file:
        file.write(book)


write_to_my()