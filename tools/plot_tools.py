import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import pydot
from typing import List
from causallearn.graph.Graph import Graph
from causallearn.graph.NodeType import NodeType
from causallearn.graph.Edge import Edge
from causallearn.graph.Endpoint import Endpoint


def to_pydot_with_colored_env(G: Graph, edges: List[Edge] = None, labels: List[str] = None,
                              title: str = "", dpi: float = 150, names_env = None, rank = True):
    '''
    Convert a graph object to a DOT object.

    Parameters
    ----------
    G : Graph
        A graph object of causal-learn
    edges : list, optional (default=None)
        Edges list of graph G
    labels : list, optional (default=None)
        Nodes labels of graph G
    title : str, optional (default="")
        The name of graph G
    dpi : float, optional (default=200)
        The dots per inch of dot object
    env_names :
    Returns
    -------
    pydot_g : Dot
    '''
    if names_env is None:
        names_env = []

    nodes = G.get_nodes()
    if labels is not None:
        assert len(labels) == len(nodes)

    pydot_g = pydot.Dot(title, graph_type="digraph", fontsize=17, ratio="0.6")  # ranksep="1.3" 0.709401709
    pydot_g.set_node_defaults(fontsize='25')
    pydot_g.obj_dict["attributes"]["dpi"] = dpi
    nodes = G.get_nodes()
    if rank:
        ENV = pydot.Subgraph(rank='sink', ranksep="equally")
        H1 = pydot.Subgraph(rank='same', ranksep="equally")
        H2 = pydot.Subgraph(rank='same', ranksep="equally")
        H3 = pydot.Subgraph(rank='source')
    for i, node in enumerate(nodes):
        node_name = labels[i] if labels is not None else node.get_name()

        # pydot_g.add_node(pydot.Node(i, label=node.get_name()))
        if node.get_node_type() == NodeType.LATENT:
            pydot_g.add_node(pydot.Node(i, label=node_name, shape='square'))
        else:
            if node_name in names_env:
                if rank:
                    ENV.add_node(pydot.Node(i, label=node_name, color='red'))
                else:
                    pydot_g.add_node(pydot.Node(i, label=node_name, color='red'))
            else:
                if rank:
                    if node_name.endswith('1'):
                        H1.add_node(pydot.Node(i, label=node_name))
                    elif node_name.endswith('2'):
                        H2.add_node(pydot.Node(i, label=node_name))
                    elif node_name.endswith('3'):
                        H3.add_node(pydot.Node(i, label=node_name))
                    else:
                        pydot_g.add_node(pydot.Node(i, label=node_name))
                else:
                    pydot_g.add_node(pydot.Node(i, label=node_name))

    # S = pydot.Subgraph(rank='same')
    # S.add_node(node4)
    if rank:
        pydot_g.add_subgraph(H3)
        pydot_g.add_subgraph(H2)
        pydot_g.add_subgraph(H1)
        pydot_g.add_subgraph(ENV)

    def get_g_arrow_type(endpoint):
        if endpoint == Endpoint.TAIL:
            return 'none'
        elif endpoint == Endpoint.ARROW:
            return 'normal'
        elif endpoint == Endpoint.CIRCLE:
            return 'odot'
        else:
            raise NotImplementedError()

    if edges is None:
        edges = G.get_graph_edges()

    for edge in edges:
        node1 = edge.get_node1()
        node2 = edge.get_node2()
        node1_id = nodes.index(node1)
        node2_id = nodes.index(node2)
        dot_edge = pydot.Edge(node1_id, node2_id, dir='both', arrowtail=get_g_arrow_type(edge.get_endpoint1()),
                              arrowhead=get_g_arrow_type(edge.get_endpoint2()))

        if Edge.Property.dd in edge.properties:
            dot_edge.obj_dict["attributes"]["color"] = "green3"

        if Edge.Property.nl in edge.properties:
            dot_edge.obj_dict["attributes"]["penwidth"] = 2.0

        pydot_g.add_edge(dot_edge)

    return pydot_g


def plot_graph(graph, labels):
    pdy = to_pydot_with_colored_env(graph, labels=labels, names_env=[])
    png_str = pdy.create_png(prog='dot')
    # treat the DOT output as an image file
    sio = io.BytesIO()
    sio.write(png_str)
    sio.seek(0)
    img = mpimg.imread(sio)

    # plot the image
    plt.imshow(img, aspect='equal')
    plt.axis('off')
    plt.show()


def to_pydot_with_false_positives(G: Graph, edges: List[Edge] = None, labels: List[str] = None,
                              title: str = "", dpi: float = 150, names_env = None, rank = True, TG=None,
                              dict_colname_to_texname=None):
    '''
    Convert a graph object to a DOT object.

    Parameters
    ----------
    G : Graph
        A graph object of causal-learn
    edges : list, optional (default=None)
        Edges list of graph G
    labels : list, optional (default=None)
        Nodes labels of graph G
    title : str, optional (default="")
        The name of graph G
    dpi : float, optional (default=200)
        The dots per inch of dot object
    env_names :
    Returns
    -------
    pydot_g : Dot
    '''
    list_of_edges_for_tex = []

    if names_env is None:
        names_env = []

    nodes = G.get_nodes()
    if labels is not None:
        assert len(labels) == len(nodes)

    pydot_g = pydot.Dot(title, graph_type="digraph", fontsize=17, ratio="0.6")  # ranksep="1.3" 0.709401709
    pydot_g.set_node_defaults(fontsize='25')
    pydot_g.obj_dict["attributes"]["dpi"] = dpi
    nodes = G.get_nodes()
    for i, node in enumerate(nodes):
        node_name = labels[i] if labels is not None else node.get_name()

        # pydot_g.add_node(pydot.Node(i, label=node.get_name()))
        if node.get_node_type() == NodeType.LATENT:
            pydot_g.add_node(pydot.Node(i, label=node_name, shape='square'))
        else:
            if node_name in names_env:
                pydot_g.add_node(pydot.Node(i, label=node_name, color='red'))
            else:
                pydot_g.add_node(pydot.Node(i, label=node_name))


    def get_g_arrow_type(endpoint):
        if endpoint == Endpoint.TAIL:
            return 'none'
        elif endpoint == Endpoint.ARROW:
            return 'normal'
        elif endpoint == Endpoint.CIRCLE:
            return 'odot'
        else:
            raise NotImplementedError()

    if edges is None:
        edges = G.get_graph_edges()

    list_edge_g_str = []
    list_edge_g = []
    for edge in edges:
        if (edge.get_endpoint2() == Endpoint.ARROW) and (edge.get_endpoint1() == Endpoint.ARROW):
            list_edge_g_str.append(str(edge.get_node1()) + str(edge.get_endpoint2()) + str(edge.get_node2()))
            list_edge_g_str.append(str(edge.get_node2()) + str(edge.get_endpoint1()) + str(edge.get_node1()))
            list_edge_g.append(edge)
            list_edge_g.append(edge)
        elif edge.get_endpoint2() == Endpoint.ARROW:
            list_edge_g_str.append(str(edge.get_node1()) + str(edge.get_endpoint2()) + str(edge.get_node2()))
            list_edge_g.append(edge)
        elif edge.get_endpoint1() == Endpoint.ARROW:
            list_edge_g_str.append(str(edge.get_node2()) + str(edge.get_endpoint1()) + str(edge.get_node1()))
            list_edge_g.append(edge)
    list_edge_tg_str = []
    list_edge_tg = []
    for edge in TG.get_graph_edges():
        if (edge.get_endpoint2() == Endpoint.ARROW) and (edge.get_endpoint1() == Endpoint.ARROW):
            list_edge_tg_str.append(str(edge.get_node1()) + str(edge.get_endpoint2()) + str(edge.get_node2()))
            list_edge_tg_str.append(str(edge.get_node2()) + str(edge.get_endpoint1()) + str(edge.get_node1()))
            list_edge_tg.append(edge)
            list_edge_tg.append(edge)
        elif edge.get_endpoint2() == Endpoint.ARROW:
            list_edge_tg_str.append(str(edge.get_node1()) + str(edge.get_endpoint2()) + str(edge.get_node2()))
            list_edge_tg.append(edge)
        elif edge.get_endpoint1() == Endpoint.ARROW:
            list_edge_tg_str.append(str(edge.get_node2()) + str(edge.get_endpoint1()) + str(edge.get_node1()))
            list_edge_tg.append(edge)

    tp_edges = list(set(list_edge_g_str) & set(list_edge_tg_str))
    fp_edges = list(set(list_edge_g_str) - set(list_edge_tg_str))

    treated_edges = []
    for edge_str in tp_edges:
        i = list_edge_g_str.index(edge_str)
        edge = list_edge_g[i]
        node1 = edge.get_node1()
        node2 = edge.get_node2()
        node1_id = nodes.index(node1)
        node2_id = nodes.index(node2)

        if edge not in treated_edges:
            if (edge.get_endpoint2() == Endpoint.ARROW) and (edge.get_endpoint1() == Endpoint.ARROW):
                dot_edge = pydot.Edge(node1_id, node2_id, dir='both', arrowtail=get_g_arrow_type(edge.get_endpoint1()),
                                      arrowhead=get_g_arrow_type(edge.get_endpoint2()), color='blue')
                tex_command = "\draw[<->,>=latex, blue] (" + dict_colname_to_texname[node1.get_name()] + ") -- (" + \
                              dict_colname_to_texname[node2.get_name()] + ");"
            else:
                dot_edge = pydot.Edge(node1_id, node2_id, dir='both', arrowtail=get_g_arrow_type(edge.get_endpoint1()),
                                      arrowhead=get_g_arrow_type(edge.get_endpoint2()))
                tex_command = "\draw[->,>=latex] (" + dict_colname_to_texname[node1.get_name()] + ") -- (" + \
                              dict_colname_to_texname[node2.get_name()] + ");"
            list_of_edges_for_tex.append(tex_command)
            pydot_g.add_edge(dot_edge)
            treated_edges.append(edge)

    for edge_str in fp_edges:
        i = list_edge_g_str.index(edge_str)
        edge = list_edge_g[i]
        node1 = edge.get_node1()
        node2 = edge.get_node2()
        node1_id = nodes.index(node1)
        node2_id = nodes.index(node2)

        if edge not in treated_edges:
            dot_edge = pydot.Edge(node1_id, node2_id, dir='both', arrowtail=get_g_arrow_type(edge.get_endpoint1()),
                                  arrowhead=get_g_arrow_type(edge.get_endpoint2()), color="red")
            tex_command = "\draw[->,>=latex, red] (" + dict_colname_to_texname[node1.get_name()] + ") -- (" + \
                          dict_colname_to_texname[node2.get_name()] + ");"
            list_of_edges_for_tex.append(tex_command)
            pydot_g.add_edge(dot_edge)
            treated_edges.append(edge)

    print("List of edges for latex:")
    for l in list_of_edges_for_tex:
        print(l)
    return pydot_g


def plot_graph_with_false_positives(graph, labels, truegraph=None, dict_colname_to_texname=None, save=None, show=False):
    pdy = to_pydot_with_false_positives(graph, labels=labels, names_env=[], TG=truegraph,
                                        dict_colname_to_texname=dict_colname_to_texname)
    png_str = pdy.create_png(prog='dot')
    # treat the DOT output as an image file
    sio = io.BytesIO()
    sio.write(png_str)
    sio.seek(0)
    img = mpimg.imread(sio)

    # plot the image
    plt.imshow(img, aspect='equal')
    plt.axis('off')

    #If the 'save' option has been provided, we save with the given filename
    if save != None:
        plt.savefig(save)
    if show:
        plt.show()
