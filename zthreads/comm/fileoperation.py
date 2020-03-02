# -*- coding:utf-8 -*-
#Author: allisnone
import csv
import random
import os,sys,time
import shutil
import hashlib

def write2csv(data,file='result.csv',encoding='utf-8',logger=None,clear=False):
    """
    把单个list写入csv文件，只写入一行
    :param data: list, the data need to write
    :param file: str, file name
    :param encoding: str, encoding type
    :return:
    """
    try:
        if clear and os.path.exists(file):
            os.remove(file)
        else:
            pass
        if sys.version_info.major==3:
            with open(file, 'a', encoding=encoding, newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data)
                csvfile.close()
        else:
            with open(file, 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data)
                csvfile.close()
    except Exception as e:
        if logger:
            logger.error('write2csv-data: {0}, file: {1}, {2}'.format(data, file,e))
        else:
            print(e)
    return

def write_datas_2csv(datas,file='result.csv',encoding='utf-8',logger=None,clear=True):
    """
    把多个list写入csv文件，写入多行
    :param datas: list, the data need to write
    :param file: str, file name
    :param encoding: str, encoding type
    :return:
    """
    try:
        if clear and os.path.exists(file):
            os.remove(file)
        else:
            pass
        with open(file, 'a', encoding=encoding, newline='') as csvfile:
            writer = csv.writer(csvfile)
            for data in datas:
                writer.writerow(data)
            csvfile.close()
    except Exception as e:
        if logger:
            logger.error('write_datas_2csv: {0}, file: {1}, {2}'.format(datas, file,e))
        else:
            print(e)
    return

def read_csv_dict(file='./raw/users.csv',encoding='utf-8'):
    """
    读取CSV文件的结果，返回list数据,每个数据是字典。
    :param file: str, file name
    :param encoding: str, encoding type
    :return:
    """
    datas = []
    with open(file, 'r',encoding=encoding) as f:
        reader = csv.DictReader(f)
        field_name = reader.fieldnames
        for row in reader:
            datas.append(dict(row))
    return datas
    
def read_csv_list(file='./raw/users.csv',ignore_header=True,encoding='utf-8',logger=None):
    """
    读取CSV文件的结果，返回list数据。
    :param file: str, file name
    :param encoding: str, encoding type
    :param logger: logger
    :param ignore_header: bool 
    :return:
    """
    data = []
    header = []
    with open(file, 'r',encoding=encoding) as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i==0 and ignore_header:
                if logger:
                    logger.info('Ignore header={0} from raw datas.'.format(row))
                else:
                    print('Ignore header={0} from raw datas.'.format(row))
                i = i + 1
                header = row
                continue
            if row:
                data.append(row)
            else:
                if logger:
                    logger.info('Line {0} was empty line.'.format(i))
                else:
                    print('Line {0} was empty line.'.format(i))
            i = i + 1
    return data,header


def remove_dir(dir):
    """
    删除指定目录，可以非空。
    :param top_dir: str, given DIR
    """
    return shutil.rmtree(dir)

def remove_all_sub_dirs_files(dir):
    """
    删除指定下目录的所有文件和所有目录，删除后该目录为空目录。
    :param top_dir: str, given DIR
    """
    if os.path.exists(dir)==False:
        print("dir not exists")
        return False
    if os.path.isdir(dir)==False:
        print("dir not a dir")
        return False 
    is_pathname_exist = False
    for dir_path,subpaths,files in os.walk(dir,False):
        for file in files:
            file_path=os.path.join(dir_path,file)
            os.remove(file_path)
        if subpaths:
            for path in subpaths:
                shutil.rmtree(os.path.join(dir_path,path))
    return 

def remove_dir_or_file(top_dir, pathname, type='dir',keyword_only=False,remove_all=True):
    """
    遍历指定文件夹中，删除指定的文件或目录名称，非绝对路径。
    :param top_dir: str, given DIR
    :param pathname: str, file name or dir name, or if pathname="*", remove all the files and dir in top_dir
    :param type: str, type="dir" or type="file"
    :param keyword_only: bool, if False, fully match pathname, or take pathname as a keyword
    :param remove_all: bool, if True, remove all matched the given pathname, or remove the first matching, then break
    :return: bool, if True, delete the existing file or dir
    """
    if os.path.exists(top_dir)==False:
        print("top_dir not exists")
        return False
    if os.path.isdir(top_dir)==False:
        print("top_dir not a dir")
        return False 
    is_pathname_exist = False
    for dir_path,subpaths,files in os.walk(top_dir,False):
        #print(dir_path,subpaths,files)
        if type=='dir':
            if os.path.split(dir_path)[-1]==pathname:
                is_pathname_exist = True
                for file in files:
                    file_path=os.path.join(dir_path,file)
                    print("delete file:%s"  %file_path)
                    os.remove(file_path)
                if subpaths:
                    for path in subpaths:
                        shutil.rmtree(os.path.join(dir_path,path))
                    print("delete subpaths:%s" %subpaths)
                print("delete dir:%s" %dir_path)
                os.rmdir(dir_path)
                if not remove_all and is_pathname_exist:
                    break
            else:
                pass
        elif type=='file':
            for file in files:
                if file==pathname:
                    is_pathname_exist = True
                    file_path=os.path.join(dir_path,file)
                    print("delete file:%s"  %file_path)
                    os.remove(file_path)
                    if not remove_all and is_pathname_exist:
                        break
                else:
                    pass
        else:
            print('Not exist type')
            return False
        if not remove_all and is_pathname_exist:
            break
    return is_pathname_exist



    
def copyFiles(sourceDir,  targetDir): 
    if sourceDir.find(".svn") > 0: 
        return 
    for file in os.listdir(sourceDir): 
        sourceFile = os.path.join(sourceDir,  file) 
        targetFile = os.path.join(targetDir,  file) 
        if os.path.isfile(sourceFile): 
            if not os.path.exists(targetDir):  
                os.makedirs(targetDir)  
            if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):  
                    open(targetFile, "wb").write(open(sourceFile, "rb").read()) 
        if os.path.isdir(sourceFile): 
            First_Directory = False 
            copyFiles(sourceFile, targetFile)
            
def coverFiles(sourceDir,  targetDir): 
    for file in os.listdir(sourceDir): 
        sourceFile = os.path.join(sourceDir,  file) 
        targetFile = os.path.join(targetDir,  file) 
        #cover the files 
        if os.path.isfile(sourceFile): 
            open(targetFile, "wb").write(open(sourceFile, "rb").read())
            
def removeFileInFirstDir(targetDir): 
    for file in os.listdir(targetDir): 
        targetFile = os.path.join(targetDir,  file) 
        if os.path.isfile(targetFile): 
            os.remove(targetFile)


def moveFileto(sourceDir,  targetDir):      
    shutil.copy(sourceDir,  targetDir)



class Hashfile:
    """
    获取文件的属性、内容相关hash值，并判断内容是否一样。
    支持('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512')
    """
    def __init__(self,file,type='md5',block_size=64*1024,limit=1024):
        self.file = file
        self.type = type
        self.block_size = block_size
        self.limit = limit
        self.stat = os.stat(file)  #获取文件属性
        self.hash = self.get_file_hash(file,block_size,limit) #获取文件内容的hash
        
    def set_hash_type(self,type):
        if type in ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'):
            self.type = type
        else:
            print('Invliad hash type={}'.format(type))
        
    def get_stat_hash(self,file=None):
        """
        基于文件大小和创建时间获取唯一的hash值
        :param file_stat: os.result obj
        """
        file_stat = None
        if file:
            file_stat = self.stat
        else:
            file_stat = os.stat(file)
        if not file_stat:
            return ''
        md5_obj = hashlib.new(self.type, b'')
        md5_obj.update('{0}{1}{2}'.format(file,file_stat.st_size,file_stat.st_ctime).encode('utf-8'))
        return md5_obj.hexdigest()
    
    def get_file_hash(self,file,block_size=None,limit=None):
        """
        基于内容获取唯一的hash值
        :param file: os.result obj
        :param type: hash type, can be  md5, sha1, sha128, sha256
        :param block_size: read file by block, to avoid read all to memory
        :param limit: file size limit, by default: 1024M
        """
        #print('time20=',time.time(),file)
        file_size = os.stat(file).st_size/1024/1024
        if block_size==None:
            block_size = self.block_size
        if limit==None:
            limit = self.limit
        if file_size > limit:
            print('file size ={}, exceed the limit of {}M'.format(file_size,limit))
            return ''
        with open(file,'rb') as f:
            hash_obj = hashlib.new(self.type,b'')
            while True:
                data = f.read(block_size)
                if not data:
                    break
                hash_obj.update(data)
            hash = hash_obj.hexdigest()
            #print('file_{}_md5={}'.format(file,hash))
            f.close()
            #print('time21=',time.time())
            return hash
        return ''
    
    def is_same_file(self,file):
        """
        判断是否是相同的文件, 基于文件属性, 更高效
        :param file: str, 文件名
        """
        if not os.path.isfile(file):
            print('Not a file obj!!!')
            return False
        return self.get_stat_hash(self.file)==self.get_stat_hash(file)
    
    def is_same_file_content(self,file,block_size=None,limit=None):
        """
        判断是否是相同的文件，基于文件内容；大文件较耗时，4G大约需要10秒
        :param file: str, 文件名
        """
        if not os.path.isfile(file):
            print('Not a file obj!!!')
            return False
        if block_size==None:
            block_size = self.block_size
        if limit==None:
            limit = self.limit
        return self.hash==self.get_file_hash(file,block_size,limit)  