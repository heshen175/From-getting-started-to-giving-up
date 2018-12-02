# coding:utf-8
from lxml import etree
import requests

#获取网页
def getHtml(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}

    response = requests.get(url,headers=headers)
    html = response.text
    return html#这里为什么要return啊

    #这是xpath模板
    # movie_img_xpath = '//*[@id="app"]/div/div/div/dl/dd[1]/div/div/div[2]/p/i/text()'
    # s = etree.HTML(html)
    # movie_img = s.xpath(movie_img_xpath)
    # print(movie_img)

#解析网页
def parseHtml(html):
    s = etree.HTML(html)
    movie_name_xpath = '//*[@id="app"]/div/div/div/dl/dd[*]/div/div/div[1]/p[1]/a/text()'
    movie_img_xpath = '//*[@id="app"]/div/div/div/dl/dd[*]/a/img[2]/@data-src'
    movie_actor_xpath = '//*[@id="app"]/div/div/div/dl/dd[*]/div/div/div[1]/p[2]/text()'
    movie_release_time_xpath = '//*[@id="app"]/div/div/div/dl/dd[*]/div/div/div[1]/p[3]/text()'
    movie_score_xpath = '//*[@id="app"]/div/div/div/dl/dd[*]/div/div/div[2]/p/i/text()'

    movie_name = s.xpath(movie_name_xpath)
    movie_img = s.xpath(movie_img_xpath)
    movie_actor = s.xpath(movie_actor_xpath)
    movie_score = s.xpath(movie_score_xpath)
    movie_release_time = s.xpath(movie_release_time_xpath)

    for i in range(len(movie_name)):#这一段代码都不懂
        print('电影名称：' + movie_name[i])
        print('主演：' + movie_actor[i].strip())
        print('图片链接：' + movie_img[i].strip())#去掉前后空格
        print('评分：' + movie_score[2*i] + movie_score[2*i + 1])
        print(movie_release_time[i])
        print('-------------------------------------------强力分割线-------------------------------------------')
def main():
    url = 'http://maoyan.com/board/7'
    html = getHtml(url)
    parseHtml(html)

if __name__ == '__main__':
    main()
