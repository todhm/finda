## Synopsis
금융상품 검색 사이트 핀다에 올라온 정보를 바탕으로 서비스에서 직접 제공하지 않는 정보를 가공해 일반 소비자와 금융 기업에게 필요한 인사이트 도출.
        

## File Description
* finda_table.py: 데이터 분석에 사용될 SQL schema를 orm 형식으로 정리해놓은 파일
* finda_crawler.py: ubuntu환경에서 필요한 데이터를 크롤링하는데 쓰는 파일
* Finda_Crawling.ipynb:로컬 환경에서 필요한 데이터를 크롤링하는 방법을 정리해놓은 파일
* Finda_analysis_deposit.ipynb: 정기예금 상품과 정기 적금 상품에 대한 분석을 진행한 ipython notebook파일
* Finda_analysis_p2p.ipynb: p2p 투자상품에 대한 분석을 진행한 ipython notebook 
* Finda_analysis_rentandmort.ipynb: 주택담보대출 상품과 전월세 대출 상품에 대한 분석을 진행한 파일
* mort_df.csv: 주택담보대출 상품 데이터를 정리한 csv파일
* rent_df.csv: 전월세대출 상품 데이터를 정리한 csv파일
* mort_reviews.csv: 주탁담보대출 상품에 대한 리뷰를 정리한 csv파일
* rent_reviews.csv: 전월세대출 상품에 대한 리뷰를 정리한 csv파일
* dp_df.csv: 정기적금 상품의 데이터를 정리한 파일
* df_df.csv: 정기예금 상품의 데이터를 정리한 파일
* dp_reviews.csv: 정기적금 상품에 대한 리뷰를 정리한 csv파일
* p2p_inv_df.csv: P2P 투자 상품의 데이터를 정리한 파일
* p2p_inv_reviews.csv: P2P 투자 상품에 대한 리뷰를 정리한 csv파일

## 프로젝트 진행 과정
* Finda_Crawling -> Finda_analysis_rentandmort -> Finda_analysis_deposit -> Finda_analysis_p2p순서로 진행

## Prerequsite
* Python 2.7
* Ipython Notebook 
* MYSQL on ubuntu server
* Konlpy(Korean Neuro-Linguistic Programming of Python) (http://konlpy.org/en/v0.4.4/)

## API Reference
* 핀다(https://www.finda.co.kr/)
