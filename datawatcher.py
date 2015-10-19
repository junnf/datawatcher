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

    def b_extremity_no_feedback(self):
        try:
            _db_data = self.db.query('select bussiness_id   \
                from bussiness_member_recommend             \
                where status = 1 group by bussiness_id      \
                having count(*) > 30 order by bussiness_id')
            
        except Exception, e:
            print traceback.print_exc()
            return

        return _db_data
    
    def b_extremity_no_feedback_del_recommend(self):
        '''
            7天未处理 删除推荐
        '''
        try: 
            _db_data = self.db.query('select * from        \
            bussiness_member_recommend where status = 1    \ 
            and UNIX_TIMESTAMP() - created_at > 604800;')
            
            _db_data1 = self.db.query('select * from positioninv     \
                where status = 2 and UNIX_TIMESTAMP() - completed_at \
                > 604800; ')
        except Exception, e:
            print traceback.print_exc()
            return
        
        return _db_data

    def b_extremity_no_feedback_stop_recommend(self):
        '''
            三天没有操作，停止推荐，并且通知
        '''
        try:
            _db_data = self.db.query('select * from      \
            bussiness_member_recommend where status = 1  \
            and UNIX_TIMESTAMP() - created_at > 259200;  \
            ')
            _db_data = self.db.query('select * from positioninv where \  
            status = 2 and UNIX_TIMESTAMP() - completed_at > 259200;  \
                ')
    def c_extremity_no_feedback(self):
        '''
            sieve (id, time, )
        '''
        try :
            #
            _db_data = self.db.query('select inv_id, customer_id,  \ 
            completed_at, status from positioninv where status = 0')
        except Exception, e:
            print traceback.print_exc()
            return
        return _db_data

def test():
    pass

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
    for _mem1 in member4:
      #created_at is time?
        if abs((_mem['completed_at'] + 172800) - time.time()) <= 3600:
            #notify
            pass
        if  abs((_mem['completed_at'] + 259200) - time.time()) <= 3600:
            #标记过期
            pass
            #关闭人员推荐

    member5 = db.b_extremity_no_feedback()
        #notify b-member
    #_now_time2 = time.time()
    for _mem2 in member5:
        if abs((_mem['']))

if __name__ == '__main__':
#   task start
    task()

 
