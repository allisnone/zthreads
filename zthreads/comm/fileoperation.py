# -*- coding:utf-8 -*-
#Author: allisnone
import csv
import random
import os,sys,time
import shutil

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

def remove_dir(top_dir, pathname, type='dir',remove_all=True):
    """
    遍历指定文件夹中，删除指定的文件或目录名称，非绝对路径。
    :param top_dir: str, given DIR
    :param pathname: str, file name or dir name, or "*"
    :param type: str, type="dir" or type="file"
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
    
    
#remove_dir(top_dir='C:\\Users\\zhangguoxin\\git\\zthreads', pathname='test2', type='dir', remove_all=True)