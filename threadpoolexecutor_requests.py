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
from concurrent.futures import ThreadPoolExecutor,as_completed,wait,ALL_COMPLETED,FIRST_COMPLETED,FIRST_EXCEPTION


def aswg_url_request(url_data):
    """
    根据需要进行的回调函数，默认不执行。
    :param url_data: dict type
    :return: result, dict 
    """
    try:
        #print('url_data_porxy=',url_data['proxy'])
        #proxy={'https': 'http://ts2:Firewall1@172.17.33.23:8080', 'http': 'http://ts2:Firewall1@172.17.33.23:8080'}
        proxy = None
        try:
            proxy = url_data['proxy']
        except Exception as e:
            print('proxy_exception: {0}'.format(e))
        req = Httprequests(url_data['url'],headers=url_data['headers'],logger=url_data['logger'],proxy=proxy)
        if proxy==None:
            req.set_proxy(proxy_host=url_data['proxy_host'],proxy_port=url_data['proxy_port'],proxy_username=url_data['proxy_username'],proxy_password=url_data['proxy_password'])
        #req.set_proxy(proxy_host=proxy_host,proxy_port='8080',proxy_username='se1',proxy_password='Firewall1')
        result = req.url_request(block_info='访问的URL中含有安全风险',encoding='utf-8',verify=False,retry_once=False,timeout=url_data['timeout'],thread=url_data['thread'])
        return {'status':True,'result':result,'result_file': url_data['result_file']}
    except Exception as e:
        if url_data['logger']!=None:
            url_data['logger'].error('aswg_url_request exception: {0}'.format(e))
        return {'status':False,'result':[],'result_file': url_data['result_file']}

def callback(future):
    """
    根据需要进行的回调函数，默认不执行。
    :param future: action函数的返回值--future
    :return:
    """
    data = future.result()
    status = data['status']
    print(data['result_file'],data['result'])
    if status:
        if data['result']:
            # doing something here
            write2csv(data['result'],file=data['result_file'])
            if True:#logger!=None:
                pass#logger.info('Executed callback status=,result={0}'.format(data['result']))
            else:
                pass#print('Executed callback status={0},result={1}'.format(status,result))
        else:
            pass
    else: 
        pass
    return 

 
#def action(arg,url,logger=None,headers=None,proxy_host='None',proxy_port=8080,proxy_username=None,proxy_password=None):
def action(url_data):
    
    """
    真实的任务定义在这个函数里
    :param thread_name: 执行该方法的线程名
    :param arg: 该函数需要的参数
    :param logger: logger
    :return:
    """
    # 模拟该函数执行了0.1秒
    time.sleep(0.1)
    #print("第%s个任务调用了线程 %s，并打印了这条信息！" % (arg+1, url))
    return aswg_url_request(url_data)
 
def adding_url_request_queue(pool,action,callback,urls=[],url_file='urls.txt',url_column=0,encoding='utf-8',logger=None):
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
        print(url)
        if not url:
            continue
        else:
            task = pool.submit(action,(i,url))#.add_done_callback(callback)
            task.add_done_callback(callback)
        i = i + 1

    return

 
# 调用方式
if __name__ == '__main__':
    #sftp_upload_file(thread_name='thread-1',seq=1,host='172.17.33.23',port=22,username='root',password='',private_key_file='/root/.ssh/id_rsa')
    # 创建一个最多包含5个线程的线程池
    pool_num = 32
    print("-" * 50)
    print('Start ThreadPoolExecutor test for ASWG Proxy, pool_num={}...'.format(pool_num))
    curr_path = 'C:\\Users\\zhangguoxin\\git\\mytrader\\mytrader'
    #logfile=os.path.join(curr_path,'./ztrader/logs/thread.log')
    logname = 'aswgRequests'
    logfile = '{0}.log'.format(logname)
    logger = initial_logger(logfile,errorfile='{0}_error.log'.format(logname),logname=logname)
    logger.info('Start aswgRequests URL test...')
    #columns = ['result']
    columns = ['url','domain','status_code','time(s)','result','pid','ppid','theadname']
    write2csv(data=columns,file='result.csv',encoding='utf-8',logger=logger,clear=True)
    headers = None
    proxy_host = '172.17.33.23'
    proxy_port = 8080
    proxy_username = 'ts2'
    proxy_password = 'Firewall1'
    proxy_url = 'http://ts2:Firewall1@172.17.33.23:8080'
    proxy={'https': proxy_url, 'http': proxy_url}
    logger.info('Set global request proxy={0}'.format(proxy))
    timeout = (30,60)
    url_file = 'urls.txt'
    url_column = 0
    #url_file = 'rank_1000.txt'
    #url_column = 1
    test_url = 'https://www.baidu.com'
    urls = get_urls_from_file(from_file=url_file,url_index=url_column,spliter=',',pre_www='www.',encoding='utf-8',default_protocol='http')
    urls.insert(0,test_url)
    with ThreadPoolExecutor(pool_num) as executor:
        #adding_url_request_queue(executor,action,callback,urls=urls, url_file='',url_column=url_column,encoding='utf-8')
        # 等待一定时间，让线程执行任务
        i = 0 
        for url in urls:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
                'Connection': 'close',#'keep-alive'  #close' 原生http无状态
                'Host': url.replace('http://','').replace('https://','')
                #'Referer': url,
            }
            url_data = {
            'url': url,
            'sequece': i,
            'logger': logger,
            'result_file': 'aswgrequest_result.csv',
            'headers': headers,
            'proxy': proxy,
            'proxy_host': proxy_host,
            'proxy_port' : proxy_port,
            'proxy_username': proxy_username,
            'proxy_password': proxy_password,
            'timeout': timeout,
            'thread': 'thread_{0}'.format(i)
            }
            if i==0:#获取basic认证的认证缓存
                aswg_url_request(url_data)
                logger.info('Request test proxy URL for Auth buffer: {0}, and will wait 10s...'.format(test_url))
                time.sleep(10)  
            else:
                if not url:
                    continue
                else:
                    task = executor.submit(aswg_url_request,(url_data))#.add_done_callback(callback)
                    task.add_done_callback(callback)
            i = i + 1
    time.sleep(3)
    print("-" * 50)
    print("任务执行完毕，正常退出！")
    logger.info('Completed aswgRequests URL test!!!')
    # 强制关闭线程池
    # pool.terminate()
    # print("强制停止任务！")

