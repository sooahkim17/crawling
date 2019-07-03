import time, pprint, json
from selenium import webdriver
from itertools import count
from bs4 import BeautifulSoup
import pandas as pd
import re


url = 'http://www.megastudy.net/'

teacher_lst = []


#chromedriver 위치 지정
wd = webdriver.Chrome('C:\\Users\CHO\Downloads\chromedriver_win32 (1)\chromedriver.exe')
wd.get(url)

RESULT_DIRECTORY = 'results'
results = []

# teacher list 활성화
selector = wd.find_element_by_class_name('mn_teachersLayer')
selector.click()
#   time.sleep(2)

#   time.sleep(10)
#   wd.execute_script("try{logerClickTrace( 'EVT', '/GNB/고3N수/메가선생님_전체보기');}catch(e){};")
time.sleep(2)

#   nav

#선생님 이름 클릭
html=wd.page_source
bs=BeautifulSoup(html,'html.parser')

inner_wrapper=bs.findAll('div',attrs={'class':'inner_wrap'})
for teacher_name in inner_wrapper:
    name2=teacher_name.findAll('a')

    for i in range(1, len(name2)):
        a=name2[i].attrs['href']
        try:
            #print(str(a))
            wd.get(a)
                
        except:
            url='http://www.megastudy.net'+a
            #printprint(str(url))
            wd.get(url)

        #선생 개인 페이지
        html=wd.page_source
        bs=BeautifulSoup(html,'html.parser')
        teacher_info_wraper = bs.find('h2', attrs={'class':'lnb_tit'})
        try:
            teacher_info = teacher_info_wraper.findAll('a')
        except:
            break
        teacher_sub = teacher_info[0].text #과목
        teacher_name = teacher_info[1].text #선생님 이름

        sub_selector = bs.findAll('p',attrs={'class':'lstedu_bookinfo--tit'}) 

        subject_lst = []
        for selector in sub_selector:
        
            a_selector = selector.find('a') # .text -> 강의 제목
            
            #학원강좌는 'a'가 없다.
            if a_selector is None:
                break
            a=a_selector.attrs['href']
            try:
                #print(str(a))
                wd.get(a)
                
            except:
                url='http://www.megastudy.net'+a_selector.attrs['href']
                try:
                    wd.get(url)
                except:
                    wd.get(url)

            #강의정보 가져오기
            html=wd.page_source
            bs=BeautifulSoup(html,'html.parser')
            lec_selector = bs.find('ul', attrs={'class':'lstedu_bookinfo--schedule'})

            #   강의 정보
            dt_selector = str(lec_selector.findAll('dt'))  # 태그 제거하기 위해 string처리
            dt_selector = re.sub('<.+?>', '', dt_selector, 0).strip('[]')
            dt_selector = list(dt_selector.split(', '))
            dd_selector = str(lec_selector.findAll('dd'))
            dd_selector = re.sub('<.+?>', '', dd_selector, 0).strip('[]')
            dd_selector = list(dd_selector.replace(
                '\n', '').replace('\t', '').split(', '))
            lec_info = dict(zip(dt_selector, dd_selector))  # 강의정보 dict

            #   책 정보
            book_selector = bs.find('div', attrs={'class': 'lstedu_bxitem'})
            lecTitle = str(book_selector.find('label', attrs={'class': 'book_tit'}))
            lecTitle = re.sub('<.+?>', '', lecTitle, 0)  # 강좌이름
            bookName_selector = str(book_selector.findAll(
                'a', attrs={'class': 'ellipsis'}))
            bookName_selector = re.sub(
                '<.+?>', '', bookName_selector, 0).strip('[]')  # 태그제거
            bookName_selector = list(bookName_selector.split(', '))
            bookPrice_selector = book_selector.findAll(
                'span', attrs={'class': 'bx_price--info'})

            if len(bookPrice_selector) != 0:
                lecPrice = bookPrice_selector.pop(0)
            else :
                lecPrice = "0원"
            
            if book_selector.find('span', attrs={'class': 'ft_str'}) is not None :
                lecPrice = bookPrice_selector.pop(0)
            lecPrice = re.sub('<.+?>', '', str(lecPrice), 0).replace('\n','').replace('\t','').strip('[]') #강좌가격
            bookPrice_selector = re.sub('<.+?>', '', str(bookPrice_selector), 0).strip() #책가격
            bookPrice_selector = list(bookPrice_selector.strip('[]').replace(',', '').split('원 '))
            book_info = dict(zip(bookName_selector, bookPrice_selector))


            #   추천 패키지
            package_table = bs.find('table', attrs={'class':'tb_char_opt'})
            packageName_selector = str(package_table.findAll('a', attrs={'class':'basket--itm--text'}))
            packageName_selector = re.sub('<.+?>', '', packageName_selector, 0).strip('[]')#태그제거
            packageName_selector = list(packageName_selector.split('패키지, ')) #패키지 이름
            packagePrice = package_table.findAll('span', attrs={'class':'ft_str'})
            packagePrice_list = []
            for pp in packagePrice:
                packagePrice_selector = str(pp.find('span', attrs={'class':'bx_price--info'}))
                packagePrice_selector = re.sub('<.+?>', '', str(packagePrice_selector), 0).strip('[]') #태그제거
                packagePrice_selector = packagePrice_selector.strip('[]').replace('원', '') #대괄호 제거
                packagePrice_list.append(str(packagePrice_selector))
            package_info = dict(zip(packageName_selector, packagePrice_list))

            subject = {}

            subject['강좌이름'] = lecTitle.replace('\n','').replace('\t','')
            subject['가격'] = lecPrice
            subject['강의정보'] = lec_info
            subject['책'] = book_info
            subject['추천패키지'] = package_info

            subject_lst.append(subject)
        teacher_dict = {}
        
        
        teacher_dict['강사'] = teacher_name
        teacher_dict['과목'] = teacher_sub
        teacher_dict['강의목록'] = subject_lst

        teacher_lst.append(teacher_dict)
        #pprint.pprint(teacher_lst)

with open('json/megastudy.json', 'w', encoding='utf-8') as file:
        json.dump(teacher_lst, file, ensure_ascii=False, indent='\t')
