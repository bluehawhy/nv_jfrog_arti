import os
import subprocess

from _src._api import config, logger
from _src import jfrog_artt

version = 'jfrog artifactory v0.1'
revision_list=[
    'Revision list',
    'v0.1 (2023-02-28) : proto type release (beta ver.)'
    ]

# how to 
# 1. need to setup - insert certi, set id and pw
# 2. check jfrog connection
# 3. download file 

def start():
    jfrog_artt.download_file_from_artifactory()
    return 0



if __name__ =='__main__':
    start()