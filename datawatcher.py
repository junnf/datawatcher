#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import torndb as mysqldb
import traceback
import os
import sys
import sched
from setting.setting import host, dbname, dbuser, password 

class Db():
    
    def __init__(self):
        try:
            db = mysqldb.Connection(host,dbname,dbuser,password)
        except Exception, e:
            print traceback.print_exc()
            
    def membersmall5(self):
        try:  
            _db_data = self.db.query('select * from bussiness_member_recommend  \
            group by customer_id having count(*) <= 5')
        except Exception, e:
            print traceback.print_exc()
            return
        return _db_data
        
    def memberx3d5(self):
        '''
          invitation < 3, recommend > 5
        '''
        try:
            _db_data = self.db.query('select customer_id from bussiness_member_recommend where  \
            customer_id in (select customer_id from positioninv group by customer_id     \
            having count(*) < 3) group by customer_id having count(*) >= 5;')
        except Exception, e:
            print traceback.print_exc()
            return
        return _db_data
 
    def memberx3x5(self):
        try:
            _db_data = self.db.query('select customer_id from bussiness_member_recommend where  \
            customer_id in (select customer_id from positioninv group by customer_id     \
            having count(*) < 3) group by customer_id having count(*) <5;')
        except Exception, e:
            print traceback.print_exc()
            return
        return _db_data

    def nofeedbackintime(self):
        try :  
            _db_data = self.db.query('select customer_id from positioninv group by customer_id having ')
        except Exception, e:
            print traceback.print_exc()
            return
        return _db_data

    def c_extremity_no_feedback(self):
        '''
            sieve (id, time, )
        '''
        try :
            _db_data = self.db.query('select inv_id, customer_id, created_at, status  \
            from positioninv where status = 0')
        except Exception, e:
            print traceback.print_exc()
            return
        return _db_data

def task():
    
    db = Db()
    member1 = db.membersmall5()
    #continue recommend member1
    #continue_recommend(member1)
    continue_member1 = db.membersmall5()
    for n1_member in continue_member1:
        '''
            notify module
        '''
        #notify

    member2 = db.memberx3d5()
    for n2_member in member2:
        '''
            无法解决
        '''
    member3 = db.memberx3x5()
    #continue_recommend(member3)

    #172800s = 48h
    member4 = db.c_extremity_no_feedback()
    _now_time = time.time()
    for _mem in member4:
      #created_at is time?
        if abs((_mem['created_at'] + 172800) - _now_time) <= 3600:
            #notify
            pass
        if  abs((_mem['created_at'] + 259200) - _now_time) <= 3600:
            #标记过期

            #关闭人员推荐


if __name__ == '__main__':
#   task start
    task()

 
