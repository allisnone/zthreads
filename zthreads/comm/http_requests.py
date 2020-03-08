# -*- coding: utf-8 -*-
#__Author__= allisnone 2018-08-01
#base on python3
#if you request https website, you need to add ASWG CA to following file:
#/root/.pyenv/versions/3.5.5/lib/python3.5/site-packages/certifi/cacert.pem
#ulimit –n 2000
import argparse
import re
import os
import csv
import string,sys
import requests
from zthreads.comm.fileoperation import write2csv,write_datas_2csv,read_text_file

from multiprocessing import Pool
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime
import urllib3
#requests.packages.urllib3.disable_warnings()
from requests.packages.urllib3.exceptions import SubjectAltNameWarning,InsecureRequestWarning
requests.packages.urllib3.disable_warnings(SubjectAltNameWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#PY_VERSION = sys.version_info.major
if sys.version_info.major==3:
    from urllib.parse import quote as quote
else:
    from urllib import quote as quote

def encode_url(url):
    """
        处理包含中文字符串/空格的URL编码问题
    :param url:
    :return:
    """
    return quote(url, safe=string.printable).replace(' ', '%20')

def get_urls_from_web(self, base_url):#,logger=None):
    """
        用于病毒测试，模拟下载病毒文件 , 依赖于页面内容编排而不一样
    :param base_url: str，  通常是用于存放病毒文件的某个url目录, 如'http://172.16.0.1/upload/VirusSamples/'
    :return: list， URL_list（Generator）
    """
    try:
        response = requests.get(base_url, headers=self.headers, proxies=self.proxy, verify=False)
        result = response.text
        if response.status_code==200:
            result = response.text
            if result:
                pattern = re.compile(r"<a href=\"(.*?)\">.*?</a>", re.S)
                fn = re.findall(pattern, result)
                #logger.info('result_fn={0}'.format(fn))
                return list(set([base_url + i for i in fn]))
            else:
                pass
    except Exception as e:
        if self.logger:
            self.logger.error('get_urls_from_web: {0}-{1}'.format(base_url,e))
        else:
            print('get_urls_from_web: {0}-{1}'.format(base_url,e))
    return []

def get_urls_from_file(from_file='url16000.txt',url_index=0,spliter=',',pre_www='www.',encoding='utf-8',default_protocol='http'):
    """
        用于url分类测试，测试文件中存放大量的url地址
    :param from_file: str 
    :param url_index: str
    :param spliter: str
    :param pre_www: str
    :param encoding: str
    :param default_protocol: str
    :return: list， URL_list（Generator）
    """
    raw_urls,header = read_text_file(file=from_file,encoding='utf-8',spliter=',',column=url_index,has_header=True,data_only=True)
    urls = []
    #print('raw_urls=',raw_urls)
    for url in raw_urls:
        #guess the protocol header
        protocol_header = url.lower()
        if "http://" in protocol_header or "https://" in protocol_header or "ftp://" in protocol_header:
            pass 
        else: #无协议头部，补全协议头，默认是http
            if pre_www:
                if pre_www in url:
                    pass
                else: #补全www前缀
                    url = pre_www + url
            else:
                pass
            if default_protocol:
                pass
            else:
                default_protocol = 'http'
            url = '{0}://'.format(default_protocol) + url
        urls.append(encode_url(url))
    return urls   

def urls_exception(self,urls,except_url_file='',url_index=1,spliter=',',pre_www='www.'):
    """
        排除特定文件中的url
    """
    #urls_exception = get_urls_from_file(except_url_file,url_index,spliter,pre_www)    
    return list(set(urls).difference(set(get_urls_from_file(except_url_file,url_index,spliter,pre_www))))


class Httprequests:
    def __init__(self,url,headers=None,proxy_host=None,prox_port=8080,proxy_username=None,proxy_password=None,logger=None):
        self.set_proxy(proxy_host, prox_port, proxy_username, proxy_password)
        #headers = {
        #        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        #}
        self.headers = headers
        self.logger = logger
        self.url = self.encode_url(url)
        self.set_proxy(proxy_host, prox_port, proxy_username, proxy_password)
        
        
    def set_proxy(self, proxy_host, prox_port=8080, proxy_username=None, proxy_password=None):
        """
        根据URL设置使用HTTP或者HTTPS的代理
        :param proxy_host: str type , host or ip
        :param prox_port: str type, port
        :param proxy_username: str type, user
        :param proxy_password: str type,  password
        :return None, set proxy like {'http': 'http://172.18.230.23:8080', 'https':'https://172.18.230.23:8080'}
        """
        proxy_str = '' #172.18.230.23:8080
        if proxy_host and prox_port:
            proxy_str = '{0}:{1}'.format(proxy_host,prox_port)
        if not proxy_str:
            self.proxy = {}
            return 
        proxy_user = ''  #yangfashouxian:Firewall1
        if proxy_username and proxy_password:
            proxy_user = '{0}:{1}'.format(proxy_username,proxy_password)
        else:#no give proxy user or pass
            pass
        proxy_url = ''
        if proxy_user:
            proxy_url = '{0}@{1}'.format(proxy_user, proxy_str)
        else:
            proxy_url = proxy_str
        self.proxy = {'http': 'http://' + proxy_url, 'https':'http://' + proxy_url}
        return  
    
    def set_header(self, headers):
        """
        set http header
        :param headers: dict type
        :return None
        """
        self.headers = headers
        return
 
    def encode_url(self, url):
        """
        处理包含中文字符串/空格的URL编码问题
        :param url:
        :return:
        """
        return quote(url, safe=string.printable).replace(' ', '%20')
    
    def get(self,url=None,params=None,headers=None,files=None):
        """
        封装get方法，return响应码和响应内容: 
        :param url: None or str
        :param params: dict type
        :param headers: dict type
        :param files:
        :return status_code,json response: int, json
        """
        if url==None:
            url = self.url
        try:
            r = requests.get(url,params = params,headers = headers,files=files)  #**kwargs
            #r.encoding = encoding
            return r.status_code,r.json()    # 返回响应码，响应内容
        except Exception as e:
            if self.logger: self.logger.error("Request get exception: {0}".format(e))
            return -1,{}
    
    def post(self, url=None, data=None, headers=None,files=None):
        """
        封装post方法，return响应码和响应内容: 
        :param url: None or str
        :param data: dict type
        :param headers: dict type
        :param files:
        :return status_code,json response: int, json
        """
        if url==None:
            url = self.url
        try:
            r = requests.post(url, data=data, headers=headers,files=files) #**kwargs
            #r.encoding = encoding
            return r.status_code,r.json()    # 返回响应码，响应内容
        except Exception as e:
            if self.logger: self.logger.error("Request post exception: {0}".format(e))
            return -1,{}
    
    def post_json(self,url=None,data=None,headers=None):
        """
        封装json post方法，return响应码和响应内容: 
        :param url: None or str
        :param data: dict type
        :param headers: dict type
        :param files:
        :return status_code,json response: int, json
        """
        if url==None:
            url = self.url
        try:
            data = json.dumps(data).encode('utf-8')  # python数据类型转化为json数据类型
            r = requests.post(url, data=data, headers=headers)
            #r.encoding = encoding
            return r.status_code,r.json()     # 返回响应码，响应内容
        except Exception as e:
            if self.logger: self.logger.error("Request post_json exception: {0}".format(e))
            return -1,{}


    def url_request(self,url=None, block_info='访问的URL中含有安全风险',encoding='utf-8',verify=False,retry_once=False,timeout=(30,60),thread=''):
        """
        下载文件，分析是否被SWG阻断
        :param url:
        :param block_info: str 
        :param encoding: str
        :param verify: bool, veirify certificate or not
        :param retry_once: bool, if True, will try http or https protocol once more
        :param timeout: tuple of int
        :return: list
        """
        #block_info = '访问的URL中含有安全风险'
        pid,ppid = os.getpid(),os.getppid()
        #if True:
        if url==None:
            url = self.url
        try:
            r = requests.get(self.encode_url(url), headers=self.headers,proxies=self.proxy,timeout=timeout,verify=verify)
            block_type = ''
            if r.status_code==403:
                r.encoding = encoding
                if block_info in r.text: #标准阻断
                    block_type = '403block'
                else: #其他403阻断
                    block_type = "403other"
            elif r.status_code==200:#200ok 放行
                block_type = "pass"
            elif r.status_code==502:#DNS resolve failure
                block_type = "dns_failed"
            else:#403，200 以外的待定
                block_type = "unknown"
            if self.logger:
                self.logger.info('request-url: {0}, http_code: {1}, action: {2}, pid-{3}, ppid-{4}, thread-{5}'.format(url, r.status_code,block_type, pid,ppid,thread))
            else:
                print('request-url: {0}, http_code: {1}, action: {2}, pid-{3}, ppid-{4}, thread-{5}'.format(url, r.status_code,block_type,pid,ppid,thread))
            return [url, url.split('/')[-1], r.status_code, block_type, pid,ppid,thread]
        #except:
        #else:
        except Exception as e:
            if retry_once:#try to guess http or https
                if "https://" in url:
                    url = url.replace('https://','http://')
                    if self.logger: self.logger.info('request-url: one more try, replace https request to http: {0}'.format(url))
                elif "http://" in url:
                    url = url.replace('http://','https://')
                    if self.logger: self.logger.info('request-url: one more try, replace http request to https: {0}'.format(url))
                else:
                    pass
                url_request(url,proxy,block_info,encoding,retry_once=False)
            if self.logger: self.logger.error('request-url-exception: {0}, ERROR: {1} '.format(url, e))
            return [url, url.split('/')[-1], 0, e,pid,ppid,thread]
    
    def request_results(self,url,file='result.csv',type='url'):#,logger=None):
        """
        :param url:
        :param block_info: str 
        :param encoding: str
        :return None
        """
        #print('ppid:{0}-pid:{1}'.format(os.getpid(),os.getppid()))
        block_info='访问的URL中含有安全风险'
        if type=='virus':
            block_info = '病毒'
        #print('type:',type(url))
        if isinstance(url, str) or isinstance(url,unicode):
            #print('url-1=',url)
            result = self.url_request(url,block_info=block_info)
            if file:#should give filename
                write2csv(result, file)
        elif isinstance(url, list):#several datas once write
            results = []
            #print('url-2=',url)
            for u in url:
                result = self.url_request(u,block_info=block_info) 
                if result:
                    results.append(result)
                else:
                    logger.error('No result for sub-request-url: {0}'.format(u))
            if results and file:#should give filename
                write_datas_2csv(results, file)
            else:
                logger.error('No any results for request-url set: {0}'.format(url))
        else:
            logger.error('Invalid request-url type: {0}, url: {1}'.format(type(url),url))
        return

#if __name__ == '__main__':
    """
    parser = argparse.ArgumentParser(description='该Python3脚本用于ASWG做URL分类测试和病毒测试。\n 1、URL测试使用方法:\n python aswgRequest.py -t url -f ulrs.txt -p 172.18.230.23:8080 -o urls_result.csv \n 2、病毒测试：  python aswgRequest.py -t virus -u http://www.sogaoqing.com/upload/VirusSamples/ -p 172.18.230.23:8080 -o virus_result.csv') 
    parser.add_argument('-t','--type', type=str, default='url',help='默认为url分类测试，从文件读取url地址；当设置为virus时，将模拟从某个web服务器特定目录下载所有文件。')
    parser.add_argument('-p','--proxy', type=str, default = '',help='默认不适用aswp代理，需指定代理时，<proxy_IP>:<proxy_port> 例如：72.18.230.23:8080') 
    parser.add_argument('-f','--url-file', type=str, default= 'urls.txt',help='默认为urls.txt， 指定包含需要测试url的文件，每行一条url。')
    parser.add_argument('-u','--url-base', type=str, default= '',help='默认为空，用于模拟下载病毒测试，指定url目录，如： http://172.16.0.1/upload/VirusSamples/')
    parser.add_argument('-o','--out-put', type=str, default='',help='默认为result.csv，测试结果保存为csv文件。')
    parser.add_argument('-c','--cpu-num', type=str, default=1,help='默认为cpu数为系统cpu核心数，输入整数')
    parser.add_argument('-l','--log-file', type=str, default='aswgRequest',help='脚本输出的日志文件')
    parser.add_argument('-w','--write-per-num', type=int, default=1,help='每次写多少个result，默认是1，并发中减少文件读写')
    parser.add_argument('-e','--except-file', type=str, default='',help='url排除文件，通常是上一次运行过的结果，不期望重复请求')
    parser.add_argument('-i','--index-url-file', type=int, default=0,help='提取每行url的序号，默认取第0列，逗号分隔')
    parser.add_argument('-j','--index-except-file', type=int, default=0,help='url排除文件中，提取每行url的序号，默认取第0列，逗号分隔')
    args = parser.parse_args()
    type = args.type
    proxy = args.proxy
    url_file = args.url_file
    result_file = args.out_put
    url_base = args.url_base
    cpu_num = int(args.cpu_num)
    log_file = args.log_file
    write_per_num = args.write_per_num
    except_url_file = args.except_file
    index_url_file = args.index_url_file
    index_except_file = args.index_except_file
    logfile = '{0}_{1}_all.log'.format(log_file,type)
    errorfile = '{0}_{1}_error.log'.format(log_file,type)
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Connection': 'keep-alive'  #'close'
    }
    #logger = initial_logger(logfile,errorfile,logname=log_file)
    logger.info('---------------------开始 {}测试-------------------------------------------'.format(type))
    #date_str = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
    logger.info('ASWG Proxy 为: {0}，开启线程数:{1}'.format(proxy,cpu_num))
    #record_result_file = True
    if  result_file:
        if os.path.exists(result_file):
            os.remove(result_file)
            logger.info('remove existing file: {0}'.format(result_file))
    else:
        logger.info('Will not record result file!!!'.format())
    urls = []
    if type=='url' or type=='aseg':
        urls = get_urls_from_file(from_file=url_file,url_index=index_url_file,spliter=',',pre_www='www.')
        if except_url_file:
            urls = urls_exception(urls, except_url_file, url_index=index_except_file, spliter=',', pre_www='www.') 
        print(len(urls))
        #sys.exit()
    elif type=='virus':
        if url_base:
            urls = get_urls_from_web(url_base)
        else:
            logger.error('缺少指定URL下载目录，脚本退出！！！')
            sys.exit()
    else:
        logger.error('测试类型错误，脚本退出！！！')
        sys.exit()
    if urls:
        logger.info('urls={0}'.format(urls))
        logger.info('待测试URL总数为：{} '.format(len(urls)))
    else:
        logger.error('获取url失败，脚本退出！！！')
        sys.exit()
    pool = Pool()
    if cpu_num>1:
        pool = Pool(cpu_num)
    else:
        pass
    #weilin modifiy at 20190705AM
    if 'aseg' == type:
        MAX_URL_LEN = 3900
        xURL=''
        for url in urls:
            if len(xURL) + len(url) > MAX_URL_LEN and '' != xURL:
                xURL += ']'
                pool.apply_async(request_results, (xURL, '',result_file,type))
                #print('xURL A : ', xURL)
                xURL = ''
            if '' == xURL:
                #xURL = 'http://172.17.200.102:8000/urlcats/batchlookup?batchlookup=[{\"url\":"' + url + '"}'
                #xURL = 'http://{0}/urlcats/batchlookup?batchlookup=[{\"url\":\"{1}\"}'.format(proxy,url)
                xURL = 'http://'+ proxy + '/urlcats/batchlookup?batchlookup=[{\"url\":"' + url + '"}'
            else:
                xURL += ',{\"url\":"' + url + '"}'
            if len(xURL) > MAX_URL_LEN:
                xURL += ']'
                pool.apply_async(request_results, (xURL, '',result_file,type))
                #print('xURL B : ', xURL)
                xURL = ''
        if '' != xURL:
            xURL += ']'
            pool.apply_async(request_results, (xURL, '',result_file,type))
            #print('xURL C : ', xURL)
            xURL = ''

    else:
        if write_per_num==1:
            pass
        elif write_per_num>1:
            if len(urls)>=cpu_num*3:
                urls = [urls[i:i+write_per_num]for i in range(0,len(urls),write_per_num)]
        else:
            pass
        logger.info('urls='%urls)
        for url in urls:
            pool.apply()
            #pool.apply_async(http_request, (url, proxy), callback=write2csv)
            pool.apply_async(request_results, (url, proxy,result_file,type))
    pool.close()
    pool.join()
    logger.info('---------------------{0}测试完成-------------------------------------------'.format(type) )
    logger.info('测试结果位于：{} '.format(result_file ))
    sys.exit()
    #需要踏平的坑
    """
    """设置 ulimit -n 10240--否则大规模 读写文件/请求会出现  Errno 99 错误"""
    """ASWG URL测试使用方法"""
    #python aswgRequest.py -t url -f urls.txt -p 172.18.230.23:8080 -o urls_result.csv -c 512 -l aswgRequest
    #python aswgRequest.py -t url -f urls.txt -p 172.18.200.240:8080 -o urls_result.csv -c 512 -l aswgRequest
    #python aswgRequest.py –t <请求类型为url> -f <url文件来源>  -p <swg代理IP:端口> -o  <日志输出>  -c <并发进程数> -l <日志文件名>
    """ASWG 病毒测试使用方法，模拟http下载病毒"""
    #python aswgRequest.py -t virus -u http://www.sogaoqing.com/upload/VirusSamples/ -p 172.18.230.23:8080 -o virus_result.csv
    #python aswgRequest.py –t <请求类型为virus> -f <url文件目录>  -p <swg代理IP:端口> -o  <日志输出>  -c <并发进程数> -l <日志文件名>
    """ASEG URL测试使用方法"""
    #1）/etc/trafficserver/records.config ,第23行去掉ip-in=127.0.0.1
    #CONFIG proxy.config.http.server_ports STRING 8000:ipv4:proto=http
    #2）修改ASEG配置文件 vi /etc/trafficserver/remap.config  ，改为管理口eth0的IP：添加两行
    #map http://aseg-eth0-ip:8000/urlcats/ http://{urlcats}
    #map http://aseg-eth0-ip:8000/urlcats/ http://{urlcats}
    #3）/etc/init.d/trafficsever restart
    #4)Linux 客户端运行脚本
    #python aswgRequest.py -t aseg -f urls.txt -p 172.17.31.26:8000 -o urls_result.csv -c 512 
    #python aswgRequest.py –t <请求类型为aseg> -f <url文件来源>  -p <aseg-eth0-ip:端口8000> -o  <日志输出>  -c <并发进程数> -l <日志文件名>
    

