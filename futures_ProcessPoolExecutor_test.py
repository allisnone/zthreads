# -*- coding:utf-8 -*-
#Author: allisnone
import time
import random

"""
一个基于thread和queue的进程池，以任务为队列元素，动态创建线程，重复利用线程，
通过close和terminate方法关闭进程池。
"""
from concurrent.futures import ProcessPoolExecutor,as_completed,wait,ALL_COMPLETED,FIRST_COMPLETED,FIRST_EXCEPTION
#from zthreads.comm.fileoperation import write2csv


def callback(future):
    """
    根据需要进行的回调函数，默认不执行。
    :param status: action函数的执行状态
    :param result: action函数的返回值
    :return:
    """
    print('callback status=,result={0}'.format(future.result()))
    return 

 
 
def action(arg):
    """
    真实的任务定义在这个函数里
    :param thread_name: 执行该方法的线程名
    :param arg: 该函数需要的参数
    :return:
    """
    # 模拟该函数执行了0.1秒
    time.sleep(0.1)
    print("第%s个任务调用了线程 ，并打印了这条信息！" % (arg+1))
    result = {'values_{0}'.format(arg+1): random.random()}
    return result
 
# 调用方式
if __name__ == '__main__':
    # 创建一个最多包含5个线程的进程池
    pool_num = 5
    #executor = ProcessPoolExecutor(5)
    # 创建100个任务，让进程池进行处理
    #tasks = [executor.submit(action, (i)) for i in range(100)]
    #for i in range(100):
    #    tasks.append(executor.submit(action, (i)))
    # 等待一定时间，让线程执行任务
    
    print("-" * 50)
    #as_completed 返回一个生成器，用于迭代， 一旦一个线程完成(或失败) 就返回
    with ProcessPoolExecutor(pool_num) as executor:
        for future in as_completed([executor.submit(action, (i)) for i in range(100)]):
            data = future.result()
            print(data)
    #executor.shutdown(wait=True)
    print("阶段1，任务执行完毕，暂停10s...！")
    time.sleep(10)
    print("阶段2，继续执行进程池函数！")
    #并发提交任务
    #tasks = [executor.submit(action, (i)) for i in range(100)]
    #回调函数-add_done_callback
    with ProcessPoolExecutor(pool_num) as executor:
        for i in range(100):
            task = executor.submit(action, (i))
            task.add_done_callback(callback)
    print("阶段2，任务执行完毕，暂停10s...！")
    time.sleep(10)
    print("阶段3，map继续执行进程池函数！")
    #map顺序执行，顺序出结果
    with ProcessPoolExecutor(pool_num) as executor:
        for data in executor.map(action,[i for i in range(100)]):
            pass#print('data=', data)
    
    print("阶段3，任务执行完毕，暂停10s...！")
    time.sleep(10)
    print("阶段4，map继续执行进程池函数！")
    #wait 是阻塞函数,第一个参数和as_completed一样, 一个可迭代的future序列,返回一个元组 ,包含2个set , 一个完成的，一个未完成的
    with ProcessPoolExecutor(pool_num) as executor:
        result = wait([executor.submit(action, (i)) for i in range(100)], return_when=ALL_COMPLETED)
        #time.sleep(10)
        print('result=',result)
    print("阶段4，任务执行完毕")
    #for i in range(100):
    #    tasks.append(executor.submit(action, (i)))
    # 等待一定时间，让线程执行任务
    
    
    # 强制关闭进程池
    # pool.terminate()
    # print("强制停止任务！")

 

