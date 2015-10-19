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

if __name__ == '__main__':
    pass
    
     

 
