from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.request import Request,urlopen
import time,re,os,sys,argparse,time,struct,json,csv
import requests

###############################################################
def toJson(ebs):
    with open('ebs_grade3.json', 'w', encoding='utf-8') as file :
        json.dump(ebs, file, ensure_ascii=False, indent='\t')

def toJsontoexcle(ebs_excel):
    with open('ebs_excel_grade3.json', 'w', encoding='utf-8') as file :
        json.dump(ebs_excel, file, ensure_ascii=False, indent='\t')

def toCSV(ebs_list):
    with open('ebs.csv', 'w', encoding='utf-8', newline='') as file :
        csvfile = csv.writer(file)
        for row in ebs_list:
            csvfile.writerow(row)
###############################################################


ebs={}

url="http://www.ebsi.co.kr/ebs/pot/potn/retrieveLmsSubMain.ebs?targetCode=D300&Clickz=G001"


driver=webdriver.Chrome('C:\\Users\\salig\\OneDrive\\바탕 화면\\노트북 파일들\\invisible\\chromedriver_win32 (1)\\chromedriver.exe')

driver.get(url)

RESULT_DIRECTORY = '__results__/crawling'
results = []
index=[]
index_f=[]
index_l=[]
t_char=[]
l_char=[]
book_list=[]
book_detail=[]
toexceldict={}

for i in range(1,4):
    driver.get(url)
    time.sleep(6)
    #print(i)
    click_url='//*[@id="stepWrap"]/ul/li['+str(i)+']/a'
   
    driver.find_element_by_xpath(click_url).click()
    time.sleep(4)
    html=driver.page_source
    bs=BeautifulSoup(html,'html.parser')


    sub_url='#stepWrap > div > div.tc0'+str(i)+'> div.domain > div > ul> li'

    sub=bs.select(sub_url)



    #과목순회
    for j in range(1,len(sub)+1):
        #time.sleep(8)
        sub_detail='//*[@id="stepWrap"]/div/div['+str(i)+']/div[1]/div/ul/li['+str(j)+']/a'
        driver.find_element_by_xpath(sub_detail).click()
        time.sleep(3)
        #전체 조회 누르기
        for k in range(2,5):
            all_select='//*[@id="stepWrap"]/div/div['+str(i)+']/div['+str(k)+']/div/ul/li[1]/a'
            driver.find_element_by_xpath(all_select).click()
            time.sleep(2)

        html=driver.page_source
        bs=BeautifulSoup(html,'html.parser')

        lec_list=bs.find('div',attrs={'class':'tbArea'}).find('tbody').findAll('tr')
        
        for t in range(len(lec_list)):
            lec_detail=lec_list[t].find('a')
            if "javascript:" in lec_detail.attrs['href']:
                continue
            else:
                lec_detail_url=lec_detail.attrs['href']
                final_lec_url="http://www.ebsi.co.kr"+lec_detail_url

        
            #if t%80==0:
                #time.sleep(5)
                #print("go")
            req=requests.get(final_lec_url)
            html=req.text
            bs=BeautifulSoup(html,'html.parser')
            if (bs.find('div',{'class':'sum'})and bs.find('div',{'class':'sum'}).find('div',attrs={'class':'tchArea'})and bs.find('div',{'class':'sum'}).find('div',attrs={'class':'tchArea'}).find('span',attrs={'class':'name'})) :



                teacher_name=bs.find('div',{'class':'sum'}).find('div',attrs={'class':'tchArea'}).find('span',attrs={'class':'name'}).find('b')

        
                #강좌 정보
                t_key=teacher_name.text
                if t_key in ebs:
                    teacherdict=ebs[t_key]
                else:
                    teacherdict={}

                lec_name=bs.find('div',attrs={'class':'topLecTit'}).find('a')
            # print(lec_name.text.strip())
                l_key=lec_name.text.strip()
                if l_key not in teacherdict:
                    lecture={}
                else:
                    continue

                lec_info=bs.find('div',attrs={'class':'lecArea'})
                #강좌 정보
                lec_li=lec_info.findAll('li')
                #인공지능 선생님 특징,강좌특징
                lec_ai=bs.findAll('div',attrs={'class':'lecAI_infoHalf'})
                #
                for n in range(6):
                    lec_kind=lec_li[n].find('strong')
                    lec_ans=lec_li[n].find('div',attrs={'class':'lecArea_cont'})
                    
                    if n==0:
                        lecture['과목']=lec_ans.text.strip()
                    if n==1:
                        lecture['학습단계']=lec_ans.text.strip()
                    if n==2:
                        lecture['학년']=lec_ans.text.strip()

                    if n==3:
                        lec_kind=lec_li[n].find('strong')
                        lec_ans=lec_li[n].find('div',attrs={'class':'lecArea_cont'}).find('b')
                        lecture['강좌현황']=lec_ans.text.strip()
                    if n==4:
                        continue
                        
                    if n==5:
                        if lec_ans.text.strip()!="교재가 없는 강좌입니다.":
                            books=lec_ans.findAll('a')
                            if books:
                                for bl in books:
                                    book_id=bl.attrs['href'][27:40]
                                    book_url="http://www.ebsi.co.kr/ebs/lms/lmsx/sbjtBookInfo.ebs?bookId="+book_id+"&sbjtId="+lec_detail_url[41:]
                                    book_req=requests.get(book_url)
                                    book_html=book_req.text
                                    book_bs=BeautifulSoup(book_html,'html.parser')
                                    book_name=book_bs.find('div',attrs={'class':'book_detail'}).find('span')
                                    book_detail.append(book_name.text)
                                    book_price=book_bs.find('div',attrs={'class':'book_detail'}).find('li',{'class':'discount'}).find('b')
                                    if book_price:
                                       book_detail.append(book_price.text)                                
                                    book_list.append(book_detail)
                                    book_detail=[]
                                lecture['book']=book_list
                                book_list=[]
                            else:
                                lecture['book']=lec_ans.text.strip().split('\n')

                

                # print("(",lec_kind.text.strip(),lec_ans.text.strip(),")")
            
                #인공지능 부분 강좌특징 및 선생님 특징
                teacher_features=bs.find('div',attrs={'class':'lecAI_info'}).find('script')


                for a in re.finditer('</em>',teacher_features.text):
                    index_f.append(a.end())
                    
                for b in re.finditer('</li>',teacher_features.text):
                    index_l.append(b.start())
                
                index.append(index_f)
                index.append(index_l)
                # print(index)
                lecture_feature=lec_ai[1].find('p')
            # print(lecture_feature.text)
            # print(len(index_f))
                for l in range(int(len(index_f)/2)-1):
                    if "집계 중입니다."!=teacher_features.text[index_f[l]:index_l[l]]:
                    # print(teacher_features.text[index_f[i]:index_l[i]])
                        l_char.append(teacher_features.text[index_f[l]:index_l[l]])
                #  else:
                #      l_char.append("집계 중입니다.")
                lecture['강좌특징']=l_char
                
                teacher_feature=lec_ai[0].find('p')
            # print(teacher_feature.text)
                for c in range(int(len(index_f)/2)-1,len(index_f)):
                    if "집계 중입니다."!=teacher_features.text[index_f[c]:index_l[c]]:
                        #print(teacher_features.text[index_f[i]:index_l[i]])
                        t_char.append(teacher_features.text[index_f[c]:index_l[c]])
                #  else:
                #     t_char.append("집계 중입니다.")
                lecture['선생님특징']=t_char
                
                lecture['수업료']="0"

                toexceldict[l_key]=t_key
                teacherdict[l_key]=lecture
                ebs[t_key]=teacherdict
            


                index_f=[]
                index_l=[]
                index=[]
                t_char=[]
                l_char=[]
            #print(ebs)
                    
                            
                   
toJson(ebs) # json파일 생성
toJsontoexcle(toexceldict)                
#toCSV(ebs) # csv파일 생성

             