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

# import requests # login 편하게? fail
#import copy
def startWeb():
    """
    @return driver
    """
    #options= setDownPath()
    driver= webdriver.Chrome('lib/chromedriver.exe')#, chrome_options= options)
    url= "http://www.saramin.co.kr/zf_user/member/suited-recruit-mail/list"
    driver.get(url)

    return driver
def login():
    try:
        input_id= WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="id"]'))
        )
        input_pw= WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="password"]'))
        )
        userid= "" #사람인 id
        userpw= "" #사람인 pw 하드코딩
        input_id.send_keys(userid)
        input_pw.send_keys(userpw)

        loginBtn= driver.find_element_by_xpath('//button[contains(text(), "로그인")]')
        loginBtn.click()
    except Exception as e:
        print('error',e) 
def getApplyList():
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="sri_btn_immediately"]'))
        )
        elements= driver.find_elements_by_xpath('//span[@class="sri_btn_immediately"]')
        applyLen= len(elements)
        print('즉시지원 개수: ',applyLen)
        return elements
    except Exception as e:
        return 'getApplyListError'+e    
def clickApplyBtn(applyList, index):
    #seemore()
    applyList[index].click()
    
    aleady= aleadyApply() 
    print(aleady)
    if not aleady: # 이미 지원한 공고가 아닐 때만
        selectPart()
        apply()
        clickCancel() #지원완료창 종료
def aleadyApply():
    """새 창
    """
    driver.switch_to.frame(driver.find_element_by_id("quick_apply_frame"))
    
    try:
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="emph"]'))
        )
        print('이미지원한 공고 찾음. 기대값: true')
        clickCancel()
        driver.switch_to_default_content()
        
        return True
    except Exception as e:
        driver.switch_to_default_content() # 원래 iframe로 돌아가기
        return False
        pass
def selectPart():
    """창의 일부
    """
    driver.switch_to.frame(driver.find_element_by_id("quick_apply_frame"))
    
    try:
        elements= WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//ul[@id="optSort"]/descendant::li'))
        )
        if 1== len(elements):
            elements[0].click() #지원부문 선택지가 1개인 경우도 있다
        elements[1].click()
        
    except Exception as e:
        pass
    driver.switch_to_default_content() # 원래 iframe로 돌아가기
    print('selectPart: 원래frame으로 돌아감')
def apply():
    print('apply 진입')
    driver.switch_to.frame(driver.find_element_by_id("quick_apply_frame"))
    print('apply iframe찾음')
    try:
        #파일 추가
        addFile= WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//a[@class="sri_btn_type3 btn_file"]'))
        )
        addFile.click()
    except Exception as e1:
        print('파일추가없엉')
        pass
    
    try:
        #포트폴리오 추가
        addPortfolio1= WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="mfile_idx_4314395"]'))
        )
        addPortfolio2= WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="mfile_idx_4314365"]'))
        )
        addPortfolio1.click()
        addPortfolio2.click()
    except Exception as e2:
        print('퐅폴input없엉')
        pass
    
    try:
        #완료
        submit= WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="sri_btn_complete _attachment_complete_btn"]'))
        )
        submit.click()
    except Exception as e3:
        print('완료없엉')
        pass
    
    try:
        #지원하기 sri_btn_apply
        applySubmit= WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class="sri_btn_apply"]'))
        )
        applySubmit.click()
    except Exception as e4:
        print('지원하기버튼없엉')
        pass
    
    driver.switch_to_default_content() # 원래 iframe로 돌아가기
def clickCancel():
    cancel= driver.find_element_by_xpath('//a[@class="once_ly_close"]')
    cancel.click()
# applyList[1].click()

# clickCancel()

# driver.switch_to.frame(driver.find_element_by_id("quick_apply_frame"))

# driver.switch_to_default_content()
def seemore():
    try:
        seemore= WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//button[@id="btn_more_bar"]'))
        )
        seemore.click()
    except Exception as e3:
        pass


#driver.close()
#driver.quit()


## test
driver= startWeb()
login()
applyList= getApplyList()
index= 4
clickApplyBtn(applyList, index)
#index= 3
#clickApplyBtn(applyList, index)



## RUN - ERROR !
#driver= startWeb()
#login()
#applyList= getApplyList()
#for index,apply in enumerate(applyList):
#    clickApplyBtn(applyList, index) # ERROR- apply() 진입 안 함
