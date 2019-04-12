import requests
import ast
import json
from influxdb import InfluxDBClient
from datetime import datetime

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
while True:
	switch_list_resp,ip = get_switch_list()
	switch_list = ast.literal_eval(switch_list_resp.text)
	print("List of switches:")
	for switch in switch_list:
		flows_dict[str(switch)] = []
		print("Switch name: {}".format(switch))
		resp_flows = requests.get("http://{}:8080/stats/flow/{}".format(ip,switch))
		flows = ast.literal_eval(resp_flows.text)
		flows_list = flows[str(switch)]
			#print(flows_list)
		for flow in flows_list:
			temp_dict = {}
			if "['OUTPUT:CONTROLLER']" not in str(flow):
                                temp_dict["dst"] = flow["match"]["nw_dst"]
				temp_dict["src"] = flow["match"]["nw_src"]
				temp_dict["count"] = flow["packet_count"]
				temp_dict["bytes"] = flow["byte_count"]
                                temp_dict["protocol"] = flow["match"]["nw_proto"]
				flows_dict[str(switch)].append(temp_dict)
			
	current_traffic = {}
	top_talkers=[]
	for switch in flows_dict.keys():
		for flow in flows_dict[switch]:
			if flow["src"]+" "+flow["dst"] in current_traffic.keys() or flow["dst"]+" "+flow["src"] in current_traffic.keys():
				pass
			else: 
				current_traffic[flow["src"]+" "+flow["dst"]+" "+str(flow["protocol"])] = flow["bytes"]
	client = InfluxDBClient('localhost', 8086, 'root', 'root', 'CurrentTraffic')
	client.create_database('CurrentTraffic')
	for record in current_traffic.keys():
			src_IP=record.split()[0]
			dst_IP=record.split()[1]
			trafficBytes=current_traffic[record]
			IP_proto=record.split()[2]
			current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
			if IP_proto=="1":
			   protocol="ICMP"
			elif IP_proto=="6":
			   protocol="TCP"
			elif IP_proto=="17":
			   protocol="UDP"
			else:
			   protocol="Misc"
		        print("Source: {}\tDestination: {}\tProtocol: {}\tTraffic in Bytes:{}".format(src_IP,dst_IP,protocol,trafficBytes))
			top_talkers.append(trafficBytes)
			json_body1 = [
			{
			"measurement": "current_traffic",
			"tags": {
				"sourceIP": src_IP,
				"destIP": dst_IP,
				"Protocol": protocol
			},
			"time": current_time,
			"fields": {
				"value": trafficBytes,
			}
			}
			]  
			#print(json_body)
			print(client.write_points(json_body1))
			result = client.query('select value from current_traffic;')
	print("Result: {0}".format(result))
	top_talkers.sort(reverse=True)
	Max_traffic=top_talkers[0]
	print("********************************************")
	print("------------TOP TALKERS--------------------")
	print("********************************************")
	for record in current_traffic.keys():
			if(current_traffic[record]==Max_traffic):
			  IP_proto=record.split()[2]
			  if IP_proto=="1":
				protocol="ICMP"
			  elif IP_proto=="6":
				protocol="TCP"
			  elif IP_proto=="17":
				protocol="UDP"
			  else:
				protocol="Misc"  
			  print("Source: {}\tDestination: {}\tProtocol: {}\tTraffic in Bytes:{}".format(record.split()[0],record.split()[1],protocol,current_traffic[record]))
