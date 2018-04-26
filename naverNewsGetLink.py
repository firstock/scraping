# coding: utf-8
import pandas as pd
import numpy as np
df= pd.read_csv('data/naverNewsSomePressLinks.csv', index_col=False, header=None)
len(df)

## 긁으려는 거 외 링크 지우기
# 133개 지움
exceptList= ['www.kukinews.com', 'news.kukinews.com', 'www.seouland.com', 'nownews.seoul.co', 'nownewstv.seoul.co', 'www.sporbiz.co', 'www.beautyhankook.com']
for exLink in exceptList:
    df= df[df[0].map(lambda x: (exLink not in x))]
df
len(df)
df[0].map(lambda x: (exceptList[0] in x)).sum()

## dict 만들기
# key: http빼고 사이트 앞 3어절, value: XPATH
link= ['news.khan.co', 'www.khan.co', 'h2.khan.co', 'news.kmib.co', 'www.naeil.com', 'news.donga.com', 'www.donga.com', 'realestate.donga.com', 'bizn.donga.com', 'travel.donga.com', 'studio.donga.com', 'yachtpia.donga.com', 'it.donga.com', 'www.m-i.kr', 'www.munhwa.com', 'www.seoul.co', 'ntn.seoul.co', 'stv.seoul.co', 'www.segye.com', 'local.segye.com', 'www.segyefn.com', 'economysegye.segye.com', 'fn.segye.com', 'www.asiatoday.co', 'news.chosun.com', 'biz.chosun.com', 'car.chosun.com', 'life.chosun.com', 'businessnews.chosun.com', 'news.joins.com', 'realestate.joins.com', 'www.hani.co', 'babytree.hani.co', '2korea.hani.co', 'www.hankookilbo.com', 'www.newsis.com', 'sports.news.naver', 'news.naver.com', 'app.yonhapnews.co', 'www.wowtv.co', 'www.wownet.co', 'news.wowtv.co', 'sports.wowtv.co', 'wowstar.wowtv.co', 'news.jtbc.co', 'www.sisain.co', 'www.sisainlive.com']
dupCnt= [3,1,1,8,1,1,3,5,1,5,2,3,1,2,2,5,1,2]
xpaths= ['//div[@id="articleBody"]', '//div[@id="articleBody"]', '//div[@class="articleArea"]', '//div[@id="ct"]', '//div[@class="content"]', '//div[@id="NewsAdContent"]', '//div[@id="article_content"]', '//div[@id="article_txt"]', '//div[@id="font"]', '//div[@id="news_body_id"]/div[@class="par"]', '//div[@id="article_body"]', '//div[@class="article-text-font-size"]', '//article[@id="article-body"]', '//div[@id="#textBody"]', '//div[@id="articleWrap"]', '//div[@id="divNewsContent"]', '//div[@class="article_content"]', '//div[@itemprop="articleBody"]']
xpaths= np.array(xpaths)
print(len(xpaths))
print(len(dupCnt))
xpaths_s= list(xpaths.repeat(dupCnt))
xpaths_s
print(link)
print(xpaths_s)
dictLink= dict(zip(link,xpaths_s))
dictLink

## xpath 얻기
sriLink= df[0].map(lambda x: '.'.join(x.split('/')[2].split('.')[0:3]))
sriLink
sriLink.value_counts()
xpathList= list([])
for link in sriLink:
    xpathList.append(dictLink[link])
xpathList
