import requests
from lxml import etree
import csv
f = open("豆瓣top250.csv","w",encoding="GB18030",newline="")
writer = csv.DictWriter(f,fieldnames=["电影排名","电影名称","演员表","电影评分","电影短评"])
writer.writeheader()
for x in range(0,226,25):#拼接每一页的地址
    url = "https://movie.douban.com/top250?start={}&filter=".format(x)
    headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    response = requests.get(url=url,headers=headers)
    htmljx_obj = etree.HTML(response.text)
    div_list = htmljx_obj.xpath('//div[@class="item"]')
    for div in div_list:
        rank = div.xpath('div[1]/em/text()')[0]
        movie_name =div.xpath('div[2]/div[1]/a/span/text()')
        director = div.xpath('div[2]/div[2]/p/text()')
        grade = div.xpath('div[2]/div[2]/div/span[2]/text()')[0]
        #因为有的电影没有短评，强行匹配短评会报错！
        try:
            short_comment = div.xpath('div[2]/div[2]/p[2]/span/text()')[0]
        except Exception as e:
            short_comment="没有短评"
        #定义一个字符串，存储清理过后的电影名称
        movie_name_string = ''
        for movie in movie_name:
            #把电影名称中的\xa0替换成空，然后把处理过后的电影名称拼接起来
            movie_name_string+=movie.replace("\xa0","")
        #用字符串存储清理过后的导演信息
        movie_director_string = ''
        for movie_director in director:
            movie_director_string+=movie_director.replace('\n',"").replace("\xa0","").replace(" ","")
        movie_dict = {"电影排名":rank,"电影名称":movie_name_string,"演员表":movie_director_string,"电影评分":grade,"电影短评":short_comment}
        writer.writerow(movie_dict)
f.close()


