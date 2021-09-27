# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 09:21:21 2021

@author: jooer
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import pandas as pd
import datetime


# sd = pd.read_excel('station_details.xlsx') 
# sd.to_pickle("./station_details.pkl")
sd = pd.read_pickle("./station_details.pkl")
df = pd.read_pickle("./full.pkl")
df2 = pd.read_pickle("./expansion1.pkl")
df3 = pd.read_pickle("./expansion2.pkl")
df = pd.concat([df,df2,df3])


def generate_graph(df,sd,date,hour):
    #select a specific date and time from the df

    subdf = df[df['Business Date'] == date]
    subdf = subdf[subdf['Entry Hour'] == hour]
    subdf = subdf.groupby(['Entry Station ID', 'Exit Station ID'])[['Ridership NSEWL']].agg('sum')
    subdf = subdf.reset_index()
    subdf = pd.concat([subdf[subdf['Entry Station ID'].between(1, 48)],subdf[subdf['Entry Station ID'].between(63, 73)]])
    subdf = pd.concat([subdf[subdf['Exit Station ID'].between(1, 48)],subdf[subdf['Exit Station ID'].between(63, 73)]])
    subdf = subdf[subdf['Ridership NSEWL'].between(0, max(subdf['Ridership NSEWL']))]
    subdf = subdf.reset_index()
    
    #instantiate graph
    # G_base = nx.DiGraph()
    G = nx.DiGraph()
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
    
    #add node positions for visuals  
    node_positions = {}
    for sd_entry in range(0,len(sd)):
        node_positions[sd['Entry Station ID'][sd_entry]] = (sd['X'][sd_entry]/100,sd['Y'][sd_entry]/100)
    for station in node_positions:
        G.add_node(station,pos=node_positions[station])  
        G2.add_node(station,pos=node_positions[station])  
    #assign attributes
    for sd_entry in range(0,len(sd)):
        node_color[sd['Entry Station ID'][sd_entry]] = sd['color'][sd_entry]
    for station in node_color:
        G.add_node(station,color=node_color[station])   
        G2.add_node(station,color=node_color[station])   
    #add edges to graph - ensure strong connected  
    list_ew_stations = list(ew_stations['Entry Station ID'])
    for i in range(0,len(list_ew_stations)):
        if list_ew_stations[i] not in [list_ew_stations[len(list_ew_stations)-1]]: #terminal stations
            G.add_edge(list_ew_stations[i],list_ew_stations[i+1], color='green', weight=1)
    for i in range(len(list_ew_stations)-1,0,-1):
        if list_ew_stations[i] not in [list_ew_stations[0]]: #terminal stations
            G.add_edge(list_ew_stations[i],list_ew_stations[i-1], color='green', weight=1)
            
    list_ns_stations = list(ns_stations['Entry Station ID'])
    for i in range(0,len(list_ns_stations)):
        if list_ns_stations[i] not in [list_ns_stations[len(list_ns_stations)-1]]: #terminal stations
            G.add_edge(list_ns_stations[i],list_ns_stations[i+1], color='red', weight=1)
    for i in range(len(list_ns_stations)-1,0,-1):
        if list_ns_stations[i] not in [list_ns_stations[0]]: #terminal stations
            G.add_edge(list_ns_stations[i],list_ns_stations[i-1], color='red', weight=1)
            
    list_ca_stations = list(ca_stations['Entry Station ID'])
    for i in range(0,len(list_ca_stations)):
        if list_ca_stations[i] not in [list_ca_stations[len(list_ca_stations)-1]]: #terminal stations
            G.add_edge(list_ca_stations[i],list_ca_stations[i+1], color='green', weight=1)
    for i in range(len(list_ca_stations)-1,0,-1):
        if list_ca_stations[i] not in [list_ca_stations[0]]: #terminal stations
            G.add_edge(list_ca_stations[i],list_ca_stations[i-1], color='green', weight=1)
    
    #get edge weight dictionary
    network_edge_weights = {}
    for df_entry in range(0,int(len(subdf))):
        shortest_path = nx.dijkstra_path(G, subdf['Entry Station ID'][df_entry], subdf['Exit Station ID'][df_entry])
        for i in range(0,len(shortest_path)-1):
            if (shortest_path[i],shortest_path[i+1]) in network_edge_weights:
                network_edge_weights[(shortest_path[i],shortest_path[i+1])] += subdf['Ridership NSEWL'][df_entry]
            else:
                network_edge_weights[(shortest_path[i],shortest_path[i+1])] = subdf['Ridership NSEWL'][df_entry]
    
    for edge in network_edge_weights.keys():
        G2.add_edge(edge[0],edge[1],weight=network_edge_weights[edge])
    
    return(G2)    


def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(150, 100), dpi=100)

    fig = plt.figure(1)
    weights = nx.get_edge_attributes(graph,'weight')
    pos = nx.get_node_attributes(graph,'pos')
    edges, colors = zip(*nx.get_edge_attributes(graph,'weight').items())
    node_colors = nx.get_node_attributes(graph,'color')
    d = dict(graph.degree)
    # colors_base = nx.get_edge_attributes(graph,'color')
    # nx.draw(graph, pos, edgelist=edges, edge_color=[v for v in colors_base.values()], width=[5 for v in weights.values()])
    nx.draw(graph, pos, edgelist=edges, edge_color=weights.values(), width=[pow(v/max(weights.values()),3)*30 for v in weights.values()], edge_cmap = plt.cm.jet, 
            vmin = 0.0, vmax = max(weights.values()),connectionstyle="arc3,rad=0.1")
    sm = plt.cm.ScalarMappable(cmap=plt.cm.jet, norm=plt.Normalize(vmin = 0.0, vmax = max(weights.values())))
    sm._A = []
    cbar = plt.colorbar(sm,shrink=0.3,pad=0.001)
    cbar.ax.tick_params(labelsize=100)
    nx.draw_networkx_nodes(graph,pos,nodelist=d.keys(), node_size=[300 for v in d.values()],node_color=[v for v in node_colors.values()])
    nx.draw_networkx_labels(graph,pos)

    cut = 1.3
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(40, xmax)
    plt.ylim(200, ymax)
   
    plt.savefig(file_name)
    pylab.close()
    del fig
    
    # print("Number of Nodes: " + str(len(graph.nodes())))
    # print("Number of Edges: " + str(len(graph.edges())))
    # print("Number of Trips: " + str(sum(weights.values())))
    # print("Trip Range: " + str(min(weights.values()))+"-"+str(max(weights.values())))

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
    
def generate_report(G,date,hour): 
# Create some Pandas dataframes from some data.
    # print(list(nx.degree_centrality(G).keys()))
    
    weights = nx.get_edge_attributes(G,'weight')
    general_details_df = pd.DataFrame({'number_of_nodes':[str(len(G.nodes()))],'number_of_edges':[str(len(G.edges()))],'number_of_trips':[str(sum(weights.values()))],'trip_range':[str(min(weights.values()))+"-"+str(max(weights.values()))]})
    degree_centrality_df = pd.DataFrame({'station_id':list(nx.degree_centrality(G).keys()),'degree_centrality':list(nx.degree_centrality(G).values())})
    weighted_degree_df = pd.DataFrame({'station_id':list(dict(G.degree(weight='weight')).keys()),'degree_centrality':list(dict(G.degree(weight='weight')).values())})
    weighted_out_degree_df = pd.DataFrame({'station_id':list(dict(G.out_degree(weight='weight')).keys()),'out_degree_centrality':list(dict(G.out_degree(weight='weight')).values())})
    weighted_in_degree_df = pd.DataFrame({'station_id':list(dict(G.in_degree(weight='weight')).keys()),'in_degree_centrality':list(dict(G.in_degree(weight='weight')).values())})
    in_degree_centrality_df = pd.DataFrame({'station_id':list(nx.in_degree_centrality(G).keys()),'in_degree_centrality':list(nx.in_degree_centrality(G).values())})
    out_degree_centrality_df = pd.DataFrame({'station_id':list(nx.out_degree_centrality(G).keys()),'out_degree_centrality':list(nx.out_degree_centrality(G).values())})
    eigenvector_centrality_df = pd.DataFrame({'station_id':list(nx.eigenvector_centrality(G,max_iter=5000).keys()),'eigenvector_centrality':list(nx.eigenvector_centrality(G,max_iter=5000).values())})
    closeness_centrality_df = pd.DataFrame({'station_id':list(nx.closeness_centrality(G).keys()),'closeness_centrality':list(nx.closeness_centrality(G).values())})
    betweenness_centrality_df = pd.DataFrame({'station_id':list(nx.betweenness_centrality(G).keys()),'betweenness_centrality':list(nx.betweenness_centrality(G).values())})
    betweenness_centrality_source_df = pd.DataFrame({'station_id':list(nx.betweenness_centrality_source(G).keys()),'betweenness_centrality_source':list(nx.betweenness_centrality_source(G).values())})
    harmonic_centrality_df = pd.DataFrame({'station_id':list(nx.harmonic_centrality(G).keys()),'harmonic_centrality':list(nx.harmonic_centrality(G).values())})
    load_centrality_df = pd.DataFrame({'station_id':list(nx.load_centrality(G).keys()),'load_centrality':list(nx.load_centrality(G).values())})
    voterank_df = pd.DataFrame({'key_stations:':nx.voterank(G)})


    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('centrality_report2_'+date+'_'+str(hour)+'.xlsx')
    
    # Write each dataframe to a different worksheet.
    general_details_df.to_excel(writer, sheet_name='general_details')
    degree_centrality_df.to_excel(writer, sheet_name='degree_centrality')
    weighted_degree_df.to_excel(writer, sheet_name='weighted_degree')
    weighted_out_degree_df.to_excel(writer, sheet_name='weighted_out_degree')
    weighted_in_degree_df.to_excel(writer, sheet_name='weighted_in_degree')
    in_degree_centrality_df.to_excel(writer, sheet_name='in_degree_centrality')
    out_degree_centrality_df.to_excel(writer, sheet_name='out_degree_centrality')
    eigenvector_centrality_df.to_excel(writer, sheet_name='eigenvector_centrality')
    closeness_centrality_df.to_excel(writer, sheet_name='closeness_centrality')
    betweenness_centrality_df.to_excel(writer, sheet_name='betweenness_centrality')
    betweenness_centrality_source_df.to_excel(writer, sheet_name='betweenness_centrality_source')
    harmonic_centrality_df.to_excel(writer, sheet_name='harmonic_centrality')
    load_centrality_df.to_excel(writer, sheet_name='load_centrality')
    voterank_df.to_excel(writer, sheet_name='voterank')

    
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

start_date = datetime.date(2020,9,27)
end_date = datetime.date(2020,9,27)
delta = datetime.timedelta(days=1)
list_of_dates = []
list_of_hours = [7,15,18]
while start_date <= end_date:
    list_of_dates.append(str(start_date))
    start_date += delta
    
for date in list_of_dates:
    for hour in list_of_hours:
        try:
            G = generate_graph(df, sd, date, hour)
            save_graph(G,"mrt_base2_"+date+"_"+str(hour)+'.pdf')
            generate_report(G,date,hour)
        except:
            print(str(date)+str(hour)+' not available.')
