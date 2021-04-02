import networkx as nx
import matplotlib.pyplot as plt
import collections
import argparse, sys
import os
from progress.bar import Bar
# Para ejecutar (se puede cambiar el folder): python3 pininos.py --folder ./data/repeated_10_scale_33/
# Las instrucciones las redacté con ahinco :V, favor de usar: python3 pininos.py --help
# Si tienen un xml, pueden usarlo en lugar de cargar el folder y esperar una eternidad
# OJO tenemos el parametro "limit" (--limit), con el cual le indicamos el numero de archivos que estamos dispuestos a utilizar, son 1064, si quieren quemar su compu o tienen tiempo dejenlo en blanco, si no, ponganle unos 10
parser=argparse.ArgumentParser()
# in this case: ./data/repeated_10_scale_33/996782_repeated10_scale33.graphml
parser.add_argument('--folder', help='Folder containing the files to use')
parser.add_argument('--limit', help='For testing, limit the numbers of file we will get')
parser.add_argument('--input', help='If you already have an xml file to use, stop suffering, use it')
parser.add_argument('--output', help='Optional output for file')

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

fullGraphml = None
cont = 0
if (args.folder):
    for dirpath, dirs, files in os.walk(args.folder):
        print('Processing folder: '+dirpath)
        bar = Bar('Processing', max= len(files) if not args.limit else int(args.limit))
        for f in files:
            if(args.limit):
                cont+=1
                if (int(args.limit) < cont):
                    break
            graphml = nx.read_graphml(os.path.join(dirpath, f))
            if not fullGraphml:
                fullGraphml = graphml
            else:
                nx.compose(fullGraphml, graphml)
            bar.next()
        bar.finish()
    if args.output:
        print('Printing file: ' + args.output)
        nx.write_gexf(fullGraphml, args.output)
elif (args.input):
    fullGraphml = nx.read_gexf(args.input)
else:
    print('We need some substance here pal, specify input or folder')
    exit()

options = {
    'node_color': 'blue',
    'node_size': 100,
    'width': 1.5,
    'arrowstyle': '-|>',
    'arrowsize': 5,
}

degrees = [d for n, d in fullGraphml.degree()]
sortedDegreesDesc = sorted(degrees, reverse=True)
degreeCount = collections.Counter(sortedDegreesDesc)
deg, cnt = zip(*degreeCount.items())

print('Generating network visual representation...')
graph = nx.draw(fullGraphml, arrows=True, **options)

print('Generating diameter...')
printDiameter(fullGraphml)
graphDictionary(deg, cnt, title="Degree Distribution", xlabel="Grades", ylabel="Quantity")

print('Generating network Betweenness Centrality visual representation...')
toupleXYBetwennessCentraily = getBetweennessCentralityXYTuple(fullGraphml)
graphDictionary(toupleXYBetwennessCentraily[0], toupleXYBetwennessCentraily[1], title="Betweenness Centrality", xlabel="Node", ylabel='BCentrality')

print('Generating network Clustering Coefficient visual representation...')
toupleXYClusteringCoefficient = getClusteringCoefficientXYTuple(fullGraphml)
graphDictionary(toupleXYClusteringCoefficient[0], toupleXYClusteringCoefficient[1], title="Clustering Coefficients", xlabel="Node", ylabel='CCoeficients')
plt.show()
