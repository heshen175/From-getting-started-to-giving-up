import requests
import re
import json

#第一个def获得URL和想要的正则表达式匹配信息
def parse_html(url):
    #更改头部信息和设置IP信息，应对反爬虫措施，这里要保证代理的IP信息有效。
    #字典方式
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"}
    response = requests.get(url, headers=headers)
    text = response.text

    #正则表达式还是不太会用，这里是直接用的作者的正则表达式，自己写的弄不出来
    # .*? 代表0个或任意个不是\n的任意字符（非贪婪模式，发现一个就立即匹配成功结束）
    regix = '<div class="pic">.*?<em class="">(.*?)</em>.*?<img.*?src="(.*?)" class="">.*?div class="info.*?class="hd".*?class="title">(.*?)</span>.*?class="other">' \
            '(.*?)</span>.*?<div class="bd">.*?<p class="">(.*?)<br>(.*?)</p>.*?class="star.*?<span class="(.*?)"></span>.*?' \
            'span class="rating_num".*?average">(.*?)</span>'


    #第二个代码是把电影名称、导演和演员、评分等信息弄出来
    #有点没有想通为什么这里要调用图片函数
    results = re.findall(regix, text, re.S)                                 #re.S跨行匹配
    for item in results:
        down_image(item[1],headers = headers)                               #调用down_image函数
        yield {                                                             #yield功能类似于return，不同之处在于它返回的是生成器。 具体参考：https://www.cnblogs.com/coder2012/p/4990834.html
            '电影名称' : item[2] + ' ' + re.sub('&nbsp;','',item[3]),       #替换&nbsp;为空值
            '导演和演员' : re.sub('&nbsp;','',item[4].strip()),             #item.strip去除元组收尾空格
            '评分': star_transfor(item[6].strip()) + '/' + item[7] + '分',  #调用star_transfor函数
            '排名' : item[0]                                                # item[0-6]是对应提取值
        }
        

#第三个def获得图片并下载
def down_image(url,headers):
    r = requests.get(url,headers = headers)
    filename = re.search('/public/(.*?)$',url,re.S).group(1)
    with open(filename,'wb') as f:                                          #wb代表打开方式为二进制只用于写入# with open  as f是open（）close（）的简化写法，具体方法参考：https://www.cnblogs.com/tianyiliang/p/8192703.html
        f.write(r.content)                                                  #r.content 是二进制的形式读取R，读取图片就是二进制啊


#第四个def将rating-t形式转化成汉字
def star_transfor(str):
    if str == 'rating5-t':
        return '五星'
    elif str == 'rating45-t' :
        return '四星半'
    elif str == 'rating4-t':
        return '四星'
    elif str == 'rating35-t' :
        return '三星半'
    elif str == 'rating3-t':
        return '三星'
    elif str == 'rating25-t':
        return '两星半'
    elif str == 'rating2-t':
        return '两星'
    elif str == 'rating15-t':
        return '一星半'
    elif str == 'rating1-t':
        return '一星'
    else:
        return '无星'
    
#第五个def将获取的以上信息保存在文本文件中，爬取信息后一般会保存在数据库或者文办文件中
def write_movies_file(str):                                                 #write_movies_file方法传入的是一个字典的参数，因此在爬取到一部电影的信息时，需要将电影信息格式化为一个字典，因此第二个代码
    with open('douban_film.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(str,ensure_ascii=False) + '\n')                  #json.dumps 将 Python 对象编码成 JSON 字符串，将字典转化为字符串，写入文件中#ensure_ascii 保证中文不乱码


#第六个def主函数
def main():
    for offset in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start=' + str(offset) +'&filter='
        for item in parse_html(url):#有一个item对象在parse_html(url)里面
            print(item)
            write_movies_file(item)#调用write_movies_files函数

if __name__ == '__main__':#解释贴：https://blog.csdn.net/anshuai_aw1/article/details/82344884
    main()
