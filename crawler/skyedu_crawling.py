from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.request import Request,urlopen
import time
import re
import os
import sys
import argparse
import time
import struct
import json
import csv

###############################################################
def toJson(skyedu):
    with open('skyedu(1).json', 'w', encoding='utf-8') as file :
        json.dump(skyedu, file, ensure_ascii=False, indent='\t')


def toCSV(skyedu_list):
    with open('skyedu.csv', 'w', encoding='utf-8', newline='') as file :
        csvfile = csv.writer(file)
        for row in skyedu_list:
            csvfile.writerow(row)

def goto():
    time.sleep(3)
    search='fnSearchMathSubmit()'
    driver.execute_script(search)

    time.sleep(5)
    html=driver.page_source
    bs=BeautifulSoup(html,'html.parser')

    infoall=bs.findAll('div',attrs={'class':'summary-info'})
    book_lists=[]
    book_detail=[]
    
        
        #정보가 너무 많아서 검색해서 나온 정보의 첫번째 페이지만 우선 들어가겠음.
    for i in range(len(infoall)):
        if len(infoall)>=1:
            
            ln=infoall[i].find('a',attrs={'class':'summary-info-title'})
            
            if 'href' in ln.attrs:
                urls='http:'+ln.attrs['href']
                html=urlopen(urls)
                bs=BeautifulSoup(html,'html.parser')
                teacher_name=bs.find('div',attrs={'class':'teacher-info'}).find('strong'
                                                                ,attrs={'class':'name'})
                    
                
                t_key=teacher_name.text
                if t_key in skyedu:
                    teacherdict=skyedu[t_key]
                else:
                    teacherdict={}
                
                   
                    
                        
                lec_name=bs.find('label',attrs={'for':'s1'})
                lec_price=bs.find('div',attrs={'class':'class-combine_price-area'}).find('strong',
                              attrs={'class':'discount-price'})
               
                l_key=lec_name.text
                if l_key not in teacherdict:
                    lecture={}
                else:
                    continue
                lecture['url']=urls
                    
                    

                books=bs.findAll('dl',attrs={'class':'class-combine_product-list'})
                #print("교재")
                if len(books)>1 :
                    book_list=books[1].findAll('dd')
                    for i in range(len(book_list)):
                        if (book_list[i].find('label',attrs={'for':'s3'})):
                            book_name=book_list[i].find('label',attrs={'for':'s3'})
                        if (book_list[i].find('label',attrs={'for':'s5'})):
                            book_name=book_list[i].find('label',attrs={'for':'s5'})
                            book_price=book_list[i].find('strong',attrs={'class':'discount-price'})
                            #print("(",book_name.text,book_price.text,")")
                                
                        book_detail.append(book_name.text)
                        book_detail.append(book_price.text)
                        book_lists.append(book_detail)
                        book_detail=[]
                        
                    #print(book_lists)
                    lecture['book']=book_lists
                book_lists=[]
                        
                    

                lecturinfo=bs.find('div',attrs={'class':'sale-box clearfix'})
                lecture_info_all=bs.find('table',attrs={'class':'tbl-lecture-info'})
                lec_ing=lecture_info_all.findAll('tr')
                for i in range(len(lec_ing)):
                    lec_th=lec_ing[i].findAll('th')
                    lec_td=lec_ing[i].findAll('td')
                    for j in range(len(lec_th)):
                        #print("(",lec_th[j].text,lec_td[j].text,")")
                        if i==3 :
                                final_price=lec_td[j].find('strong',attrs={'class':
                                                                           'discount-price'})
                                if final_price is not None:
                                    lecture[lec_th[j].text]=final_price.text
                                else:
                                    lecture[lec_th[j].text]=lec_td[j].text

                        else:
                            lecture[lec_th[j].text]=lec_td[j].text
                teacherdict[l_key]=lecture
                skyedu[t_key]=teacherdict
                #print(skyedu)
        
                    
        else:
            continue

    return skyedu
           
    
###############################################################


skyedu={}

url="https://skyedu.conects.com/lecture/product"

driver=webdriver.Chrome('C:\\Users\salig\OneDrive\바탕 화면\노트북 파일들\invisible\chromedriver_win32 (1)\chromedriver.exe')

driver.get(url)

RESULT_DIRECTORY = '__results__/crawling'
results = []

time.sleep(10)
html=driver.page_source
bs=BeautifulSoup(html,'html.parser')

#학년별 순회
grade_info=bs.find('ul',attrs={'class':
                               'lecture-select-area lecture-select-subject'})
grade_select=grade_info.findAll('a')

for i in range(5):
    driver.get(url)
    

    #학년별로 누르기 고1까지만 누르겠음
    grade_detail=grade_select[i].attrs['onclick']
    #print(grade_detail)
    
    grade=grade_detail
    driver.execute_script(grade)
    
    
    
    if i>2:
        goto()
        continue



    time.sleep(5)
    html=driver.page_source
    bs=BeautifulSoup(html,'html.parser')

    #학년 선택한 다음 과목별 순회
    subject_info=bs.find('ul',attrs={'class':
                                     'lecture-select-area lecture-select-level'})
    subject_select=subject_info.findAll('a')
    #과목별로 순회하면서 검색하고 얻어온 정보 상세 페이지 들어감
    for j in range(len(subject_select)):
        driver.get(url)
        driver.execute_script(grade)

        time.sleep(5)
        subject_detail=subject_select[j].attrs['onclick']
        #print(subject_detail)


        subject=subject_detail
        driver.execute_script(subject)

        time.sleep(10)
        search='fnSearchSubmit()'
        driver.execute_script(search)



        time.sleep(12)
        html=driver.page_source
        bs=BeautifulSoup(html,'html.parser')

        infoall=bs.findAll('div',attrs={'class':'summary-info'})
        #print(len(infoall))
        book_lists=[]
        book_detail=[]
        
        #정보가 너무 많아서 검색해서 나온 정보의 첫번째 페이지만 우선 들어가겠음.
        for i in range(len(infoall)):
            if len(infoall)>=1:
                ln=infoall[i].find('a',attrs={'class':'summary-info-title'})
                if 'href' in ln.attrs:
                    urls='http:'+ln.attrs['href']
                    #driver.get(urls)
                    #lp=infoall.find('strong',attrs={'class':'price-discount'})
                    
                    #print(ln.text)
                    #time.sleep(6)
                    html=urlopen(urls)
                    bs=BeautifulSoup(html,'html.parser')
                    #time.sleep(4)
                    teacher_name=bs.find('div',attrs={'class':'teacher-info'}).find('strong'
                                                                ,attrs={'class':'name'})
                    
                    #print(teacher_name.text)
                    t_key=teacher_name.text
                    if t_key in skyedu:
                        teacherdict=skyedu[t_key]
                    else:
                        teacherdict={}
                
                   
                    
                        
                    lec_name=bs.find('label',attrs={'for':'s1'})
                    lec_price=bs.find('div',attrs={'class':'class-combine_price-area'}).find('strong',
                              attrs={'class':'discount-price'})
                    #print("(",lec_name.text,lec_price.text,")")
                    l_key=lec_name.text
                    if l_key not in teacherdict:
                        lecture={}
                    else:
                        continue
                    
                
                    lecture['url']=urls

                    books=bs.findAll('dl',attrs={'class':'class-combine_product-list'})
                    #print("교재")
                    if len(books)>1 :
                        book_list=books[1].findAll('dd')
                        for i in range(len(book_list)):
                            if (book_list[i].find('label',attrs={'for':'s3'})):
                                book_name=book_list[i].find('label',attrs={'for':'s3'})
                            if (book_list[i].find('label',attrs={'for':'s5'})):
                                book_name=book_list[i].find('label',attrs={'for':'s5'})
                            book_price=book_list[i].find('strong',attrs={'class':'discount-price'})
                            #print("(",book_name.text,book_price.text,")")
                                
                            book_detail.append(book_name.text)
                            book_detail.append(book_price.text)
                            book_lists.append(book_detail)
                            book_detail=[]
                        
                        #print(book_lists)
                        lecture['book']=book_lists
                    book_lists=[]
                        
                    

                    lecturinfo=bs.find('div',attrs={'class':'sale-box clearfix'})
                    lecture_info_all=bs.find('table',attrs={'class':'tbl-lecture-info'})
                    lec_ing=lecture_info_all.findAll('tr')
                    for i in range(len(lec_ing)):
                        lec_th=lec_ing[i].findAll('th')
                        lec_td=lec_ing[i].findAll('td')
                        for j in range(len(lec_th)):
                            #print("(",lec_th[j].text,lec_td[j].text,")")
                            if i==3 :
                                final_price=lec_td[j].find('strong',attrs={'class':
                                                                           'discount-price'})
                                if final_price is not None:
                                    lecture[lec_th[j].text]=final_price.text
                                else:
                                    lecture[lec_th[j].text]=lec_td[j].text

                            else:
                             lecture[lec_th[j].text]=lec_td[j].text
                    teacherdict[l_key]=lecture
                    skyedu[t_key]=teacherdict
                    #print(skyedu)
                    
        else:
            continue
           
                                   
#toCSV(skyedu) # csv파일 생성
toJson(skyedu) # json파일 생성
             


  
    
    

