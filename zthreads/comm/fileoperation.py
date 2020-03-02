# -*- coding:utf-8 -*-
#Author: allisnone
import csv
import random
import os,sys,time
import shutil
import hashlib
import paramiko

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




# file size related
def getdirsize(dir):
    """
    获取目录占用空间大小, 单位字节
    :param top_dir: str, given DIR
    :return  int 
    """
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([os.stat(join(root, name)).st_size for name in files])
    return size

def get_int_size(size='10M'):
    """
    存储大单位字节数转化字节，返回字节数
    :param size: str
    :return  int 
    """
    unit = 'KMGTPEZY'#['K','M','G','T','P','E','Z','Y']
    if isinstance(size, int):
        return size
    elif isinstance(size, float):
        return int(size)
    elif isinstance(size, str):
        if size.isdigit():
            return int(size)
        elif is_number(size[:-1]):#size[:-1].isdigit():
            unit_index = unit.find(size[-1].upper())  
            if unit_index>=0:
                return int(float(size[:-1]) * (1024 ** (unit_index + 1 )))
            else: #1024的八次方意外的字节数
                return -1
        else:
            return -2
    else:
        return -3

def get_str_size(size=100):
    """
    字节数转化为带单位的字节，比如1234567字节，转化为：1.18M
    返回str类型
    :param size: int
    :return  str 
    """
    if size<0:
        return ''
    unit = 'KMGTPEZY'#['K','M','G','T','P','E','Z','Y']
    n = len(unit)
    while n>=0:
        if size>1024**n:
            break
        n = n -1
    size_str = '%s'%size
    if n>=1:
        size_unit = round(float(size)/(1024**n),2)
        size_str = '%s%s' % (size_unit,unit[n-1])
    return size_str

#file operation    
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


#File property
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
        #os.stat_result(st_mode=33206, st_ino=7318349394957043, st_dev=413549050, 
        #st_nlink=1, st_uid=0, st_gid=0, st_size=1093, 
        #st_atime=1583140201, st_mtime=1583118773, st_ctime=1583117999)
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
    
    
#file transfer
#免密登录：ssh-copy-id root@172.17.33.23
class SftpClient:
    #sftp 上传或者下载文件
    def __init__(self,ip,port=22,username='skygardts',password='123456',private_key_file='',keepalive=False):
        self.transport = None
        self.sftp = None
        self.keepalive = keepalive
        self.set_sftp_connection(ip,port,username=username,password=password,private_key_file=private_key_file)
        
    def set_sftp_connection(self,ip,port=22,username='username',password='123456',private_key_file=''):
        #初始化sftp的连接
        self.transport = paramiko.Transport((ip, port))
        if private_key_file:
            self.transport.connect(username=username, pkey=private_key)
        else:
            self.transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        return
        
    def _put(self,source,dest):
        # sftp 上传文件
        return self.sftp.put(source, dest)
    
    def put(self,source,dest):
        self._put(source, dest)
        if not self.keepalive:
            self.transport.close()
        return
    
    def _get(self,source,dest):
        #sftp 下载文件
        return self.sftp.get(source, dest)
    
    def get(self,source,dest):
        self._get(source, dest)
        if not self.keepalive:
            self.transport.close()
        return 
        
    def close(self):
        return self.transport.close()


class Sftpclient:
    #初始化连接创建Transport通道
    #优先使用private rsakey登录， 需要提前做免密登录设置：ssh-copy-id root@172.17.33.23
    def __init__(self,host='172.17.33.23',port=22,username='root',password='',private_key_file='',timeout=10,logger=None,keepalive=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.keepalive = keepalive  #if TRue上传或者下载完时，马上关闭连接
        self.logger = logger
        self.private_key = None  #RSAKey
        #private_key=paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
        #ssh=paramiko.SSHClient()
        #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        #ssh.connect(hostname="192.168.1.102",port=22,username="root",pkey=private_key)
        self.__transport = paramiko.Transport((self.host,self.port))
        if private_key_file: #Login by private_key_file, like /root/.ssh/id_rsa
            #private_key_file = '/root/.ssh/id_rsa'
            self.set_rpivate_rsakey(private_key_file)
            if self.private_key:
                try:
                    self.__transport.connect(username=self.username,pkey=self.private_key)#,timeout=timeout)
                except Exception as e:
                    if self.logger==None:
                        print('Failed to login by private rsakey, exception: {0} for host: {1}@{2}:{3}!; try to login by password...'.format(e,self.username,self.host,self.port))
                    else:
                        self.logger.info('Failed to login by private rsakey, exception: {0} for host: {1}@{2}:{3}!; try to login by password...'.format(e,self.username,self.host,self.port))
                    self.ssh_login_by_password()
        else: ##Login by password
            self.ssh_login_by_password()
        self.sftp = paramiko.SFTPClient.from_transport(self.__transport)
    
    def set_rpivate_rsakey(self,private_key_file):
        if os.path.exists(private_key_file) and os.path.isfile(private_key_file):
            self.private_key = paramiko.RSAKey.from_private_key_file(private_key_file)
        else:
            if self.logger==None:
                print('Invalid private_key_file: {0} for host: {1}@{2}:{3}!'.format(private_key_file,self.username,self.host,self.port))
            else:
                self.logger.error('Invalid private_key_file: {0} for host: {1}@{2}:{3}!'.format(private_key_file,self.username,self.host,self.port))
    
    def ssh_login_by_password(self):
        if self.password:
            self.__transport.connect(username=self.username,password=self.password)#,timeout=timeout)
        else:
            if self.logger==None:
                print('Both password and private_key_file are empty for host: {1}@{2}:{3}!'.format(self.username,self.host,self.port))
            else:
                self.logger.error('Both password and private_key_file are empty for host: {1}@{2}:{3}!'.format(self.username,self.host,self.port))
        return
    
    #关闭通道
    def close(self):
        self.sftp.close()
        self.__transport.close()
    
    #上传文件到远程主机
    def upload(self,local_path,remote_path):
        self.sftp.put(local_path,remote_path)
        if self.keepalive:
            pass
        else:
            self.close()
        if self.logger==None:
            pass
        else:
            self.logger.info('Uploaded from localhost:{0} to {1}:{2}'.format(local_path,self.host,remote_path))
        return True
    
    #从远程主机下载文件到本地
    def download(self,local_path,remote_path):
        self.sftp.get(remote_path,local_path)
        if self.keepalive:
            pass
        else:
            self.close()
        if self.logger==None:
            pass
        else:
            self.logger.info('Downloaded to localhost:{0} from {1}:{2}'.format(local_path,self.host,remote_path))
        return True
    
    #在远程主机上创建目录
    def mkdir(self,target_path,mode='0777'):
        self.sftp.mkdir(target_path,mode)
    
    #删除远程主机上的目录
    def rmdir(self,target_path):
        self.sftp.rmdir(target_path)
    
    #查看目录下文件以及子目录（如果需要更加细粒度的文件信息建议使用listdir_attr）
    def listdir(self,target_path):
        return self.sftp.listdir(target_path)
    
    #删除文件
    def remove(self,target_path):
        self.sftp.remove(target_path)
    
    #查看目录下文件以及子目录的详细信息（包含内容和参考os.stat返回一个FSTPAttributes对象，对象的具体属性请用__dict__查看）
    def listdirattr(self,target_path):
        try:
            list = self.sftp.listdir_attr(target_path)
        except BaseException as e:
            print(e)
        return list
    
    #获取文件详情
    def stat(self,remote_path):
        return self.sftp.stat(remote_path)
    
    #SSHClient输入命令远程操作主机
    def cmd(self,command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode().strip()
        return result
