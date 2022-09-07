# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 19:20:18 2022

@author: archa
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



#mysql
sqlalchemy_db_url="mysql://root:avina@127.0.0.1:3306/customer"

engine= create_engine(sqlalchemy_db_url)

#sessionlocal is database session
sessionlocal= sessionmaker(autocommit=False,bind=engine)

Base= declarative_base()
