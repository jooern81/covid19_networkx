# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 09:21:21 2021

@author: jooer
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import random
import pandas as pd


# sd = pd.read_excel('station_details.xlsx') 
# sd.to_pickle("./station_details.pkl")
sd = pd.read_pickle("./station_details.pkl")
df = pd.read_pickle("./full.pkl")

#select a specific date and time from the df
date = '2020-01-26'
hour = 6
subdf = df[df['Business Date'] == date]
subdf = subdf[subdf['Entry Hour'] == hour]
subdf = subdf.groupby(['Entry Station ID', 'Exit Station ID'])[['Ridership NSEWL']].agg('sum')
subdf = subdf.reset_index()
subdf = pd.concat([subdf[subdf['Entry Station ID'].between(1, 48)],subdf[subdf['Entry Station ID'].between(63, 73)]])
subdf = pd.concat([subdf[subdf['Exit Station ID'].between(1, 48)],subdf[subdf['Exit Station ID'].between(63, 73)]])
subdf = subdf.reset_index()

#instantiate graph
G = nx.DiGraph()

#use dictionary to set line attribute for stations
node_color = {}

#get the stations from each line and sort them in their running order, paired with their entry/exit ID
ew_stations = sd[['Entry Station ID','EW ID']]
ew_stations = ew_stations[ew_stations['EW ID'] !='x']
ew_stations = ew_stations.sort_values(['EW ID'], ascending=[1])

ns_stations = sd[['Entry Station ID','NS ID']]
ns_stations = ns_stations[ns_stations['NS ID'] !='x']
ns_stations = ns_stations.sort_values(['NS ID'], ascending=[1])

ca_stations = sd[['Entry Station ID','CA ID']]
ca_stations = ca_stations[ca_stations['CA ID'] !='x']
ca_stations = ca_stations.sort_values(['CA ID'], ascending=[1])

#add node positions for visuals  
node_positions = {}
for sd_entry in range(0,len(sd)):
    node_positions[sd['Entry Station ID'][sd_entry]] = (sd['X'][sd_entry]/100,sd['Y'][sd_entry]/100)
for station in node_positions:
    G.add_node(station,pos=node_positions[station])  
        
#assign attributes
for sd_entry in range(0,len(sd)):
    node_color[sd['Entry Station ID'][sd_entry]] = sd['color'][sd_entry]
for station in node_color:
    G.add_node(station,color=node_color[station])   
    
# for station in red_line1:
#     node_line[station] = 'NSL'
#     node_color[station] = 'red'
#     G.add_node(station,pos=node_positions[station]) 
# for station in red_line2:
#     node_line[station] = 'NSL' 
#     node_color[station] = 'red'
#     G.add_node(station,pos=node_positions[station]) 

#notice that we break the red line into two, this is one way to create tidily create an interchange station later on

#add nodes to graph
# list_of_stations = [] #track the nodes added into the graph
# for station in subdf['Entry Station ID']:
#     if station not in list_of_stations:
#         list_of_stations.append(station)
#         G.add_node(station,line=node_line[station])

#add edges to graph    
# list_ew_stations = list(ew_stations['Entry Station ID'])
# for i in range(0,len(list_ew_stations)):
#     if list_ew_stations[i] not in [list_ew_stations[len(list_ew_stations)-1]]: #terminal stations
#         G.add_edge(list_ew_stations[i],list_ew_stations[i+1], color='green', weight=1)
        
# list_ns_stations = list(ns_stations['Entry Station ID'])
# for i in range(0,len(list_ns_stations)):
#     if list_ns_stations[i] not in [list_ns_stations[len(list_ns_stations)-1]]: #terminal stations
#         G.add_edge(list_ns_stations[i],list_ns_stations[i+1], color='red', weight=1)

# list_ca_stations = list(ca_stations['Entry Station ID'])
# for i in range(0,len(list_ca_stations)):
#     if list_ca_stations[i] not in [list_ca_stations[len(list_ca_stations)-1]]: #terminal stations
#         G.add_edge(list_ca_stations[i],list_ca_stations[i+1], color='green', weight=1)
        
#extra attention for interchange stations
# G.add_edge(229,72, color='red')
# G.add_edge(72,301, color='red')

#add in trip edges
for df_entry in range(0,int(len(subdf))):
    G.add_edge(subdf['Entry Station ID'][df_entry],subdf['Exit Station ID'][df_entry],weight=subdf['Ridership NSEWL'][df_entry])
#add in trip edges color

# for edge in G.edges:
#     if G.edges[edge[0],edge[1]]['weight'] > 1 and G.edges[edge[0],edge[1]]['weight']  <= 100:
#         G.add_edge(edge[0],edge[1], color='palegreen')
#     if G.edges[edge[0],edge[1]]['weight']  > 100 and G.edges[edge[0],edge[1]]['weight']  <= 200:
#         G.add_edge(edge[0],edge[1], color='yellow')
#     if G.edges[edge[0],edge[1]]['weight']  > 200 and G.edges[edge[0],edge[1]]['weight']  <= 300:
#         G.add_edge(edge[0],edge[1], color='orange')
#     if G.edges[edge[0],edge[1]]['weight']  > 300 and G.edges[edge[0],edge[1]]['weight']  <= 400:
#         G.add_edge(edge[0],edge[1], color='red')
#     if G.edges[edge[0],edge[1]]['weight']  > 500:
#         G.add_edge(edge[0],edge[1], color='black')
#         print(edge[0],edge[1])
        
def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(200, 200), dpi=100)
    plt.axis('off')
    fig = plt.figure(1)
    edges = graph.edges()
    weights = [graph[u][v]['weight'] for u,v in edges]
    max_weight = max(weights)
    weights2 = [pow(graph[u][v]['weight']/max_weight,3)*20 for u,v in edges]
    d = dict(graph.degree)
    pos = nx.get_node_attributes(graph,'pos')
    node_colors = nx.get_node_attributes(graph,'color')
    # edge_colors = nx.get_edge_attributes(graph, 'color')
    edges, colors = zip(*nx.get_edge_attributes(graph,'weight').items())
    # nx.draw_networkx_nodes(graph,pos,nodelist=d.keys(), node_size=[pow(v,2) for v in d.values()],node_color=[v for v in node_colors.values()])
    

    nx.draw(G, pos, edgelist=edges, edge_color=weights, width=weights2, edge_cmap = plt.cm.jet, vmin = 0.0, vmax = max(weights))
    nx.draw_networkx_nodes(graph,pos,nodelist=d.keys(), node_size=[300 for v in d.values()],node_color=[v for v in node_colors.values()])
    # nx.draw_networkx_edges(graph,pos, edgelist=edges, width=[weight / 1 for weight in weights],connectionstyle=None,edge_color=[v for v in edge_colors.values()])
    nx.draw_networkx_edge_labels(G,pos,edge_labels=nx.get_edge_attributes(G,'weight'))
    nx.draw_networkx_labels(graph,pos)

    cut = 1.1
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(-xmax, xmax)
    plt.ylim(-ymax, ymax)
   
    plt.savefig(file_name)
    pylab.close()
    del fig
    
save_graph(G,"mrt_"+date+"_"+str(hour)+'.pdf')

def centrality_measures(G):
    nx.degree_centrality(G)
    nx.in_degree_centrality(G)
    nx.out_degree_centrality(G)
    nx.eigenvector_centrality(G)
    nx.closeness_centrality(G)
    nx.betweenness_centrality(G)
    nx.betweenness_centrality_source(G)
    nx.harmonic_centrality(G)
    nx.voterank(G,10)
    
    