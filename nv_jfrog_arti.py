import os

from _src._api import logger
from _src import jfrog_arti, jfrog_arti_cmd, jfrog_arti_ui

logging= logger.logger

version = 'jfrog artifactory v0.1'
revision_list=[
    'Revision list',
    'v0.1 (2023-02-28) : proto type release (beta ver.)'
    ]

# how to 
# 1. need to setup - insert certi, set id and pw
# 2. check jfrog connection
# 3. download file 
# 3-1. check file exist in local
# 3-2. check file size 
# 

def file_check_in_pc(file = None,path='./static/temp'): #return type : bool
    check_value = False
    loca_file_path = os.path.join(path,os.path.basename(file))
    if os.path.exists(loca_file_path) is True:
        check_value =  True
        #logging.info(f'file already exist - {loca_file_path}')
    return check_value

def start():
    jfrog_arti_cmd.main()
    return 0
    
if __name__ =='__main__':
    start()