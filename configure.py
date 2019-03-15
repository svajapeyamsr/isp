"""
1. Functions take argument config_set

config_set= {}
config_set.setdefault('<IP addr>', [])

config_set= {'<IP addr1>': [cmd1, cmd2, cmd3, ...],
             '<IP addr2>': [cmd1, cmd2, cmd3, ...],
                ....
                }
"""
"""
2. To use this module:

#Import
from configure import Configure

config_set= {}
ips= []

#Prep config set
for ip in ips:
    config_set.setdefault(ip, [])

configs_set[ip1].append(cmd1)
configs_set[ip1].append(cmd2)

configs_set[ip2].append(cmd1)
configs_set[ip2].append(cmd2)


#Configure
obj1= Configure()
obj1.configure_linux_boxes(config_set)
obj1.configure_cisco_boxes(config_set)
"""

from datetime import datetime
import threading
from netmiko import ConnectHandler


#Threaded class. Each thread will configure separate box
class Configure_Linux_Box(threading.Thread):
    def __init__(self, net_device, commands):
        threading.Thread.__init__(self)
        self.net_device= net_device
        self.commands= commands
    
    def run(self):
        self.net_connect= ConnectHandler(**self.net_device)
        self.net_connect.find_prompt()
    
        for command in self.commands:
            output= self.net_connect.send_command_timing(command, strip_command= False, strip_prompt= False)
            
            #If Error Handling is needed, uncomment this. Adds delay!
            """
            output_status= self.net_connect.send_command_timing("echo $?", strip_command= False, strip_prompt= False)
            if(output_status!= "0"):
                print("Configuration error at device {}! Check syntax. See logfile for more info.".format(
                    self.net_device['ip']))
                with open('configure_linux_error_log.txt', 'a') as f:
                    f.write("{}::: CONFIG ERROR ::: {}".format(datetime.now().ctime(), output))
                    f.close()
            """
            
            
#Threaded class. Each thread will configure separate box           
class Configure_Cisco_Box(threading.Thread):
    def __init__(self, net_device, commands):
        threading.Thread.__init__(self)
        self.net_device= net_device
        self.commands= commands

    def run(self):
        self.net_connect= ConnectHandler(**self.net_device)
        self.net_connect.send_config_set(self.commands)

#Configures a set of boxes given 
class Configure():
    def __init__(self):
        self.net_device= {
            'device_type': None,
            'ip': None,
            'username': "angn",
            'password': "gapurocks123"
            }
        
    def configure_linux_boxes(self, config_set):
        threads= []
        for ip, commands in config_set.items():
            self.net_device['device_type']= "linux"
            self.net_device['ip']= ip
            
            thr_configure_linux_box= Configure_Linux_Box(self.net_device, commands)
            thr_configure_linux_box.daemon= True
            thr_configure_linux_box.start()
            threads.append(thr_configure_linux_box)
        
        for element in threads:
            element.join()
            
    def configure_cisco_boxes(self, config_set):
        threads= []
        for ip, commands in config_set.items():
            self.net_device['device_type']= "cisco_ios"
            self.net_device['ip']= ip
        
            thr_configure_cisco_box= Configure_Cisco_Box(self.net_device, commands)
            thr_configure_cisco_box.daemon= True
            thr_configure_cisco_box.start()
            threads.append(thr_configure_cisco_box)
        
        for element in threads:
            element.join()
            
            

