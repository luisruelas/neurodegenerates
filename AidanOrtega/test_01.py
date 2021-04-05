#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 03:06:32 2021

@author: aidanortega
"""
import collections
import matplotlib.pyplot as plt
import networkx as nx

#Leemos la red desde un graphml
g = nx.read_graphml("repeated_10_scale_33/996782_repeated10_scale33.graphml")

#Imprimimos la cantidad de nodos y enlaces
nodos = g.nodes()
enlaces = g.edges()
print("# Nodos : {}".format(nodos))
print("# Enlaces : {}".format(enlaces))

#Visualizamos la composición default de la red
nx.draw(g)


# # Cálculo del camino más corto promeedio
# prom_caminos = nx.average_shortest_path_length(g)
# print("Camino más corto promedio : {}".format(prom_caminos))

# #Cálculo del diámetro de la red
# diametro = nx.diameter(g)
# print("Diámetro de la red : {}".format(diametro))

#Cálculo de los componentes principales
componentes = nx.number_connected_components(g)
my_concomp = nx.connected_components(g)

S = [g.subgraph(c).copy() for c in my_concomp]

#Cálculo del clustering coeficient (coeficiente de agrupamiento)
clust_coef = nx.average_clustering(g)

#Cálculo del grado de la red
grados = nx.degree(g)

#Cálculo del de medidas de centralidad
#Betweeness centrality
bet_cent = nx.betweenness_centrality(g)
print("Betweeness Centrality : {}".format(bet_cent))

#Edge betweeness 
edg_bet = nx.edge_betweenness(g)
print("Edge Betweeness: {}".format(edg_bet))

#Clustering
clust = nx.clustering(g)
print("Clustering : {}".format(clust))

#Distribución de grado

degree_sequence = sorted([d for n, d in g.degree()], reverse=True)  # degree sequence
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())

fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color="b")

plt.title("Degree Histogram")
plt.ylabel("Count")
plt.xlabel("Degree")
ax.set_xticks([d + 0.4 for d in deg])
ax.set_xticklabels(deg)

# # draw graph in inset
# plt.axes([0.4, 0.4, 0.5, 0.5])
# Gcc = g.subgraph(sorted(nx.connected_components(), key=len, reverse=True)[0])
# pos = nx.spring_layout(g)
# plt.axis("off")
# nx.draw_networkx_nodes(g, pos, node_size=20)
# nx.draw_networkx_edges(g, pos, alpha=0.4)
# plt.show()
