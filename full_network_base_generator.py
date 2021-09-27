# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 09:23:23 2021

@author: jooer
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import pandas as pd
import datetime



sd = pd.read_excel('station_details.xlsx') 
sd.to_pickle("./station_details_full.pkl")
sd = pd.read_pickle("./station_details_full.pkl")


def generate_graph(sd):
    #select a specific date and time from the df

    #instantiate graph

    G2 = nx.DiGraph()
    
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
    
    ne_stations = sd[['Entry Station ID','NE ID']]
    ne_stations = ne_stations[ne_stations['NE ID'] !='x']
    ne_stations = ne_stations.sort_values(['NE ID'], ascending=[1])
    
    cc_stations = sd[['Entry Station ID','CC ID']]
    cc_stations = cc_stations[cc_stations['CC ID'] !='x']
    cc_stations = cc_stations.sort_values(['CC ID'], ascending=[1])
    
    ce_stations = sd[['Entry Station ID','CE ID']]
    ce_stations = ce_stations[ce_stations['CE ID'] !='x']
    ce_stations = ce_stations.sort_values(['CE ID'], ascending=[1])
    
    dt_stations = sd[['Entry Station ID','DT ID']]
    dt_stations = dt_stations[dt_stations['DT ID'] !='x']
    dt_stations = dt_stations.sort_values(['DT ID'], ascending=[1])
    
    #add node positions for visuals  
    node_positions = {}
    for sd_entry in range(0,len(sd)):
        node_positions[sd['Entry Station ID'][sd_entry]] = (sd['X'][sd_entry]/100,sd['Y'][sd_entry]/100)
    for station in node_positions:

        G2.add_node(station,pos=node_positions[station])  
    #assign attributes
    for sd_entry in range(0,len(sd)):
        node_color[sd['Entry Station ID'][sd_entry]] = sd['color'][sd_entry]
    for station in node_color:
 
        G2.add_node(station,color=node_color[station])   
        
    #add base edges to graph - ensure strong connected  
    base_edges = []
    
    list_ew_stations = list(ew_stations['Entry Station ID'])
    for i in range(0,len(list_ew_stations)):
        if list_ew_stations[i] not in [list_ew_stations[len(list_ew_stations)-1]]: #terminal stations
            G2.add_edge(list_ew_stations[i],list_ew_stations[i+1], color_base='green', weight=1)
            base_edges.append((list_ew_stations[i],list_ew_stations[i+1]))
    for i in range(len(list_ew_stations)-1,0,-1):
        if list_ew_stations[i] not in [list_ew_stations[0]]: #terminal stations
            G2.add_edge(list_ew_stations[i],list_ew_stations[i-1], color_base='green', weight=1)
            base_edges.append((list_ew_stations[i],list_ew_stations[i-1]))
            
    list_ns_stations = list(ns_stations['Entry Station ID'])
    for i in range(0,len(list_ns_stations)):
        if list_ns_stations[i] not in [list_ns_stations[len(list_ns_stations)-1]]: #terminal stations
            G2.add_edge(list_ns_stations[i],list_ns_stations[i+1], color_base='red', weight=1)
            base_edges.append((list_ns_stations[i],list_ns_stations[i+1]))
    for i in range(len(list_ns_stations)-1,0,-1):
        if list_ns_stations[i] not in [list_ns_stations[0]]: #terminal stations
            G2.add_edge(list_ns_stations[i],list_ns_stations[i-1], color_base='red', weight=1)
            base_edges.append((list_ns_stations[i],list_ns_stations[i-1]))
            
    list_ca_stations = list(ca_stations['Entry Station ID'])
    for i in range(0,len(list_ca_stations)):
        if list_ca_stations[i] not in [list_ca_stations[len(list_ca_stations)-1]]: #terminal stations
            G2.add_edge(list_ca_stations[i],list_ca_stations[i+1], color_base='green', weight=1)
            base_edges.append((list_ca_stations[i],list_ca_stations[i+1]))
    for i in range(len(list_ca_stations)-1,0,-1):
        if list_ca_stations[i] not in [list_ca_stations[0]]: #terminal stations
            G2.add_edge(list_ca_stations[i],list_ca_stations[i-1], color_base='green', weight=1)
            base_edges.append((list_ca_stations[i],list_ca_stations[i-1]))
            
    list_ne_stations = list(ne_stations['Entry Station ID'])
    for i in range(0,len(list_ne_stations)):
        if list_ne_stations[i] not in [list_ne_stations[len(list_ne_stations)-1]]: #terminal stations
            G2.add_edge(list_ne_stations[i],list_ne_stations[i+1], color_base='purple', weight=1)
            base_edges.append((list_ne_stations[i],list_ne_stations[i+1]))
    for i in range(len(list_ne_stations)-1,0,-1):
        if list_ne_stations[i] not in [list_ne_stations[0]]: #terminal stations
            G2.add_edge(list_ne_stations[i],list_ne_stations[i-1], color_base='purple', weight=1)
            base_edges.append((list_ne_stations[i],list_ne_stations[i-1]))
            
    list_cc_stations = list(cc_stations['Entry Station ID'])
    for i in range(0,len(list_cc_stations)):
        if list_cc_stations[i] not in [list_cc_stations[len(list_cc_stations)-1]]: #terminal stations
            G2.add_edge(list_cc_stations[i],list_cc_stations[i+1], color_base='yellow', weight=1)
            base_edges.append((list_cc_stations[i],list_cc_stations[i+1]))
    for i in range(len(list_cc_stations)-1,0,-1):
        if list_cc_stations[i] not in [list_cc_stations[0]]: #terminal stations
            G2.add_edge(list_cc_stations[i],list_cc_stations[i-1], color_base='yellow', weight=1)
            base_edges.append((list_cc_stations[i],list_cc_stations[i-1]))
       
    list_ce_stations = list(ce_stations['Entry Station ID'])
    for i in range(0,len(list_ce_stations)):
        if list_ce_stations[i] not in [list_ce_stations[len(list_ce_stations)-1]]: #terminal stations
            G2.add_edge(list_ce_stations[i],list_ce_stations[i+1], color_base='yellow', weight=1)
            base_edges.append((list_ce_stations[i],list_ce_stations[i+1]))
    for i in range(len(list_ce_stations)-1,0,-1):
        if list_ce_stations[i] not in [list_ce_stations[0]]: #terminal stations
            G2.add_edge(list_ce_stations[i],list_ce_stations[i-1], color_base='yellow', weight=1)
            base_edges.append((list_ce_stations[i],list_ce_stations[i-1]))
    
    list_dt_stations = list(dt_stations['Entry Station ID'])
    for i in range(0,len(list_dt_stations)):
        if list_dt_stations[i] not in [list_dt_stations[len(list_dt_stations)-1]]: #terminal stations
            G2.add_edge(list_dt_stations[i],list_dt_stations[i+1], color_base='blue', weight=1)
            base_edges.append((list_dt_stations[i],list_dt_stations[i+1]))
    for i in range(len(list_dt_stations)-1,0,-1):
        if list_dt_stations[i] not in [list_dt_stations[0]]: #terminal stations
            G2.add_edge(list_dt_stations[i],list_dt_stations[i-1], color_base='blue', weight=1)
            base_edges.append((list_dt_stations[i],list_dt_stations[i-1]))
    
    #special edges for interchange stations
    G2.add_edge(106,202, color_base='black', weight=1) #serang
    G2.add_edge(63,333, color_base='black', weight=1) #expo
    G2.add_edge(207,324, color_base='black', weight=1) #macph
    G2.add_edge(35,208, color_base='black', weight=1) #paya
    G2.add_edge(301,31, color_base='black', weight=1) #bugis
    G2.add_edge(213,334, color_base='black', weight=1) #prom
    G2.add_edge(229,302, color_base='black', weight=1) #bayf
    G2.add_edge(228,13, color_base='black', weight=1) #marinabay
    G2.add_edge(111,316, color_base='black', weight=1) #little india
    G2.add_edge(3,204, color_base='black', weight=1) #bishan
    G2.add_edge(10,112, color_base='black', weight=1) #dhoby
    G2.add_edge(112,231, color_base='black', weight=1) #dhoby
    G2.add_edge(231,10, color_base='black', weight=1) #dhoby
    G2.add_edge(305,114, color_base='black', weight=1) #china
    G2.add_edge(115,15, color_base='black', weight=1) #outram
    G2.add_edge(116,227, color_base='black', weight=1) #harbour
    G2.add_edge(313,217, color_base='black', weight=1) #botanic
    G2.add_edge(41,330, color_base='black', weight=1) #tampines
    
    G2.add_edge(202,106, color_base='black', weight=1) #serang
    G2.add_edge(333,63, color_base='black', weight=1) #expo
    G2.add_edge(324,207, color_base='black', weight=1) #macph
    G2.add_edge(208,35, color_base='black', weight=1) #paya
    G2.add_edge(31,301, color_base='black', weight=1) #bugis
    G2.add_edge(334,213, color_base='black', weight=1) #prom
    G2.add_edge(302,229, color_base='black', weight=1) #bayf
    G2.add_edge(13,228, color_base='black', weight=1) #marinabay
    G2.add_edge(316,111, color_base='black', weight=1) #little india
    G2.add_edge(204,3, color_base='black', weight=1) #bishan
    G2.add_edge(112,10, color_base='black', weight=1) #dhoby
    G2.add_edge(231,112, color_base='black', weight=1) #dhoby
    G2.add_edge(10,231, color_base='black', weight=1) #dhoby
    G2.add_edge(114,305, color_base='black', weight=1) #china
    G2.add_edge(15,115, color_base='black', weight=1) #outram
    G2.add_edge(227,116, color_base='black', weight=1) #harbour
    G2.add_edge(217,313, color_base='black', weight=1) #botanic
    G2.add_edge(330,41, color_base='black', weight=1) #tampines
    
    
    return(G2,base_edges)    
   

def save_graph(graph,base_edges,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(150, 100), dpi=100)

    fig = plt.figure(1)

    pos = nx.get_node_attributes(graph,'pos')
    edges, colors = zip(*nx.get_edge_attributes(graph,'color_base').items())
    node_colors = nx.get_node_attributes(graph,'color')
    d = dict(graph.degree)

    nx.draw(graph, pos, edgelist=edges, edge_color=colors, width=15,alpha=0.2)
    # nx.draw(graph, pos, edgelist=edges, edge_color=weights.values(), width=[pow(v/max(weights.values()),3)*30 for v in weights.values()], edge_cmap = plt.cm.jet, 
    #         vmin = 0.0, vmax = max(weights.values()), alpha=0.9, connectionstyle="arc3,rad=0.2")

    nx.draw_networkx_nodes(graph,pos,nodelist=d.keys(), node_size=[300 for v in d.values()],node_color=[v for v in node_colors.values()])
    nx.draw_networkx_labels(graph,pos)
    # nx.draw_networkx_edges(graph,pos, edgelist=edges, width=[weight / 1 for weight in weights],connectionstyle=None,edge_color=[v for v in edge_colors.values()])
    # out = nx.draw(G,pos,edge_color = weights.values(), edge_cmap = plt.cm.jet, vmin = 0.0, vmax = max(weights.values()))


    cut = 1.3
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(40, xmax)
    plt.ylim(200, ymax)
   
    plt.savefig(file_name)
    pylab.close()
    del fig


def centrality_measures(G):
    #how to factor in the weights?
    nx.degree_centrality(G)
    nx.in_degree_centrality(G)
    nx.out_degree_centrality(G)
    nx.eigenvector_centrality(G)
    nx.closeness_centrality(G)
    nx.betweenness_centrality(G)
    nx.betweenness_centrality_source(G)
    nx.harmonic_centrality(G)
    nx.load_centrality(G)
    nx.voterank(G,10)
    nx.pagerank(G)
    
def generate_report(G): 
# Create some Pandas dataframes from some data.
    weights = nx.get_edge_attributes(G,'weight')
    edges, weight = zip(*nx.get_edge_attributes(G,'weight').items())
    general_details_df = pd.DataFrame({'number_of_nodes':[str(len(G.nodes()))],'number_of_edges':[str(len(G.edges()))],'number_of_trips':[str(sum(weights.values()))],'trip_range':[str(min(weights.values()))+"-"+str(max(weights.values()))]})
    degree_centrality_df = pd.DataFrame({'station_id':list(nx.degree_centrality(G).keys()),'degree_centrality':list(nx.degree_centrality(G).values())})
    weighted_degree_df = pd.DataFrame({'station_id':list(dict(G.degree(weight='weight')).keys()),'degree_centrality':list(dict(G.degree(weight='weight')).values())})
    weighted_out_degree_df = pd.DataFrame({'station_id':list(dict(G.out_degree(weight='weight')).keys()),'out_degree_centrality':list(dict(G.out_degree(weight='weight')).values())})
    weighted_in_degree_df = pd.DataFrame({'station_id':list(dict(G.in_degree(weight='weight')).keys()),'in_degree_centrality':list(dict(G.in_degree(weight='weight')).values())})
    in_degree_centrality_df = pd.DataFrame({'station_id':list(nx.in_degree_centrality(G).keys()),'in_degree_centrality':list(nx.in_degree_centrality(G).values())})
    out_degree_centrality_df = pd.DataFrame({'station_id':list(nx.out_degree_centrality(G).keys()),'out_degree_centrality':list(nx.out_degree_centrality(G).values())})
    edge_weight_df = pd.DataFrame({'edge_tuple':edges,'edge_weight':weight})
    eigenvector_centrality_df = pd.DataFrame({'station_id':list(nx.eigenvector_centrality(G,max_iter=600).keys()),'eigenvector_centrality':list(nx.eigenvector_centrality(G,max_iter=600).values())})
    # closeness_centrality_df = pd.DataFrame({'station_id':list(nx.closeness_centrality(G).keys()),'closeness_centrality':list(nx.closeness_centrality(G).values())})
    betweenness_centrality_df = pd.DataFrame({'station_id':list(nx.betweenness_centrality(G).keys()),'betweenness_centrality':list(nx.betweenness_centrality(G).values())})
    betweenness_centrality_source_df = pd.DataFrame({'station_id':list(nx.betweenness_centrality_source(G).keys()),'betweenness_centrality_source':list(nx.betweenness_centrality_source(G).values())})
    pagerank_df = pd.DataFrame({'station_id':list(nx.pagerank(G).keys()),'betweenness_centrality_source':list(nx.pagerank(G).values())})
    # harmonic_centrality_df = pd.DataFrame({'station_id':list(nx.harmonic_centrality(G).keys()),'harmonic_centrality':list(nx.harmonic_centrality(G).values())})
    # load_centrality_df = pd.DataFrame({'station_id':list(nx.load_centrality(G).keys()),'load_centrality':list(nx.load_centrality(G).values())})
    # voterank_df = pd.DataFrame({'key_stations:':nx.voterank(G)})


    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('base_centrality_report'+'.xlsx')
    
    # Write each dataframe to a different worksheet.
    general_details_df.to_excel(writer, sheet_name='general_details')
    degree_centrality_df.to_excel(writer, sheet_name='degree_centrality')
    weighted_degree_df.to_excel(writer, sheet_name='weighted_degree')
    weighted_out_degree_df.to_excel(writer, sheet_name='weighted_out_degree')
    weighted_in_degree_df.to_excel(writer, sheet_name='weighted_in_degree')
    in_degree_centrality_df.to_excel(writer, sheet_name='in_degree_centrality')
    out_degree_centrality_df.to_excel(writer, sheet_name='out_degree_centrality')
    edge_weight_df.to_excel(writer, sheet_name='edge_weights')
    eigenvector_centrality_df.to_excel(writer, sheet_name='eigenvector_centrality')
    # closeness_centrality_df.to_excel(writer, sheet_name='closeness_centrality')
    betweenness_centrality_df.to_excel(writer, sheet_name='betweenness_centrality')
    betweenness_centrality_source_df.to_excel(writer, sheet_name='betweenness_centrality_source')
    pagerank_df.to_excel(writer, sheet_name='pagerank_centrality')
    # harmonic_centrality_df.to_excel(writer, sheet_name='harmonic_centrality')
    # load_centrality_df.to_excel(writer, sheet_name='load_centrality')
    # voterank_df.to_excel(writer, sheet_name='voterank')

    
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    
G,base_edges = generate_graph(sd)
save_graph(G,base_edges,"FULL_MAP.png")
generate_report(G)