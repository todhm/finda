import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, CHAR, Date, String, Time, Index, DateTime, TIMESTAMP, func, or_
from sqlalchemy.dialects.mysql import INTEGER, BIT, TINYINT, TIME, DOUBLE, TEXT,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker

server = '127.0.0.1'
connection_string = 'mysql+mysqldb://root:MYSQLPassword@{}:3306/findas'.format(server)
engine = create_engine(connection_string, pool_recycle = 3600, encoding='utf-8')
Base = declarative_base()

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, CHAR, Date, String, Time, Index, DateTime, TIMESTAMP, func, or_
from sqlalchemy.dialects.mysql import INTEGER, BIT, TINYINT, TIME, DOUBLE, TEXT,TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
server = 'ec2-54-149-149-184.us-west-2.compute.amazonaws.com'
connection_string = 'mysql+mysqldb://root:io596847@{}:3306/findas'.format(server)
engine = create_engine(connection_string, pool_recycle = 3600, encoding='utf-8')

Base = declarative_base()

class rent(Base):
    __tablename__ = 'rent'
    idandtype = Column(String(15), primary_key = True, nullable = False, autoincrement = False)
    productname = Column(String(50), nullable= False, default = None)
    interest_type = Column(String(20),nullable = False, default = None)
    company = Column(String(50), nullable= False, default = None)
    lowest_rate = Column(DOUBLE, nullable= False, default = None)
    highest_rate = Column(DOUBLE, nullable= False, default = None)
    last_month_interest = Column(DOUBLE, nullable = True, default = None )
    maximum_period = Column(INTEGER, nullable = True, default = None )
    preference = Column(TEXT, nullable = True, default = None)
    redemption_fee = Column(TEXT, nullable = True, default = None)
    related_fee = Column(TEXT, nullable = True, default = None)
    review_counts = Column(INTEGER, nullable = False, default = 0)
    average_rate = Column(DOUBLE, nullable = True, default = None)
    
class deposit_fixed(Base):
    __tablename__ = 'deposit_fixed'
    idandtype = Column(String(15), primary_key = True, nullable = False, autoincrement = False)
    productname = Column(String(50), nullable = False, default = None)
    company = Column(String(50), nullable= False, default = None)
    interest_type = Column(String(15),nullable = False, default = 'simple')
    highest_rate = Column(DOUBLE,nullable = False, default = None)
    deposit_limit = Column(String(15), nullable = True, default = None)
    period = Column(String(20), nullable = True, default = None)
    redemption_interest = Column(TEXT, nullable = True, default = None)
    monthly_interest = Column(TEXT,nullable = True, default = None)
    review_counts = Column(INTEGER, nullable = True, default = 0)
    average_rate = Column(DOUBLE, nullable = True, default = None)
    
class deposit_periodic(Base):
    __tablename__ = 'deposit_periodic'
    idandtype = Column(String(15), primary_key = True, nullable = False, autoincrement = False)
    productname = Column(String(50), nullable = False, default = None)
    company = Column(String(50), nullable= False, default = None)
    interest_type = Column(String(15),nullable = False, default = 'simple')
    deposit_type = Column(String(15),nullable = False, default = None)
    highest_rate = Column(DOUBLE,nullable = False, default = None)
    deposit_limit = Column(String(15), nullable = True, default = None)
    period = Column(String(20), nullable = True, default = None)
    monthly_interest = Column(TEXT,nullable = True, default = None)
    preference = Column(TEXT,nullable = True, default = None)
    review_counts = Column(INTEGER, nullable = True, default = 0)
    average_rate = Column(DOUBLE, nullable = True, default = None)

class p2p_invest(Base):
    __tablename__ = 'p2p_invest'
    idandtype = Column(String(15), primary_key = True, nullable = False, autoincrement = False)
    productname = Column(String(50), nullable = False, default = None)
    company = Column(String(50), nullable= False, default = None)
    grade = Column(String(15),nullable = False, default = None)
    interest = Column(DOUBLE,nullable = False, default = None)
    period = Column(String(15), nullable = True, default = None)
    default_rate = Column(DOUBLE, nullable = True, default = None)
    target_rate = Column(DOUBLE,nullable = False, default = None)
    target = Column(INTEGER,nullable = False, default = None)
    review_counts = Column(INTEGER, nullable = True, default = 0)
    average_rate = Column(DOUBLE, nullable = True, default = None)
    
    
class p2p_rent(Base):
    __tablename__ = 'p2p_rent'
    idandtype = Column(String(15), primary_key = True, nullable = False, autoincrement = False)
    productname = Column(String(50), nullable = False, default = None)
    company = Column(String(50), nullable= False, default = None)
    rent_limit = Column(INTEGER, nullable =False, default = None)
    interest = Column(String(20),nullable = False, default = None)
    period = Column(String(15), nullable = False, default = None)
    rent_type = Column(String(20), nullable = False, default = None)
    characteristic = Column(TEXT,nullable = True, default = None)
    requirement = Column(TEXT,nullable = False, default = None)
    review_counts = Column(INTEGER, nullable = True, default = 0)
    average_rate = Column(DOUBLE, nullable = True, default = None)


class reviews(Base):
    __tablename__ = 'reviews'
    reviewid = Column(INTEGER, nullable = False, autoincrement = True, primary_key = True)
    date = Column(String(15), nullable = False, autoincrement = False, primary_key = False)
    idandtype = Column(String(15), nullable = False, autoincrement = False)
    total_rating = Column(DOUBLE,nullable = False, default = None)
    interest_sat = Column(INTEGER,nullable = False, default = None)
    online_sat = Column(INTEGER, nullable = False, default = None)
    prof_sat = Column(INTEGER, nullable = False, default = None)
    service_sat = Column(INTEGER, nullable = False, default = None)
    review = Column(TEXT,nullable = True, default = None)
    