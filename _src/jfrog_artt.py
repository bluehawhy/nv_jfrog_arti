from mailbox import linesep
import os

from _src._api import config, logger, method_logger

logging = logger.logger


logging= logger.logger

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



#=================method call =================
@method_logger.print_method
def install_jfrog_lib():
    # 1. check version
    #set up jFrog binary
    #for window
    cmd = 'jf -v'
    lines= send_cmd(cmd)    
    if 'jf version' in lines:
        logging.info(f'installed - {lines}')
    else:
        logging.info(f'install jf lib')
        cmd = "powershell \"Start-Process -Wait -Verb RunAs powershell '-NoProfile iwr https://releases.jfrog.io/artifactory/jfrog-cli/v2-jf/[RELEASE]/jfrog-cli-windows-amd64/jf.exe -OutFile $env:SYSTEMROOT\system32\jf.exe'\"; jf intro"
        logging.info(cmd)
        os.system(cmd)
    return 0

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
            
def download_file_from_artifactory(arti_path, local_path):
    cmd = f"jf rt dl {arti_path} {local_path}"
    logging.info(cmd)
    os.system(cmd)
    return 0

if __name__ =='__main__':
    print(__file__)