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


def get_interchange_transfer_bonus(df,sd,date,hour):
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
    interchange_transfer_bonus = {}
    for df_entry in range(0,int(len(subdf))):
        shortest_path = nx.dijkstra_path(G, subdf['Entry Station ID'][df_entry], subdf['Exit Station ID'][df_entry])
        colors = []
        for i in range(0,len(shortest_path)):
            colors.append(nx.get_node_attributes(G2,'color')[shortest_path[i]])
            if 'red' in colors and 'green' in colors and 'yellow' in colors:
                interchange_index = len(colors)-colors[::-1].index('yellow')-1
                
                if shortest_path[interchange_index] in interchange_transfer_bonus:   
                    interchange_transfer_bonus[shortest_path[interchange_index]] += subdf['Ridership NSEWL'][df_entry]
                else:
                    interchange_transfer_bonus[shortest_path[interchange_index]] = subdf['Ridership NSEWL'][df_entry]

    print(interchange_transfer_bonus)
    return(interchange_transfer_bonus)    


def generate_report(interchange_transfer_bonus_dict,date,hour): 

    interchange_transfer_df = pd.DataFrame([list(interchange_transfer_bonus_dict.values())],columns=list(interchange_transfer_bonus_dict.keys()))
    interchange_transfer_df['date'] = date
    interchange_transfer_df['hour'] = hour
    return(interchange_transfer_df)


start_date = datetime.date(2021,3,1)
end_date = datetime.date(2021,3,31)
delta = datetime.timedelta(days=1)
list_of_dates = []
list_of_hours = [7,15,18]
list_of_reports = []
while start_date <= end_date:
    list_of_dates.append(str(start_date))
    start_date += delta
    
for date in list_of_dates:
    for hour in list_of_hours:
        try:
            interchange_transfer_bonus_dict = get_interchange_transfer_bonus(df, sd, date, hour)
            list_of_reports.append(generate_report(interchange_transfer_bonus_dict,date,hour))
        except:
            print(str(date)+str(hour)+' not available.')

df = pd.concat(list_of_reports)
df.to_excel("interchange_transfer_bonus.xlsx") 