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
#from zthreads.comm.fileoperation import write2csv,write_datas_2csv,read_csv_dict,read_csv_list,Sftpclient
from zthreads.comm.http_requests import write2csv,write_datas_2csv,get_urls_from_web,get_urls_from_file,urls_exception,Httprequests
#logger = initial_logger(logfile='thread.log',errorfile='thread_error.log',logname='thread')


def aswg_url_request(url,headers=None,proxy_host='None',proxy_port=8080,proxy_username=None,proxy_password=None,logger=None,thread=''):
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
        #headers = {
            #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
            #'Host': '',
            #'Referer': ''
        #}
        req = Httprequests(url,headers=headers,logger=logger)
        #req.set_proxy(proxy_host=proxy_host,prox_port=prox_port,proxy_username=proxy_username,proxy_password=proxy_password)
        #req.set_proxy(proxy_host=proxy_host,prox_port='8080',proxy_username='se1',proxy_password='Firewall1')
        result = req.url_request(block_info='访问的URL中含有安全风险',encoding='utf-8',verify=False,retry_once=False,timeout=(15,30),thread=thread)
        return result
    except Exception as e:
        return []

def callback(status, result, logger=None):
    """
    根据需要进行的回调函数，默认不执行。
    :param status: action函数的执行状态
    :param result: action函数的返回值
    :param logger: logger
    :return:
    """
    #print('callback status={0},result={1}'.format(status,result))
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
                pass#print('Executed callback status={0},result={1}'.format(status,result))
        else:
            pass
    else: 
        pass
    return 

 
def action(thread_name,arg,url,logger=None,headers=None,proxy_host='None',proxy_port=8080,proxy_username=None,proxy_password=None,):
    """
    真实的任务定义在这个函数里
    :param thread_name: 执行该方法的线程名
    :param arg: 该函数需要的参数
    :param logger: logger
    :return:
    """
    # 模拟该函数执行了0.1秒
    time.sleep(0.1)
    #print("第%s个任务调用了线程 %s，并打印了这条信息！" % (arg+1, thread_name))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'Connection': 'close',#'keep-alive'  #close' 原生http无状态
        'Host': url.replace('http://','').replace('https://','')
        #'Referer': url
    }
    #print(headers)
    result = aswg_url_request(url,headers=headers,proxy_host=proxy_host,proxy_port=proxy_port,proxy_username=proxy_username,proxy_password=proxy_password,logger=logger,thread=thread_name)
    if logger:
        logger.info('i={0}, all_thread_num={1}, free_thread_num={2}'.format(arg,len(pool.generate_list), len(pool.free_list)))
    return result
 
def adding_url_request_queue(pool,action,callback,urls=[],url_file='urls.txt',url_column=0,encoding='utf-8'):
    """
    根据需要进行的回调函数，默认不执行。
    :param pool: 线程池Object
    :param action: action函数名称
    :param callback: callback函数名称
    :param ssh_data_file: str, file with ssh datas
    :return: bool
    """
    if urls:
        pass
    else:
        urls = get_urls_from_file(from_file=url_file,url_index=url_column,spliter=',',pre_www='www.',encoding='utf-8',default_protocol='http')
    i = 0
    for url in urls:
        if not url:
            continue
        else:
            if pool.logger:
                pool.put(action, (i,url,pool.logger,), callback)
            else:
                pool.put(action, (i,url,), callback)
        i = i + 1

    return

    

 
# 调用方式
if __name__ == '__main__':
    #sftp_upload_file(thread_name='thread-1',seq=1,host='172.17.33.23',port=22,username='root',password='',private_key_file='/root/.ssh/id_rsa')
    # 创建一个最多包含5个线程的线程池
    print("-" * 50)
    print('Start url thread pool test...')
    pool_num = 1000
    curr_path = 'C:\\Users\\zhangguoxin\\git\\mytrader\\mytrader'
    #logfile=os.path.join(curr_path,'./ztrader/logs/thread.log')
    logfile = 'thread.log'
    logger = initial_logger(logfile,errorfile='thread_error.log',logname='thread')
    logger.info('start treadpool test')
    #columns = ['result']
    columns = ['host','username','password','port','result']
    write2csv(data=columns,file='result.csv',encoding='utf-8',logger=logger,clear=True)
    pool = Threadpools(pool_num,max_task_num=None,logger=logger)
    # 创建100个任务，让线程池进行处理
    #for i in range(100):
    #    pool.put(action, (i,), callback)
    #ssh_data_file=os.path.join(curr_path,'./ztrader/conf/ssh_iplist.txt')
    url_file = 'urls.txt'
    url_file = 'rank_1000.txt'
    url_column = 1
    urls = get_urls_from_file(from_file=url_file,url_index=url_column,spliter=',',pre_www='www.',encoding='utf-8',default_protocol='http')
    adding_url_request_queue(pool,action,callback,urls=urls, url_file='',url_column=url_column,encoding='utf-8')
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

