# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from sqlalchemy import Column, ForeignKey, Integer, CHAR, Date, String, Time, Index, DateTime, TIMESTAMP, func, or_
from sqlalchemy.dialects.mysql import INTEGER, BIT, TINYINT, TIME, DOUBLE, TEXT,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup 
import requests
import finda_table
import pandas as pd
import numpy as np
import re 
from itertools import chain
class Finda_crawler(object):

    def __init__(self):
        server = '127.0.0.1'
        connection_string = 'mysql+mysqldb://root:MYSQLpassword@{}:3306/findas'.format(server)
        engine = create_engine(connection_string, pool_recycle = 3600, encoding='utf-8')
        Session = sessionmaker(bind=engine)
        self.Session = Session 

    def mortgage_rent(self):
        mortconcatenated = chain(range(6,231), range(623, 1025))
        rentconcatenated = range(4,260)
        for productid in mortconcatenated:
            self.rent_crawler(productid, 'MORT')

        for productid in rentconcatenated:
            self.finda_crawler(productid,'RENT')

    def deposit_fixed(self):
        for productid in range(2359, 3399):
            self.finda_crawler(productid, 'DEPOSITFSS')

    def deposit_periodic(self):
        for productid in range(8,655):
            self.finda_crawler(productid, 'DEPOSIT')

    def p2p_invest(self):
        for productid in range(774,1610):
            self.finda_crawler(productid, 'P2PINVEST')

    def p2p_loan(self):
        for productid in range(1,16):
            self.finda_crawler(productid, 'P2PLOAN')

    def finda_crawler(self,productid, product_type):
        session = self.Session()
        data = requests.get('https://www.finda.co.kr/review/detail/?product_id={}&product_type={}'.format(productid, product_type))
        soup = BeautifulSoup(data.text)
        idandtype = str(productid) + product_type #제품 id and type
        print idandtype
        temp = soup.find('div',attrs = {'class': 'review-title container'})
        product_name = temp.find('h2').get_text() #제품명
        if len(product_name) < 1:
            print 'no product in this page'
            return False

        company_https = temp.find('img').attrs['src'] 
        company = re.findall('bank\/(\w+)',company_https.encode('utf-8'))[0] #상품회사 이름
        reviews = finda_table.reviews
        if product_type == 'RENT': #대출 상품을 크롤링하는 경우
            rent = finda_table.rent
            for  tag_index ,data in  enumerate(temp.find('div', attrs = {'class' : 'review-data' }).find_all('div')):
                if tag_index == 0 :
                    interest_type = data.find('p').get_text()

                elif tag_index == 1 :
                    try:
                        highest_rate = float(re.match('\d.\d+',data.find('p').get_text()).group())
                    except:
                        highest_rate = float(re.match('\d+',data.find('p').get_text()).group())
                        
                elif tag_index == 2 :
                    try:
                        lowest_rate = float(re.match('\d.\d+',data.find('p').get_text()).group())
                    except:
                        lowest_rate = float(re.match('\d+',data.find('p').get_text()).group())

                elif tag_index == 3:
                    try:
                        last_month_interest =  float(re.match('\d.\d+',data.find('p').get_text()).group())         
                    except:
                        last_month_interest =  float(re.match('\d+',data.find('p').get_text()).group())   
                else:
                    maximum_period =  int(re.match('\d+',data.find('p').get_text()).group())      

            for detail_index,detail in enumerate(temp.find_all('div',attrs = {'class' : 'review-info'})): 
                if detail.find('h5').get_text().encode('utf-8') == '우대금리 항목':
                        preference = detail.find('p').get_text()
                elif detail.find('h5').get_text().encode('utf-8') == '중도상환수수료':
                        redemption_fee = detail.find('p').get_text()
                elif detail.find('h5').get_text().encode('utf-8') == '대출 관련 비용':
                        related_fee = detail.find('p').get_text()
            scoreboard = soup.find('div', attrs = {'score-total card'})
            
            try: #상품에 댓글이 달린경우
                review_counts = int(re.match('\W+(\d+)', scoreboard.find('p').get_text()).group(1))
                average_rate = float(scoreboard.find('h4').get_text())        
                rowdata = rent(idandtype = idandtype, productname = product_name.encode('utf-8'),interest_type = interest_type.encode('utf-8'), company = company, lowest_rate = lowest_rate,
                                   highest_rate = highest_rate,last_month_interest = last_month_interest, maximum_period = maximum_period,
                                   preference = preference.encode('utf-8'), redemption_fee = redemption_fee.encode('utf-8'),
                                   related_fee = related_fee.encode('utf-8'), review_counts = review_counts, average_rate = average_rate)
            except:
                rowdata = rent(idandtype = idandtype, productname = product_name.encode('utf-8'),interest_type = interest_type.encode('utf-8'), company = company, lowest_rate = lowest_rate,
                                   highest_rate = highest_rate,last_month_interest = last_month_interest, maximum_period = maximum_period,
                                   preference = preference.encode('utf-8'), redemption_fee = redemption_fee.encode('utf-8'),
                                   related_fee = related_fee.encode('utf-8'),review_counts = 0)

            try:
                session.add(rowdata)
            except :
                session.close()
                print 'rent_product_adding error',idandtype
                return False
            
            
        elif product_type == 'DEPOSITFSS': #정기예금을 크롤링하는 경우 
            deposit_fixed = finda_table.deposit_fixed
            for  tag_index ,data in  enumerate(temp.find('div', attrs = {'class' : 'review-data' }).find_all('div')):
                if tag_index == 0 :
                    interest_type = data.find('p').get_text()

                elif tag_index == 1 :
                    try:
                        highest_rate = re.findall('\d.\d+', data.find('p').get_text())[1] #최고 이자율이 실수형태로 되어있는 경우
                    except:
                        print 'interest rate error '
                        highest_rate = re.findall('\d+', data.find('p').get_text())[1] #최고 이자율이 정수 형태로 되어있는경우

                elif tag_index == 2 :
                    try:
                        deposit_limit = data.find('p').get_text()
                    except:
                        deposit_limit = data.find('p').get_text()

                else:
                    period =  data.find('p').get_text()      

            for detail_index,detail in enumerate(temp.find_all('div',attrs = {'class' : 'review-info'})): 
                
                if detail_index == 0 :
                        monthly_interest = detail.get_text()
                elif detail_index == 1 :
                        redemption_interest = detail.find('p').get_text()

            scoreboard = soup.find('div', attrs = {'score-total card'})

            try: #상품의 평가가 이루어진경우
                review_counts = int(re.match('\W+(\d+)', scoreboard.find('p').get_text()).group(1))
                average_rate = float(scoreboard.find('h4').get_text())        
                rowdata = deposit_fixed(idandtype = idandtype, productname = product_name.encode('utf-8'), company = company, 
                                        interest_type = interest_type.encode('utf-8'), highest_rate = highest_rate, deposit_limit = deposit_limit.encode('utf-8'),
                                       period = period.encode('utf-8'), redemption_interest = redemption_interest.encode('utf-8'),
                                       monthly_interest = monthly_interest.encode('utf-8'), review_counts = review_counts, average_rate = average_rate)
            except: # 상품에 대한 평가가 이루어지지 않는 경우
                rowdata =  deposit_fixed(idandtype = idandtype, productname = product_name.encode('utf-8'), company = company, 
                                        interest_type = interest_type.encode('utf-8'), highest_rate = highest_rate, deposit_limit = deposit_limit.encode('utf-8'),
                                       period = period.encode('utf-8'), redemption_interest = redemption_interest.encode('utf-8'),
                                       monthly_interest = monthly_interest.encode('utf-8'), review_counts = 0 )
            try:
                session.add(rowdata)
            except:
                print 'depositfss_product_adding error',idandtype
                return False
                                    
                                                                        
        elif product_type == 'DEPOSIT': #정기적금을 크롤링하는 경우
            deposit_periodic = finda_table.deposit_periodic
            for  tag_index ,data in  enumerate(temp.find('div', attrs = {'class' : 'review-data' }).find_all('div')):
                if tag_index == 0 :
                    interest_type = data.find('p').get_text()
                                    
                elif tag_index == 1 : # 적립방식
                    deposit_type = data.find('p').get_text() 
                    
                elif tag_index == 2 : # 기간별 최고 금리                   
                    try:
                        highest_rate = float(re.match('\d.\d+',data.find('p').get_text()).group()) #금리가 실수형일경우
                    except:
                        highest_rate = float(re.match('\d+',data.find('p').get_text()).group()) # 금리가 정수형일경우

                elif tag_index ==3: #납입가능 금액
                    deposit_limit =  data.find('p').get_text()  
                    
                else : # 가능 납입기간
                    period =  data.find('p').get_text()   
                
                                    
            for detail_index,detail in enumerate(temp.find_all('div',attrs = {'class' : 'review-info'})): 
                if detail_index == 0 : #개월별 기본 금리
                    monthly_interest = detail.get_text()
                elif detail_index == 1 : # 우대사항
                    preference = detail.find('p').get_text()

            scoreboard = soup.find('div', attrs = {'score-total card'})

            try: #상품의 평가가 이루어진경우
                review_counts = int(re.match('\W+(\d+)', scoreboard.find('p').get_text()).group(1))
                average_rate = float(scoreboard.find('h4').get_text())        
                rowdata = deposit_periodic(idandtype = idandtype, productname = product_name.encode('utf-8'), company = company, 
                                        interest_type = interest_type.encode('utf-8'), deposit_type = deposit_type.encode('utf-8'),
                                        highest_rate = highest_rate, deposit_limit = deposit_limit.encode('utf-8'), period = period.encode('utf-8')
                                        ,monthly_interest = monthly_interest.encode('utf-8'),preference = preference.encode('utf-8'),
                                        review_counts = review_counts, average_rate = average_rate)
            except: # 상품에 대한 평가가 이루어지지 않는 경우
                rowdata =  deposit_periodic(idandtype = idandtype, productname = product_name.encode('utf-8'), company = company, 
                                        interest_type = interest_type.encode('utf-8'),deposit_type = deposit_type.encode('utf-8'),
                                        highest_rate = highest_rate, deposit_limit = deposit_limit.encode('utf-8'),
                                        period = period.encode('utf-8'),monthly_interest = monthly_interest.encode('utf-8'),
                                        preference = preference.encode('utf-8'),review_counts = 0 )
            try:
                session.add(rowdata)
            except:
                print 'rent_product_adding error',idandtype
                return False



        elif product_type == 'P2PINVEST': #p2p투자상품을 사용하는 경우 
            p2p_invest = finda_table.p2p_invest
            for  tag_index ,data in  enumerate(temp.find('div', attrs = {'class' : 'review-data' }).find_all('div')):
                if tag_index == 0 :
                    grade = data.find('p').get_text()
                    
                elif tag_index == 1 : # 투자수익률                  
                    try:
                        interest = float(re.match('\d.\d+',data.find('p').get_text()).group()) #금리가 실수형일경우
                    except:
                        interest = float(re.match('\d+',data.find('p').get_text()).group()) # 금리가 정수형일경우

                elif tag_index == 2: #투자기간
                    period =  data.find('p').get_text()  
                    
                elif tag_index == 3 : # 부도율                  
                    try:
                        default_rate = float(re.match('\d+',data.find('p').get_text()).group()) #부도율이 정수형일경우
                    except:
                        default_rate = float(re.match('\d.\d+',data.find('p').get_text()).group()) #부도율이 실수일경우
                
                elif tag_index == 4 : # 모집율                  
                    try:
                        target_rate = float(re.match('\d+',data.find('p').get_text()).group()) #금리가 정수일경우
                    except:
                        target_rate = float(re.match('\d.\d+',data.find('p').get_text()).group()) # 금리가 실수형일경우
                
                else : # 모집금액
                    target_str =  data.find('p').get_text()   
                    target_num = re.match('\d+.+\d',target_str).group()
                    target = int(target_num.replace(',',""))
                
            scoreboard = soup.find('div', attrs = {'score-total card'})
            try: #상품의 평가가 이루어진경우
                review_counts = int(re.match('\W+(\d+)', scoreboard.find('p').get_text()).group(1))
                average_rate = float(scoreboard.find('h4').get_text())        
                rowdata = p2p_invest(idandtype = idandtype, productname = product_name.encode('utf-8'), company = company,
                                     grade = grade.encode('utf-8'), interest = interest, period = period.encode('utf-8'),
                                     default_rate = default_rate,target_rate = target_rate, target = target,
                                     review_counts = review_counts, average_rate = average_rate)
            except: # 상품에 대한 평가가 이루어지지 않는 경우
                rowdata =  p2p_invest(idandtype = idandtype, productname = product_name.encode('utf-8'), company = company,
                                            grade = grade.encode('utf-8'), interest = interest, period = period.encode('utf-8'),
                                            default_rate = default_rate,target_rate = target_rate, target = target,
                                            review_counts = 0 )
            try:
                session.add(rowdata)
            except:
                print 'p2p_invest_adding error',idandtype
                return False

        elif product_type == 'P2PLOAN':
            p2p_rent = finda_table.p2p_rent
            for  tag_index ,data in  enumerate(temp.find('div', attrs = {'class' : 'review-data' }).find_all('div')):
                if tag_index == 0 :
                    try:
                        limit_str =  data.find('p').get_text()   
                        limit_num = re.match('\d+.+\d',limit_str).group()
                        rent_limit = int(limit_num.replace(',',""))
                    except:
                        rent_limit = 0 # 대출한도가 협의 후 결정인 경우 0으로 지정 협의후 결정인 경우가 1밖에 없기 때문에
            
                elif tag_index == 1 : # 이자율            
                    interest = data.find('p').get_text()

                elif tag_index == 2: #투자기간
                    period =  data.find('p').get_text()  
                            
                else : # 모집금액
                    rent_type = data.find('p').get_text()
            
            for detail_index,detail in enumerate(temp.find_all('div',attrs = {'class' : 'review-info'})): 
                if detail_index == 0 :
                        characteristic = detail.find('p').get_text()
                elif detail_index == 1 :
                        requirement = detail.find('p').get_text()
            
            scoreboard = soup.find('div', attrs = {'score-total card'})
            try: #상품의 평가가 이루어진경우
                review_counts = int(re.match('\W+(\d+)', scoreboard.find('p').get_text()).group(1))
                average_rate = float(scoreboard.find('h4').get_text())        
                rowdata = p2p_rent(idandtype = idandtype, productname = product_name.encode('utf-8'), company = company,
                                     rent_limit = rent_limit, interest = interest.encode('utf-8'),period = period.encode('utf-8'),
                                     characteristic = characteristic.encode('utf-8'), requirement = requirement.encode('utf-8'),
                                     rent_type = rent_type.encode('utf-8'),review_counts = review_counts, average_rate = average_rate)
            except: # 상품에 대한 평가가 이루어지지 않는 경우
                rowdata = p2p_rent(idandtype = idandtype, productname = product_name.encode('utf-8'), company = company,
                                     rent_limit = rent_limit, interest = interest.encode('utf-8'),period = period.encode('utf-8'),rent_type = rent_type.encode('utf-8'),
                                     characteristic = characteristic.encode('utf-8'), requirement = requirement.encode('utf-8'),
                                     review_counts = 0)
            try:
                session.add(rowdata)
            except:
                print 'p2p_loan_adding error',idandtype
                return False
        

    

        reviews_box = soup.find_all('div', attrs = {'class':'review-all-item'}) # 상품에 달린 댓글 
        if len(reviews_box) > 0: # 댓글이 달린경우 댓글을 sql data base에 저장함
            for i in reviews_box:
                for num,j in  enumerate(i.find('ul', attrs = {'class': 'score-sub'}).find_all('li')):
                    satis_point =  int(re.match('\W+(.+)',j.get_text().encode('utf-8')).group(1)) #개별항목 점수
                    if num == 0 :
                        interest_sat = satis_point
                    elif num == 1:
                        online_sat = satis_point
                    elif num == 2:
                        prof_sat = satis_point
                    else :
                        service_sat = satis_point
                total_rating = (interest_sat + online_sat + prof_sat + service_sat) / 4.0 #합계 평균 점수 
                review = i.find('div',attrs = {'class': 'review-item-text'}).find('p').get_text() #댓글
                date = i.find('h6').get_text() # 댓글 작성 날짜 
                reviewrow = reviews(date = date.encode('utf-8'), idandtype = idandtype, total_rating = total_rating, 
                                    interest_sat = interest_sat, online_sat = online_sat, prof_sat = prof_sat,
                                    service_sat = service_sat,review = review.encode('utf-8'))
                try:
                    session.add(reviewrow)
                except:
                    print 'comments_error',idandtype
                    continue
        
        try:        
            session.commit()
        except Exception as e:
            print e 
            print 'session commit error',idandtype
            return False
        session.close()

if __name__ == '__main__':
    crawling_object = Finda_crawler()
    crawling_object.deposit_fixed()
    crawling_object.deposit_periodic()
    crawling_object.p2p_rent()
    crawling_object.p2p_invest()
    crawling_object.mortgage_rent()