# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 16:46:47 2021

@author: jooer
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import random
import pandas as pd

# G = nx.Graph()
# G.add_edge(1,2,color='r',weight=2)
# G.add_edge(2,3,color='b',weight=4)
# G.add_edge(3,4,color='g',weight=6)

# pos = nx.circular_layout(G)

# edges = G.edges()
# colors = [G[u][v]['color'] for u,v in edges]
# weights = [G[u][v]['weight'] for u,v in edges]

# nx.draw(G, pos, edges=edges, edge_color=colors, width=weights)



def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(200, 200), dpi=40)
    plt.axis('off')
    fig = plt.figure(1)
    edges = graph.edges()
    weights = [graph[u][v]['weight'] for u,v in edges]
    d = dict(graph.degree)
    pos = nx.get_node_attributes(graph,'pos')
    node_colors = nx.get_node_attributes(graph,'color')
    edge_colors = nx.get_edge_attributes(graph, 'color')
    nx.draw_networkx_nodes(graph,pos,nodelist=d.keys(), node_size=[v * 100 for v in d.values()],node_color=[v for v in node_colors.values()])
    nx.draw_networkx_edges(graph,pos,width=weights,connectionstyle="arc3,rad=0.9",edge_color=[v for v in edge_colors.values()])
    nx.draw_networkx_labels(graph,pos)

    cut = 1.1
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(-xmax, xmax)
    plt.ylim(-ymax, ymax)

    plt.savefig(file_name)
    pylab.close()
    del fig




# df = pd.read_excel('sample2.xlsx')  
# print(df)
# df = df[['ridership','hour','entry_id','exit_id']]
# df.to_pickle("./sample.pkl")
df = pd.read_pickle("./sample.pkl")

df = df.groupby(['entry_id', 'exit_id','hour'])[['ridership']].agg('sum')
df = df.reset_index()
df = df[df['hour'] == 19]
df = df.reset_index()

G = nx.DiGraph()
node_positions = {}
for node in df['entry_id']:
    node_positions[node] = (node*2,node*2)   #fix the position to something more like actual layout
    node_positions[999] = (0,0)         #some kind of workaround for the random node 999

node_colors = {}
for node in df['entry_id']:
    if node >= 0 and node < 162:
        node_colors[node] = 'green'
    if  node >= 162:
        node_colors[node] = 'red'  
    node_colors[999] = 'red'       #some kind of workaround for the random node 999

list_of_nodes = []
for station in df['entry_id']:
    if station not in list_of_nodes:
        G.add_node(station,pos=node_positions[station])
        G.add_node(station,color=node_colors[station])
    G.add_node(999,pos=node_positions[station])     #some kind of workaround for the random node 999
    G.add_node(999,color=node_colors[station])     #some kind of workaround for the random node 999

for df_entry in range(1,int(len(df))):
    G.add_edge(df['entry_id'][df_entry],df['exit_id'][df_entry],weight=df['ridership'][df_entry])
    

for edge in G.edges:
    if G.edges[edge[0],edge[1]]['weight'] > 0 and G.edges[edge[0],edge[1]]['weight']  <= 100:
        G.add_edge(edge[0],edge[1], color='palegreen')
    if G.edges[edge[0],edge[1]]['weight']  > 100 and G.edges[edge[0],edge[1]]['weight']  <= 200:
        G.add_edge(edge[0],edge[1], color='yellow')
    if G.edges[edge[0],edge[1]]['weight']  > 200 and G.edges[edge[0],edge[1]]['weight']  <= 300:
        G.add_edge(edge[0],edge[1], color='orange')
    if G.edges[edge[0],edge[1]]['weight']  > 300 and G.edges[edge[0],edge[1]]['weight']  <= 400:
        G.add_edge(edge[0],edge[1], color='red')
    if G.edges[edge[0],edge[1]]['weight']  > 500:
        G.add_edge(edge[0],edge[1], color='black')
        

print('Number of nodes = ' + str(G.number_of_nodes()))
print('Number of edges = ' + str(G.number_of_edges()))



# pos=nx.circular_layout(G,scale=0.1,center=(0.5,0.5),dim=2)

# labels = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
# nx.draw(G, pos=pos)
# plt.show()

#Assuming that the graph g has nodes and edges entered
save_graph(G,"my_graph.pdf")


############################################################################################
# G = nx.Graph()
# list_of_nodes = [1,2,3,4,5,6,7,8,9,10,11,100]
# list_of_edges = []
# list_of_weighted_edges = []

# for station in list_of_nodes:
#     G.add_edge(station,station+1,weight=random.randint(2, 4))


# # list_of_edges = [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10)]    #think of a way to generate this 


    
# G.add_nodes_from(list_of_nodes)
# # G.add_edges_from(list_of_edges)
# # G.add_weighted_edges_from(list_of_weighted_edges)

# print('Number of nodes = ' + str(G.number_of_nodes()))
# print('Number of edges = ' + str(G.number_of_edges()))

# pos=nx.circular_layout(G,scale=0.1,center=(0.5,0.5),dim=2)

# labels = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
# nx.draw(G, pos=pos)
# plt.show()