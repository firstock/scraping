# coding: utf-8
# 사람인 합소서 긁기. release 용
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os.path
from os import rename
from os import listdir
from os import mkdir

import time
import csv

import re



def startWeb(numPage=1):
    """
    @return driver
    """
    driver= webdriver.Chrome('lib/chromedriver.exe')
    url= "http://www.saramin.co.kr/zf_user/public-recruit/coverletter-list/page/"+str(numPage)+"?company_nm="
    driver.get(url)
    
    return driver
    
def movePage(numPage):
    url= "http://www.saramin.co.kr/zf_user/public-recruit/coverletter-list/page/"+str(numPage)+"?company_nm="
    driver.get(url)
    try:
        element= WebDriverWait(driver, 10).until(
            # is coming a content?
            EC.presence_of_element_located((By.XPATH, '//h2'))
        )
    except Exception as e:
        print('error',e)
        
        
def saveLink(dict_pass):
    elements= driver.find_elements_by_xpath('//h2')
    #dict_pass= dict([])
    for element in elements:
        dict_pass[element.text]= element.find_element_by_xpath('a').get_attribute('href')
        #print(i, element.text)
        #print(element.find_element_by_xpath('a').get_attribute('href'))
    return dict_pass
    
def movePageLink(link):
    driver.get(link)
    try:
        element= WebDriverWait(driver, 10).until(
            # is coming a content?
            EC.presence_of_element_located((By.XPATH, '//li'))
        )
    except Exception as e:
        print('error',e)
        
        
def getContent():
    """
    @return element_txt, element_duty
    @except 지원분야가 써있지 않은 페이지?
    """
    try:
        elementCon= WebDriverWait(driver, 3).until(
            # is coming a content?
            EC.presence_of_element_located((By.XPATH, '//div[@class="box_ty3"]'))
        )
        element_txt= rmSpecialChr(elementCon.text)
    except Exception as e:
        print('error',e)
        
    try:
        elementDu= WebDriverWait(driver, 1).until(
            # is coming a content?
            EC.presence_of_element_located((By.XPATH, '//span[@class="tag_apply"]'))
        )
        element_duty= rmSpecialChr(elementDu.text)
    except Exception as e:
        element_duty= '지원분야 공통'
        pass
    
    #element_txt= driver.find_element_by_xpath('//div[@class="box_ty3"]').text
    #element_duty= driver.find_element_by_xpath('//span[@class="tag_apply"]').text
    
    return element_txt, element_duty
    
    
def rmSpecialChr(weirdStr):
    """
    @param string
    @return string. #특문제거, \n -> 띟띟띟
    """
    regPattLine= '\n'
    res= re.sub(regPattLine,'띟띟띟',weirdStr)
    regPatt= '[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9()": ]|[[\u3131-\u318E\uAC00-\uD7A3]]'
    res= re.sub(regPatt,'',res)
    return res
    

numPages= range(1,338)
dictLinks= dict([])

for numPage in numPages:
    print(numPage)
    movePage(numPage)
    dictLinks= saveLink(dictLinks)
 
# dictLinks

driver.close()
driver.quit()

mkdir('data')

with open('data/passLink.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in dictLinks.items():
        writer.writerow([key, value])

print(len(dickLinksRead)  )

driver= startWeb()



## 스레드 필요!. 그냥하면 1시간 45분 가량
dictContents= dict([])

for i, (toJob, link) in enumerate(dickLinksRead.items()):
    #if (62< i) and (78>=i):
    print(i)#, toJob, link)
    movePageLink(link)
    selfintro, duty= getContent()
    dictContents[toJob+' '+duty]= selfintro


with open('data/passContents.csv', 'w', newline='', encoding='cp949') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in dictContents.items():
        writer.writerow([key, value])
        
        
