# -*- coding:utf-8 -*-
#Author: allisnone
import csv
import random
import os,sys,time
import paramiko
# pip install paramiko --trusted-host mirrors.aliyun.com
"""
一个基于thread和queue的线程池，以任务为队列元素，动态创建线程，重复利用线程，
通过close和terminate方法关闭线程池。
"""
from zthreads.threadpools.threadpools import Threadpools
from zthreads.comm.logger import initial_logger
from zthreads.comm.fileoperation import write2csv,write_datas_2csv,read_csv_dict,read_csv_list,Sftpclient
#logger = initial_logger(logfile='thread.log',errorfile='thread_error.log',logname='thread')

def sftp_upload_file(thread_name,seq,host,username,password='',port=22,private_key_file='',logger=None,result_type='list',timeout=10):
    """
    根据需要进行的回调函数，默认不执行。
    :param host: str, ssh host IP
    :param user: str, ssh login username
    :param password: str, ssh login username
    :param logger: logger
    :param result_type: str, type of the result
    :return: result, dict or list
    """
    #result = [host,username,password,port]
    try:
        #sftp = Sftpclient(host=host,port=port,username=username,password=password,private_key_file=private_key_file,timeout=10)
        sftp = Sftpclient(host=host,port=port,username=username,password=password,private_key_file=private_key_file,timeout=10)
        info = sftp.upload(local_path='/root/ssh_threadpool/abc.txt',remote_path='/root/abc.txt')
        if logger!=None: 
            logger.info('host:%s  hostname:%s'%(host,info))
            logger.info("第%s个任务调用了线程 %s，并打印了这条信息！" % (seq+1, thread_name))
        else:
            print('host:%s  hostname:%s'%(host,info))
            print("第%s个任务调用了线程 %s，并打印了这条信息！" % (seq+1, thread_name))
        sftp.close()
        if result_type=='dict':
            return {'host':host,'username':username,'password':password,'port': port, 'data': info}
        else:
            return [host,username,password,port,info]
    except Exception as e:
        if logger!=None:
            print('Connect the server [{0}] exception: {1}'.format(host,e))
        else:
            print('Connect the server [{0}] exception: {1}'.format(host,e))
        if result_type=='dict':
            return {'host':host,'username':username,'password':password,'port': port, 'data': ''}
        else:
            return [host,username,password,port,'']
        


def ssh_fun(thread_name,seq,host,username,password='',port=22,logger=None,result_type='list',private_key_file='',timeout=10):
    """
    根据需要进行的回调函数，默认不执行。
    :param host: str, ssh host IP
    :param user: str, ssh login username
    :param password: str, ssh login username
    :param logger: logger
    :param result_type: str, type of the result
    :return: result, dict or list
    """
    #result = [host,username,password,port]
    try:
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password,timeout=10)
        #stdin, stdout, stderr = ssh.exec_command('hostname')
        stdin, stdout, stderr = ssh.exec_command('free -m')
        info = stdout.read().decode().strip()
        """
        #sftp = Sftpclient(host=host,port=port,username=username,password=password,private_key_file=private_key_file,timeout=10)
        sftp = Sftpclient(host=host,port=port,username=username,password=password,private_key_file=private_key_file,timeout=10)
        info = sftp.cmd('hostname')
        if logger!=None: 
            logger.info('host:%s  hostname:%s'%(host,info))
            logger.info("第%s个任务调用了线程 %s，并打印了这条信息！" % (seq+1, thread_name))
        else:
            print('host:%s  hostname:%s'%(host,info))
            print("第%s个任务调用了线程 %s，并打印了这条信息！" % (seq+1, thread_name))
        sftp.close()
        if result_type=='dict':
            return {'host':host,'username':username,'password':password,'port': port, 'data': info}
        else:
            return [host,username,password,port,info]
    except Exception as e:
        if logger!=None:
            print('Connect the server [{0}] exception: {1}'.format(host,e))
        else:
            print('Connect the server [{0}] exception: {1}'.format(host,e))
        if result_type=='dict':
            return {'host':host,'username':username,'password':password,'port': port, 'data': ''}
        else:
            return [host,username,password,port,'']
 
def adding_ssh_queue(pool,action,callback,ssh_data_file='ssh_iplist.txt',encoding='utf-8'):
    """
    根据需要进行的回调函数，默认不执行。
    :param pool: 线程池Object
    :param action: action函数名称
    :param callback: callback函数名称
    :param ssh_data_file: str, file with ssh datas
    :return: bool
    """
    ip_datas = read_csv_dict(file=ssh_data_file,encoding=encoding)
    print('ip_datas=',ip_datas)
    i = 0
    for data in ip_datas:
        host = data['host']
        username = data['username']
        password = data ['password']
        port = data ['port']
        if port:
            pass
        else:
            port = 22
        if host and username and password:
            if pool.logger:
                pool.put(ssh_fun, (i,host,username,password,port,pool.logger,), callback)
            else:
                pool.put(ssh_fun, (i,host,username,password,port,), callback)
        else:
            if pool.logger:
                logger.error("One of host={0}, username={1} or password={2} port={3} is invalid".format(host,username,password,port))
            else:
                print("One of host={0}, username={1} or password={2} port={3} is invalid".format(host,username,password,port))
        i = i + 1
    return

    
def callback(status, result, logger=None):
    """
    根据需要进行的回调函数，默认不执行。
    :param status: action函数的执行状态
    :param result: action函数的返回值
    :param logger: logger
    :return:
    """
    print('callback status={0},result={1}'.format(status,result))
    if status:
        if result:
            # doing something here
            if isinstance(result,str):
                result = [result]
            elif isinstance(result,list):
                pass
            else:
                pass
            write2csv(result)
            if logger!=None:
                logger.info('Executed callback status={0},result={1}'.format(status,result))
            else:
                print('Executed callback status={0},result={1}'.format(status,result))
        else:
            pass
    else: 
        pass
    return 

 
 
def action(thread_name,arg,host,user,password,logger=None):
    """
    真实的任务定义在这个函数里
    :param thread_name: 执行该方法的线程名
    :param arg: 该函数需要的参数
    :param logger: logger
    :return:
    """
    # 模拟该函数执行了0.1秒
    time.sleep(0.1)
    print("第%s个任务调用了线程 %s，并打印了这条信息！" % (arg+1, thread_name))
    result = {'values1': random.random()}
    result = ssh_fun(host,user,password,logger=None)
    return result
 
# 调用方式
if __name__ == '__main__':
    sftp_upload_file(thread_name='thread-1',seq=1,host='172.17.33.23',port=22,username='root',password='',private_key_file='/root/.ssh/id_rsa')
    # 创建一个最多包含5个线程的线程池
    curr_path = 'C:\\Users\\zhangguoxin\\git\\mytrader\\mytrader'
    #logfile=os.path.join(curr_path,'./ztrader/logs/thread.log')
    logfile = 'thread.log'
    logger = initial_logger(logfile,errorfile='thread_error.log',logname='thread')
    logger.info('start treadpool test')
    #columns = ['result']
    columns = ['host','username','password','port','result']
    write2csv(data=columns,file='result.csv',encoding='utf-8',logger=None,clear=True)
    pool = Threadpools(5,max_task_num=None,logger=logger)
    # 创建100个任务，让线程池进行处理
    #for i in range(100):
    #    pool.put(action, (i,), callback)
    #ssh_data_file=os.path.join(curr_path,'./ztrader/conf/ssh_iplist.txt')
    ssh_data_file = 'ssh_iplist.txt'
    adding_ssh_queue(pool,action,callback,ssh_data_file)
    # 等待一定时间，让线程执行任务
    time.sleep(3)
    print("-" * 50)
    print("\033[32;0m任务停止之前线程池中有%s个线程，空闲的线程有%s个！\033[0m"
          % (len(pool.generate_list), len(pool.free_list)))
    # 正常关闭线程池
    pool.close()
    print("任务执行完毕，正常退出！")
    # 强制关闭线程池
    # pool.terminate()
    # print("强制停止任务！")

