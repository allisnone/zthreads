# -*- coding: utf-8 -*-
#__Author__= allisnone 2018-08-01
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import os,sys

def initial_logger(logfile='all.log',errorfile='error.log',logname='mylogger',debug=True):
    logger = logging.getLogger(logname)
    if debug:
        logger.setLevel(logging.DEBUG)
    if os.path.exists(logfile):
        pass
    else:
        print('File does not exist')
    if sys.version_info.major==3: 
        rf_handler = TimedRotatingFileHandler(logfile, when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
    else:
        rf_handler = TimedRotatingFileHandler(logfile, when='midnight', interval=1, backupCount=7)
    rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    #f_handler = logging.FileHandler(errorfile)
    #f_handler.setLevel(logging.ERROR)
    #f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))
    logger.addHandler(rf_handler)
    #logger.addHandler(f_handler)
    return logger