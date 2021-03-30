import networkx as nx
import matplotlib.pyplot as plt
import collections
import argparse, sys
import os
# Para ejecutar (se puede cambiar el archivo por cualquier otro): python3 pininos.py --file ./data/repeated_10_scale_33/996782_repeated10_scale33.graphml
# IMPORTANTE: mi script asume la existencia de una carpeta de "data" en su mismo nivel, pero pueden cambiar el archivo explorado con la bandera "file", con los archivos que acordamos descomprimidos
# Descripción: saca las gráficas de los parámetros que son posibles obtener
    # Grade distribution
    # Clustering coefficient
    # Diameter (como hay independencia de componentes, es infinito)
    # Edge Betweenness (hay un problema con el calculo, puede verse en los comentarios)
parser=argparse.ArgumentParser()
# in this case: ./data/repeated_10_scale_33/996782_repeated10_scale33.graphml
parser.add_argument('--file', help='Graphml location to interpret')
args=parser.parse_args()

def printDiameter(network):
    try:
        diameter = nx.diameter(network)
        print('Diameter: ' + diameter)
    except nx.NetworkXError:
        print ('Infinite Diameter')
    else:
        print('Error calculating diameter')

def dictionaryToTupleXY(dictToConvert):
    x, y = zip(*dictToConvert.items())
    return (x, y)

def getBetweennessCentralityXYTuple(network):
    try:
        dictionaryBc = nx.betweenness_centrality(network)
        return dictionaryToTupleXY(dictionaryBc)
    except nx.NetworkXError:
        print ('Hello')
    else:
        print('Error calculating betweenness centrality')

def getClusteringCoefficientXYTuple(network):
    try:
        dictionaryBc = nx.clustering(network)
        return dictionaryToTupleXY(dictionaryBc)
    except nx.NetworkXError:
        print ('Hello')
    else:
        print('Error calculating betweenness centrality')

def getEdgeBetweennessCentrality(network):
    try:
        dictionaryBc = nx.edge_betweenness_centrality(network)
        print(dictionaryBc)
        exit()
        return dictionaryToTupleXY(dictionaryBc)
    except nx.NetworkXError:
        print ('Hello')
    else:
        print('Error calculating betweenness centrality')

def graphDictionary(x, y, title="Title", xlabel="x", ylabel="y"):
    fig, ax = plt.subplots()
    plt.bar(x, y, width=0.80, color="b")
    plt.title(title)
    plt.ylabel(xlabel)
    plt.xlabel(ylabel)
    ax.set_xticks([float(d) + float(0.4) for d in x])
    ax.set_xticklabels(x)


graphml = nx.read_graphml(args.file)
options = {
    'node_color': 'blue',
    'node_size': 100,
    'width': 1.5,
    'arrowstyle': '-|>',
    'arrowsize': 12,
}
degrees = [d for n, d in graphml.degree()]
sortedDegreesDesc = sorted(degrees, reverse=True)
degreeCount = collections.Counter(sortedDegreesDesc)
deg, cnt = zip(*degreeCount.items())
#parametros
printDiameter(graphml)
graphDictionary(deg, cnt, title="Degree Distribution", xlabel="Grades", ylabel="Quantity")

toupleXYBetwennessCentraily = getBetweennessCentralityXYTuple(graphml)
graphDictionary(toupleXYBetwennessCentraily[0], toupleXYBetwennessCentraily[1], title="Betweenness Centrality", xlabel="Node", ylabel='BCentrality')

toupleXYClusteringCoefficient = getClusteringCoefficientXYTuple(graphml)
graphDictionary(toupleXYClusteringCoefficient[0], toupleXYClusteringCoefficient[1], title="Clustering Coefficients", xlabel="Node", ylabel='CCoeficients')

#This is like "where to where", so I can't graph it normally, I may assign name to the connection?
# toupleXYEdgeBetweennessCentrality = getEdgeBetweennessCentrality(graphml)
# graphDictionary(toupleXYEdgeBetweennessCentrality[0], toupleXYEdgeBetweennessCentrality[1], title="Edge Betweenness Centrality", xlabel="connection", ylabel='EBCentrality')

plt.show()

# graph = nx.draw(graphml, arrows=True, **options)
# plt.show()