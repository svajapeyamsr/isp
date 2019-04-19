import requests, json
import networkx as nx
import matplotlib.pyplot as plt

TOPOLOGY_IMAGE= 'static/topology.png'
CONTROLLER_IP= "172.16.3.1"

switches= []
links_info= []


def non_duplicate(links_info):
    final_links_info= []
    
    for element in links_info:
        this_tuple= element
        duplicate_tuple= (element[1], element[0],
                          {'src_port': element[2]['dst_port'],
                          'dst_port': element[2]['src_port'],
                          'status': element[2]['status']})
        
        #first iteration
        if(len(final_links_info))== 0:
            final_links_info.append(element)
        
        #exact duplicate
        elif this_tuple in final_links_info:
            continue
        
        #interchanged duplicate
        elif duplicate_tuple in final_links_info:
            continue
        
    return(final_links_info)



def get_topo_info():

    #link_dict_str= requests.get("http://{}:8080/misc/link_dict".format(CONTROLLER_IP))
    link_dict_str= '''{"7610470746945": {"2": [270559499225422, 2, true]}, "270559499225422": {"2": [7610470746945, 2, true]}}'''
    
    
    link_dict= json.loads(link_dict_str)
    
    
    for dpid in link_dict.items():
        switches.append(dpid[0])
        
        source_ports= []
        dest_ports= []
        dest_dpids= []
        link_status= []
        
        source_dpid= dpid[0]
        dest_items= dpid[1]
        
        for item in dest_items.items():
            source_ports.append(item[0])
            dest_dpids.append(item[1][0])
            dest_ports.append(item[1][1])
            
            if item[1][2]== True:
                link_status.append("UP")
            else:
                link_status.append("DOWN")
                
        
        
        for i in range(0, len(source_ports)):
            links_info.append((source_dpid, dest_dpids[i],
                              {'src_port': source_ports[i],
                               'dst_port': dest_ports[i],
                               'status': link_status[i]}))
            


    final_links_info= non_duplicate(links_info)
        
    return(switches, final_links_info)

def check_link_status(links):
    up_links= []
    down_links= []
    for link in links:
        status = link[-1]['status']
        if status== "UP":
            up_links.append(link)
        
        elif status== "DOWN":
            down_links.append(link)
    return up_links, down_links


def get_edge_labels(links, label_name):
    labels_dict = {}
    for link in links:
        # graph edges = (tail, head) = (dst_dpid, src_dpid)
        labels_dict[(link[1], link[0])]= link[2][label_name]
    return labels_dict


def set_edge_labels(G, pos, edge_labels, label_pos):
    nx.draw_networkx_edge_labels(G, pos, edge_labels= edge_labels,
    label_pos= label_pos)



def draw_nodes(G, switches):
    G.add_nodes_from(switches)
    global pos
    pos= nx.spring_layout(G)         # positions for all nodes
    nx.draw_networkx_nodes(G, pos, node_shape= 's', labels= True,
        nodelist= switches, node_color= 'skyblue', node_size= 6000,
        edgecolors= 'k')


def draw_edges(G, links):
    G.add_edges_from(links)
    up_links, down_links= check_link_status(links)
    nx.draw_networkx_edges(G, pos, edgelist= up_links, edge_color= 'g')
    nx.draw_networkx_edges(G, pos, edgelist= down_links, edge_color= 'r')


def draw_labels(G, links):
    nx.draw_networkx_labels(G, pos, font_size = 10, font_family='sans-serif')
    src_ports = get_edge_labels(links, 'src_port')
    set_edge_labels(G, pos, src_ports, 0.2)
    dst_ports = get_edge_labels(links, 'dst_port')
    set_edge_labels(G, pos, dst_ports, 0.8)

def draw_topology(switches, links):
    G= nx.MultiGraph()
    plt.figure(num= TOPOLOGY_IMAGE, figsize= (12,12), dpi= 80, edgecolor= 'k')
    draw_nodes(G, switches)
    draw_edges(G, links)
    draw_labels(G, links)
    plt.axis('off')
    plt.savefig(TOPOLOGY_IMAGE)
    print("Saved the network topology as {}".format(TOPOLOGY_IMAGE))



def graph_topo_info():
    switches, links= get_topo_info()
    if switches:
        draw_topology(switches, links)


if __name__ == "__main__":
    switches, links= get_topo_info()
    if switches:
        draw_topology(switches, links)

