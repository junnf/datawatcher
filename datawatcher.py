#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import torndb as mysqldb
import traceback
import os
import sys
import sched

from setting.setting import host, dbname, dbuser, password 
#from setting.setting import recommend_member

from sendcloud import sendemail
from sendcloud import sendmessage

class Db(object):
    
    def __init__(self):
        
        try:
            self.db = mysqldb.Connection(host,dbname,dbuser,password)
        except Exception, e:
            print traceback.print_exc()
            return

    def membersmall5(self,exist_recommend):
        '''
          需要重新考虑完全没有推荐的人
          _db_data2部分
        '''
        try:  
            _db_data1 = self.db.query('select name,telephone,email      \
                from customer_member_t where is_open_recommend = 1      \
                and resume_review_status=10 and member_id in            \
                (select customer_id from bussiness_member_recommend     \
                group by customer_id having count(*) <= 5) order by member_id;')

            _db_data2 = self.db.query('select name,email,telephone from \
                customer_member_t where member_id not in \
                (select customer_id from bussiness_member_recommend )   \
                and  is_open_recommend = 1 and resume_review_status=10;')
        except Exception, e:
            print traceback.print_exc()
            return

        if exist_recommend == 1:
            return _db_data1
        elif exist_recommend == 0:
            return _db_data2

    def memberx3d5(self):
        '''
          invitation < 3, recommend > 5
        '''
        try:
            _db_data = self.db.query('select customer_id from bussiness_member_recommend where  \
            customer_id in (select customer_id from positioninv group by customer_id     \
            having count(*) < 3) group by customer_id having count(*) >= 5;')
            #print _db_data
            for x in _db_data:
                print self.db.query('select * from bussiness_member_recommend where customer_id = ' + str(x['customer_id']))
                print '\n'

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
            _db_data = self.db.query('select customer_id \
                from positioninv group by customer_id having ')
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
            where status = 2 and UNIX_TIMESTAMP() - completed_at     \
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
            and UNIX_TIMESTAMP() - created_at > 259200;')
            
            _db_data = self.db.query('select * from positioninv \
                where status = 2 and \
                UNIX_TIMESTAMP() - completed_at > 259200;') 
        except Exception, e:
            print traceback.print_exc()
            return
        return _db_data

    def c_extremity_no_feedback(self):
        '''
            sieve (id, time, )
        '''
        try :
            #
            #_db_data = self.db.query('select inv_id, customer_id,  \ 
            #completed_at, status from positioninv where status = 0')
            _db_data1 = self.db.query('select inv_id, customer_id   \
            from positioninv where status = 0 and UNIX_TIMESTAMP()  \
            - completed_at > 172800  ')

        except Exception, e:
            print traceback.print_exc()
            return
        return _db_data1

    def c_extremity_no_feedback_close_recommend(self):

        '''
            72小时无法处理将这个邀请置为过期，关闭此人推荐
        '''
        try :
            _db_data - self.db.query('select inv_id,customer_id,from positioninv \
                where status = 0 and UNIX_TIMESTAMP() - completed_at > 259200')
        
        except Exception, e:
            print traceback.print_exc()
            return
        
        return _db_data
            
def test_1():
    db = Db()
    member1 = db.memberx3d5()
    for x in member1:
        
      member2 = dm.memberx3x5()
    

def test_danger():
    db = Db() 
    member0 = db.membersmall5(0)
    member1 = db.membersmall5(1)
    for y in member0: 
        sendemail.get_params(emailto = str(x['email'])),
        emailfrom = 'datacenter@sendcloud.org',
        fromname = 'DataCenter',
        subject = '请修改条件，修改职位描述'
        content = x['name']+'你好: 你的职位推荐有问题,请修改'
    
    for x in member1:
        sendemail.get_params(emailto = str(x['email'])),
        emailfrom = 'datacenter@sendcloud.org',
        fromname = 'DataCenter',
        subject = '请修改条件，修改职位描述'
        content = x['name']+'你好: 你的职位推荐有问题,请修改' 
   
    member2 = db.memberx3d5()
    
       # sendemail.get_params(emailto = str())    

def test():
    db = Db()
    #db.memberx3d5()
    mem0 = db.membersmall5(0)
    mem1 = db.membersmall5(1)
    for x in mem0:
        _name = x['name'].encode('utf-8')
        _email = x['email'].encode('utf-8')
        _tel = x['telephone'].encode('utf-8')


def task():
    
    db = Db()
    member1 = db.membersmall5()
    #continue recommend member1
    #continue_recommend(member1)
    continue_member1 = db.membersmall5()
    for n1_member in continue_member1:
        print n1_member
        '''
        #    notify module
        '''
        #notify

    member2 = db.memberx3d5()
    for n2_member in member2:
        print n2_member
        '''
       #     无法解决
        '''
    member3 = db.memberx3x5()
    #continue_recommend(member3)

    member4 = db.c_extremity_no_feedback()

    member5 = db.b_extremity_no_feedback()
        #notify b-member
    #_now_time2 = time.time()
    
if __name__ == '__main__':
  
  # db = mysqldb.Connection(host,dbname,dbuser,password)
 #   test()
  #   task start
    test()

 
