from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import parse_qs
import cgi
import sys
import re
from netmiko import ConnectHandler

class GP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_HEAD(self):
        self._set_headers()
    def do_GET(self):
        self._set_headers()
        print (self.path)
        print (parse_qs(self.path[2:]))
        self.wfile.write(bytes("<html><body><h1>Get Request Received!</h1></body></html>\n",'utf-8'))
    def do_POST(self):
        
        self._set_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        vlan=(form.getvalue("vlan"))
        print ("VLAN is "+str(vlan))
        cust_IP=form.getvalue("ip")
        print ("IP assigned "+str(cust_IP))
        cust_URL=form.getvalue("url")
        print ("Customer URL "+str(cust_URL))
        self.wfile.write(bytes("<html><body><h1>POST Request Received!</h1></body></html>\n",'utf-8'))
        #print("Verify")
        
        dev_a = { 'device_type': 'arista_eos',
              'ip': '172.16.16.9',
              'username': 'angn',
              'password': 'gapurocks123'
            }
    
        net_connect = ConnectHandler(**dev_a)
        net_connect.enable()
        command=["vlan "+str(vlan)]
        send = net_connect.send_config_set(command)
        
        commands = ["interface vlan "+str(vlan),"ip address "+str(cust_IP)+" 255.255.255.0"]
        send = net_connect.send_config_set(commands)
        
        command1=["interface Vxlan1","vxlan source-interface Loopback1","vxlan udp-port 4789","vxlan vlan "+str(vlan)+" vni "+str(vlan),"vxlan flood vtep 1.1.1.1"]
        send = net_connect.send_config_set(command1)
        
        #dns_entry = ('echo "%s      300             IN      A       %s" >> /var/named/thunder.com' %(str(cust_URL),str(cust_IP)))
        
        
        dev_b = { 'device_type': 'arista_eos',
              'ip': '172.16.16.10',
              'username': 'angn',
              'password': 'gapurocks123'
            }
        
        b=cust_IP.split(".")
        c=((b[0:3]))
        c.append("1")
        gw_IP=c[0]+"."+c[1]+"."+c[2]+"."+c[3]
                
                
        net_connect_2 = ConnectHandler(**dev_b)
        net_connect_2.enable()
        command=["vlan "+str(vlan)]
        send = net_connect_2.send_config_set(command)
        
        commands = ["interface vlan "+str(vlan),"ip address "+str(gw_IP)]
        send = net_connect_2.send_config_set(commands)
        
        command1=["interface Vxlan1","vxlan source-interface Loopback1","vxlan udp-port 4789","vxlan vlan "+str(vlan)+" vni "+str(vlan),"vxlan flood vtep 2.2.2.2"]
        send = net_connect_2.send_config_set(command1)
        
        
        
def run(server_class=HTTPServer, handler_class=GP, port=8088):

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Server running at localhost:8088...')
    httpd.serve_forever()

run()
