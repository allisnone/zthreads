# -*- coding:utf-8 -*-
#Author: allisnone
from zthreads.comm.fileoperation import Hashfile,read_text_file
import time

read_text_file(file='ssh_iplist.txt')

#remove_all_sub_dirs_files(dir='C:\\Users\\zhangguoxin\\git\\zthreads\\test\\test1\\test3')    
#remove_dir(top_dir='C:\\Users\\zhangguoxin\\git\\zthreads', pathname='test2', type='dir', remove_all=True)
t0 = time.time()
#hf = Hashfile('C:\\Users\\zhangguoxin\\git\\zthreads\\test\\test1\\testremove.txt')
f = 'D:\\iso\\SK80-debian-skyguard-ucss.iso'
print(t0,time.time())
hf = Hashfile('D:\\iso\\SK80-debian-skyguard-ucss.iso',type='md5',block_size=128*1024,limit=10240)
print(t0,time.time())
print(hf.hash)
t1 = time.time()
print(t1-t0)
f1 = 'C:\\Users\\zhangguoxin\\Downloads\\VMware-viclient-all-6.0.0.exe'
#print(hf.get_file_hash(f1,block_size=128*1024,limit=1024))
t10 = time.time()
print(t10-t1)
print(hf.is_same_file('C:\\Users\\zhangguoxin\\git\\zthreads\\test\\test1\\testremove1.txt'))
t2 = time.time()
print(t2-t1)
print(hf.is_same_file_content(f1))
t3 = time.time()
print(t3-t2)

f3 = 'C:\\Users\\zhangguoxin\\Downloads\\webservice.jar'
print(hf.is_same_file_content(f3))