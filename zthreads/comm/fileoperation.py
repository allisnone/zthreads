# -*- coding:utf-8 -*-
#Author: allisnone
import csv
import random
import os,sys,time

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