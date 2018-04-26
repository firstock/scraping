# coding: utf-8
# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os.path
from os import rename
from os import listdir

import time

import csv
def startWeb(numPage=1):
    """
    @return driver
    """
    driver= webdriver.Chrome('lib/chromedriver.exe')
    url= "http://mabinogi.nexon.com/page/news/notice_list.asp?searchtype=2&searchword=%BA%AF%B0%E6%C1%A1&page="+str(numPage)
    driver.get(url)
    
    return driver
def movePage(numPage):
    url= "http://mabinogi.nexon.com/page/news/notice_list.asp?searchtype=2&searchword=%BA%AF%B0%E6%C1%A1&page="+str(numPage)
    driver.get(url)
    try:
        element= WebDriverWait(driver, 10).until(
            # is comming content?
            EC.presence_of_element_located((By.XPATH, '//ul[@class="notice"]'))
        )
    except Exception as e:
        print('error',e)
def saveLink(listLink):
    xpathLink= '//div[@class="board_common01"]/ul/li/dl/dt/a'
    
    elements= driver.find_elements_by_xpath(xpathLink)
    for element in elements:
        listLink.append(element.get_attribute("href"))
    return listLink
def movePageLink(link):
    driver.get(link)
    try:
        element= WebDriverWait(driver, 10).until(
            # is coming a content?
            EC.presence_of_element_located((By.XPATH, '//div[@class="view_cont"]'))
        )
    except Exception as e:
        print('error',e)
def getContent():
    """
    @return conTitleText, conDateText, conBodyText, 
    """
    try:
        conTitle= WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="board_view01"]/dl/dt'))
        )
        
        conDate= WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="date"]'))
        )
        
        conBody= WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="view_cont"]'))
        )
        
        conWriter= WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH,  '//p[@class="btm_id"]'))
        )
        
        conTitleText= rmSpecialChr(conTitle.text)
        conDateText= rmSpecialChr(conDate.text)
        conBodyText= rmSpecialChr(conBody.text)
        conWriterText= rmSpecialChr(conWriter.text)
    except Exception as e:
        print('error',e)
        
    return conTitleText, conDateText, conBodyText, conWriterText
def rmSpecialChr(weirdStr):
    """
    @param string
    @return string. #특문제거, \n -> ___
    """
    regPattLine= '\n'
    res= re.sub(regPattLine,'___',weirdStr)
    regPatt= '[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9()": ]|[[\u3131-\u318E\uAC00-\uD7A3]]'
    res= re.sub(regPatt,'',res)
    res= re.sub('\\s+', ' ', res) # 공백 제거 해,말아? 하자. 안 하면 헬일듯
    return res


numPages= range(1,61)
listLink= list([])

for numPage in numPages:
    print(numPage)
    movePage(numPage)
    listLink= saveLink(listLink)

listLink

import pandas as pd
from pandas import DataFrame
import re

DataFrame(listLink).to_csv("data/mabinoticeLinks.csv", index= False, header=None)

# read file
mbLinkRead= pd.read_csv("data/mabinoticeLinks.csv", header=None)

mbLinkRead= list(mbLinkRead[0])
mbLinkRead[0:5]
len(mbLinkRead)

driver= startWeb()

titleList= list([])
dateList= list([])
bodyList= list([])
writerPList= list([])

for i, link in enumerate(mbLinkRead):
    #if (0== i):# | (1==i):
    #print(link)
    print(i)
    movePageLink(link)

    title, date, body, writerP= getContent()

    titleList.append(title)
    dateList.append(date)
    bodyList.append(body)
    writerPList.append(writerP)

noticeData= { 
    'title':titleList,
    'date':dateList,
    'zbody':bodyList,
    'writerP':writerPList
}
dfNotice= pd.DataFrame(data= noticeData)

dfNotice.to_csv('data/mbNoticeContent.csv', index= False, encoding= 'cp949')

df= pd.read_csv("data/mbNoticeContent.csv", encoding= 'cp949')

df.columns

# 문자열로 찾기

def findStr(inputStr):
    tradein= lambda x:inputStr in x
    return df[df.zbody.map(tradein)]

inputStr= '�?�?'
findStr(inputStr).to_csv('data/MBfind'+inputStr+'.csv', index= False, encoding= 'cp949')
