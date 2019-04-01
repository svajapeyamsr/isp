import requests
import ast

flows_dict = {}

def get_switch_list_backup():
	try:
                switch_list_resp = requests.get("http://10.10.10.40:8080/stats/switches")
        	return switch_list_resp,"10.10.10.40"
        except:
                print("Port not open to accept api requests in 10.10.10.40")
		return False,False

def get_switch_list():
	try:
		switch_list_resp = requests.get("http://10.10.10.20:8080/stats/switches")
		return switch_list_resp,"10.10.10.20"
	except:
		print("Port not open to accept api requests in 10.10.10.20. Checking backup server")
		switch_list_resp,ip = get_switch_list_backup()
		if switch_list_resp == False:
			print("Unable to get stats through api") 
			quit()
		return switch_list_resp,ip

switch_list_resp,ip = get_switch_list()
switch_list = ast.literal_eval(switch_list_resp.text)
print("List of switches:")
for switch in switch_list:
	flows_dict[str(switch)] = []
	print("Switch name: {}".format(switch))
	resp_flows = requests.get("http://{}:8080/stats/flow/{}".format(ip,switch))
	flows = ast.literal_eval(resp_flows.text)
	flows_list = flows[str(switch)]
	for flow in flows_list:
		temp_dict = {}
		if "['OUTPUT:CONTROLLER']" not in str(flow):
			temp_dict["dst"] = flow["match"]["nw_dst"]
			temp_dict["src"] = flow["match"]["nw_src"]
			temp_dict["count"] = flow["packet_count"]
			temp_dict["bytes"] = flow["byte_count"]
			flows_dict[str(switch)].append(temp_dict)
		
current_traffic = {}
for switch in flows_dict.keys():
	for flow in flows_dict[switch]:
		if flow["src"]+" "+flow["dst"] in current_traffic.keys() or flow["dst"]+" "+flow["src"] in current_traffic.keys():
			pass
		else: 
			current_traffic[flow["src"]+" "+flow["dst"]] = flow["bytes"]

for record in current_traffic.keys():
	print("Source: {}\tDestination: {}\tTraffic in Bytes:{}".format(record.split()[0],record.split()[1],current_traffic[record]))

