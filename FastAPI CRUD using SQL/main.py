# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 19:19:38 2022

@author: archa
"""

from fastapi import FastAPI, Query, Depends
from typing import Optional,List
from pydantic import BaseModel
from sqlalchemy import Column,String, Integer,Boolean
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import json


from database import Base,engine,sessionlocal


#model
class Users(Base):
    __tablename__="customers"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50))
    email=Column(String(50), unique=True)
    password=Column(String(50))
    
    
Base.metadata.create_all(bind=engine)
app=FastAPI()
 
def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()
    
        
 #schema is used to retrieve data from the table if it any formaat
   
class custm_schema(BaseModel):
   
    name:str
    email:str
    
    class Config:
        orm_mode=True                            #its dictionary or json format
        
class CustCreateSchema(custm_schema):
    password:str
        
@app.get('/customers', response_model=List[CustCreateSchema])
def get_customers(db:Session=Depends(get_db)):
    return db.query(Users).all()

@app.post("/customers",response_model=custm_schema)
def post_cust(customer:CustCreateSchema,db:Session=Depends(get_db)):
    u = Users(name=customer.name,email=customer.email,password=customer.password)
    db.add(u) 
    db.commit()
    return u
    
@app.put("/customers/{cust_id}",response_model=custm_schema)
def update_cust(cust_id:int,customer:CustCreateSchema,db:Session=Depends(get_db)):
#    try:
        u=db.query(Users).filter(Users.id==cust_id).first()
        u.name=customer.name
        u.email=customer.email
        db.add(u)
        db.commit()
        return u 
 #   except:
 #       return HTTPException(status_code=404,details="customer not found")
    
@app.delete("/customers/{cust_id}",response_class=JSONResponse)
def delete_cust(cust_id:int,db:Session=Depends(get_db)):
#    try:
        u=db.query(Users).filter(Users.id==cust_id).first()
        db.delete(u)
        return {f"user of id {cust_id} has been deleted":True}
#   except:
#       return HTTPException(status_code=404,details="customer not found")
         
        
        
        
 #this below line use to convert model into tables in database


