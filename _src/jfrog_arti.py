from mailbox import linesep
import os
import json

from _src._api import config, logger, method_logger

logging = logger.logger


config_path ='static\config\config.json'
config_data =config.load_config(config_path)


#=============================================
def send_cmd(cmd):
    os.system(f'{cmd} > static\\temp\\result.txt')
    f = open("static\\temp\\result.txt", "r")
    lines =f.read()
    f.close()
    os.system('del static\\temp\\result.txt')
    return lines

#=================sub function call =================
def sync_file_local(arti_file, local_path):
    #set variable
    file_path_local = os.path.join(local_path,*arti_file['path'].split('/')[1:])
    file_path_arti = arti_file['path']
    file_check_local = os.path.exists(file_path_local)
        
    file_size_in_local = os.path.getsize(file_path_local) if file_check_local is True else 0
    file_size_in_arti = arti_file['size']
    file_size_check = True if str(file_size_in_local) == str(file_size_in_arti) else False
        
    #there is no file in local
    if file_check_local is False:
        logging.info(f'check file in local - {file_check_local}')
        download_a_file_from_artifactory(file_path_arti,local_path)
        return 0
    #there is file but diff size.
    if file_size_check is False:
        logging.info(f'local size - {file_size_in_local}, arti size - {file_size_in_arti}')
        download_a_file_from_artifactory(file_path_arti,local_path)
        return 0
    else:
        logging.info(f'check file in local - {file_check_local}, file_size_check - {file_size_check}')
        return 0

def download_a_file_from_artifactory(arti_path, local_path):
    cmd = f'jf rt dl "{arti_path}" "{local_path}"'
    logging.info(cmd)
    os.system(cmd)
    return 0


#=================method call =================
@method_logger.print_method
def search_file_list_in_artifactory(arti_path):
    cmd = f'jf rt s "{arti_path}"'
    lines = send_cmd(cmd)
    lines = json.loads(lines)    
    return lines

@method_logger.print_method
def install_jfrog_lib():
    # 1. check version
    #set up jFrog binary
    #for window
    cmd = 'jf -v'
    lines= send_cmd(cmd)    
    if 'jf version' in lines:
        logging.info(f'installed - {lines}')
        return True, 'already installed'
    else:
        logging.info(f'install jf lib')
        cmd = "powershell \"Start-Process -Wait -Verb RunAs powershell '-NoProfile iwr https://releases.jfrog.io/artifactory/jfrog-cli/v2-jf/[RELEASE]/jfrog-cli-windows-amd64/jf.exe -OutFile $env:SYSTEMROOT\system32\jf.exe'\"; jf intro"
        logging.info(cmd)
        os.system(cmd)
        #checking again.
        cmd = 'jf -v'
        lines= send_cmd(cmd)
        if 'jf version' in lines:
            logging.info(f'installed - {lines}')
            return True, 'installed'
        else:
            logging.info(f'not installed - {lines}')
            return False, 'not installed'

@method_logger.print_method
def update_jfrog_server_config(
    user = config_data['swf_server']['user'], 
    password = config_data['swf_server']['password'],
    last_arti = config_data['last_arti'],
    last_path = config_data['last_path']):
    config_data['swf_server']['user'] = user
    config_data['swf_server']['password'] = password
    config_data['last_arti'] = last_arti
    config_data['last_path'] = last_path
    config.save_config(config_data,config_path)
    return config_data


@method_logger.print_method
def setup_jfrog_server_config():
    serverId = config_data['swf_server']['serverId']
    url = config_data['swf_server']['url']
    user = config_data['swf_server']['user']
    password = config_data['swf_server']['password']
    clientCertPath = os.path.join(os.getcwd(),config_data['swf_server']['clientCertPath'])
    clientCertKeyPath = os.path.join(os.getcwd(),config_data['swf_server']['clientCertKeyPath'])
    cmd = f'jf c add {serverId} --url={url} --user={user} --password={password} --client-cert-key-path="{clientCertKeyPath}" --client-cert-path="{clientCertPath}" --overwrite=true'
    logging.info(cmd)
    os.system(cmd)
    return 0

@method_logger.print_method
def show_jfrog_server_config():
    cmd = "jf c show"
    lines = send_cmd(cmd)
    logging.info(lines)
    return 0

@method_logger.print_method
def check_artifactory_connection(server_id=config_data['swf_server']['serverId']):
    connection_status = False
    cmd = f"jf rt p --server-id={server_id}"
    lines = send_cmd(cmd)
    #logging.info(lines)
    line = lines.split('\n')[0]
    if "OK" in line:
        logging.info("Artifactory Connection : OK")
        connection_status = True
    else:
        logging.info("Artifactory Connection : NOK")
    return connection_status


@method_logger.print_method
def sync_arti_local(arti_path, local_path):
    #search file list and convert one
    file_lists = search_file_list_in_artifactory(arti_path)
    for file in file_lists:
        logging.info(f"start download - {file['path']}")
        sync_file_local(file, local_path)
    logging.info(f"finish download - {arti_path}")
    return 0

if __name__ =='__main__':
    print(__file__)