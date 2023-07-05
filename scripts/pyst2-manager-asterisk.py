#Connecting to Asterisk AMI using the pyst2 library
#Applicable to Asterisk version 18.15.1+
#Please install the pyst2 library, pip3 install pyst2
#使用pyst2库连接asterisk AMI
#适用于Asterisk 18.15.1+版本
#请安装pyst2库，pip3 install pyst2


from asterisk.manager import Manager  

def ami_login():
    manager.connect('server_ip')
    manager.login('username', 'secret')

def show_aors():
    response = manager.send_action({'Action': 'Command', 'Command': 'PJSIP show aors'})
    lines = response.response
    for line in lines:
        result = line.strip()
        print(result)
    manager.logoff()

def show_auths():
    response = manager.send_action({'Action': 'Command', 'Command': 'PJSIP show auths'})
    lines = response.response
    for line in lines:
        result = line.strip()
        print(result)
    manager.logoff()

def call_exten():  #拨打电话
    response = manager.send_action({
        'Action': 'Originate',
        'Channel': 'PJSIP/6001',     # 配置取自/etc/asterisk/pjsip.conf或extensions.conf
        'Exten': '6001',             # 配置取自/etc/asterisk/pjsip.conf或extensions.conf
        'Context': 'from-internal',  # 配置取自/etc/asterisk/pjsip.conf或extensions.conf
        'Priority': 1
    })



if __name__ == '__main__':
    manager = Manager()
    try:
        ami_login()
        #show_aors()
        #show_auths()
        call_exten()
    except Exception as e:
        print(f"无法连接服务器: {str(e)}")        

 
        

 
