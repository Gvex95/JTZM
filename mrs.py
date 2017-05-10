from enum import Enum
from typing import Dict, List
import math
import random
import matplotlib.pyplot as plt
import time

class Vertex:
    def __init__(self, name):
        self.name = name
        self.color = VertexColor.WHITE
        self.parent = None
        self.d = 0
        #samo kod dfs-a
        self.f = 0

class VertexColor(Enum):
    BLACK = 0
    GRAY = 127
    WHITE = 255

def breadth_first_search(graph: Dict[Vertex, Vertex], source: Vertex):
    for vertex in graph.keys():
        if vertex != source:
            vertex.color=VertexColor.WHITE
            vertex.d=math.inf
            vertex.parent = None
    source.color = VertexColor.GRAY
    source.d=0
    source.parent = None
    Q = []
    Q.append(source)
    while len(Q) is not 0:
        u = Q.pop(0)
        for vertex in graph[u]:
            if vertex.color is VertexColor.WHITE:
                vertex.color = VertexColor.GRAY
                vertex.parent = u
                vertex.d = u.d + 1
                Q.append(vertex)
        u.color = VertexColor.BLACK


def depth_first_search(G: Dict[Vertex, List[Vertex]]):
    for u in G.keys():
        u.color=VertexColor.WHITE
        u.parent=None
    time = 0
    for u in G.keys():
        if u.color is VertexColor.WHITE:
            dfs_visit(G, u, time)

def dfs_visit(G: Dict[Vertex, List[Vertex]], u: Vertex, time):
    time = time + 1
    u.d = time
    u.color = VertexColor.GRAY
    for v in G[u]:
        if v.color is VertexColor.WHITE:
            v.parent = u
            dfs_visit(G, v, time)
    u.color = VertexColor.BLACK
    time = time + 1
    u.f = time
    
def print_path_bfs(G: Dict[Vertex, List[Vertex]], s: Vertex, v: Vertex):
    breadth_first_search(G, s)
    print_path(s, v)
def print_path_dfs(G: Dict[Vertex, List[Vertex]], s: Vertex, v: Vertex):
    depth_first_search(G)
    print_path(s, v)

def print_path(s: Vertex, v: Vertex):
    if v == s:
        print(s.name)
        return
    elif v.parent is None:
        print('No path from ',s.name,' to ',v.name,' exists')
        return
    else:
        ret = print_path(s, v.parent)
        print(v.name)
        return

VERTEXR = Vertex('R')
VERTEXV = Vertex('V')
VERTEXS = Vertex('S')
VERTEXW = Vertex('W')
VERTEXT = Vertex('T')
VERTEXU = Vertex('U')
VERTEXY = Vertex('Y')
VERTEXX = Vertex('X')
VERTEXZ = Vertex('Z')

BFSG = {
    VERTEXS: [VERTEXR, VERTEXW],
    VERTEXR: [VERTEXS, VERTEXV],
    VERTEXV: [VERTEXR],
    VERTEXW: [VERTEXS, VERTEXT, VERTEXX],
    VERTEXT: [VERTEXW, VERTEXX, VERTEXU],
    VERTEXX: [VERTEXT, VERTEXW, VERTEXY],
    VERTEXU: [VERTEXT, VERTEXX, VERTEXY],
    VERTEXY: [VERTEXT, VERTEXX, VERTEXU]
    }

breadth_first_search(BFSG, VERTEXT)
print('bfs path')
print_path_bfs(BFSG,VERTEXV, VERTEXW)

DFSG = {
    VERTEXU: [VERTEXX, VERTEXV],
    VERTEXX: [VERTEXV],
    VERTEXV: [VERTEXY],
    VERTEXY: [VERTEXX],
    VERTEXW: [VERTEXY, VERTEXS],
    VERTEXZ: [VERTEXZ]
}

print('dfs path')
print_path_dfs(DFSG, VERTEXV, VERTEXY)
depth_first_search(DFSG)

#random i plot


def sum_edges(graph: Dict[Vertex, List[Vertex]]):
    """Returns number of aall edges of a graph"""
    suma = 0
    for keys in graph.keys():
        suma += len(graph[keys])
    return suma

def sum_vertexes(graph: Dict[Vertex, List[Vertex]]):
    """Returns all number of vertexes in graph"""
    return len(graph.keys())

def random_vertices(size, elements):
    """Generate a list of random vertices"""
    verticesnames = random.sample(range(1, size+1), elements)
    vertices = []
    for item in verticesnames:
        #Make a vertex out of every random int
        vertices.append(Vertex(item))
    return vertices

def generate_graph(size: int):
    """Returns randomly generated graph of omitted size
    maximum size is 10000"""
    graph = dict()
    #Generate size number of verticies
    vertices = random_vertices(10000, size)
    #Init graph
    for item in vertices:
        #Put every vertex into the graph
        graph[item] = []
    for item in graph:
        #generate random edges for every vertex
        edgenumber = random.randint(0, size)
        random.shuffle(vertices)
        #assign the edges to the graphs vertex
        graph[item] = vertices[0:edgenumber]
    #return the random graph
    return graph

def first_source(graph: Dict[Vertex, List[Vertex]]):
    """Return a the first vertex in the dictionary"""
    for item in graph:
        return item

def time_measure(graph: Dict[Vertex, List[Vertex]], bfs: bool=False):
    """Returns how long it took for dfs (default) or bfs (set aditonal argument to True)"""
    time_start = 0
    time_end = 0
    if not bfs:
        time_start = time.clock()
        depth_first_search(graph)
        time_end = time.clock()
    else:
        time_start = time.clock()
        breadth_first_search(graph, first_source(graph))
        time_end = time.clock()
    return time_end - time_start

def analyse():
    """Extracts runing times. New graph will be made for every value in runnsize.
     modify runnsize for different size of graphs"""
    vertices = [5, 25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    exectimebfs = []
    exectimedfs = []
    edges = []
    for item in vertices:
        temp_graph = generate_graph(item)
        # number of edges
        edges.append(sum_edges(temp_graph))
        # extract time for bfs
        exectimebfs.append(time_measure(temp_graph, True))
        # extract time for dfs
        exectimedfs.append(time_measure(temp_graph))
    plot_graph_stats(vertices, edges, exectimebfs, 'Breath-First-Search')
    plot_graph_stats(vertices, edges, exectimedfs, 'Depth-First-Search')

def plot_graph_stats(vertices: List[int], edges: List[int], exec_time: List[int], label: str):
    """Makes plot of graph structure"""
    input_data = []
    for index, item in enumerate(vertices):
        input_data.append(item + edges[index])
    plt.plot(input_data, exec_time, label=label)
    plt.xlabel('V + E [n]')
    plt.ylabel('T[S]')
    plt.legend()
    print(label)
    for index, item in enumerate(vertices):
        print("Number of vertecies: {} Number of edges: {} Time: {}"\
        .format(item, edges[index], exec_time[index]))

analyse()
plt.show()
