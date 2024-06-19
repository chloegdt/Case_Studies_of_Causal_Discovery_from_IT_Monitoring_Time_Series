import click
import random
from Algorithms.Hybrids_of_CB_and_NB.cbnb_e import CBNBe
from Algorithms.Hybrids_of_CB_and_NB.nbcb_e import NBCBe
from Algorithms.Hybrids_of_CB_and_NB.nbcb_w import NBCBw
from Algorithms.Hybrids_of_CB_and_NB.cbnb_w import CBNBw
import Algorithms.algorithms

from evalusation_measure import f1_score
from causallearn.graph.GeneralGraph import GeneralGraph
from causallearn.graph.GraphNode import GraphNode

import numpy as np
import pandas as pd

from causallearn.graph.Edge import Edge
from causallearn.graph.Endpoint import Endpoint

from tools.plot_tools import plot_graph_with_false_positives


dict_colname_to_texname = {
    "pre_Message_dispatcher_bolt": "PMDB",
    "message_dispatcher_bolt": "MDB",
    "check_message_bolt": "CMB",
    "Real_time_merger_bolt": "RTMB",
    "metric_bolt": "MB",
    "group_status_information_bolt": "GSIB",
    "capacity_last_metric_bolt": "LMB",
    "capacity_elastic_search_bolt": "ESB"
}


@click.command()
@click.option('--tau', default=15, type=int, help='param_tau_max')
@click.option('--sig', default=0.05, type=float, help='param_sig_level')
@click.argument('method', type=click.Choice(['CBNB_W', 'CBNB_E', 'NBCB_W', 'NBCB_E', 'GCMVL', 'PCMCI', 'PCGCE', 'VARLINGAM', 'TIMINO', 'DYNOTEARS'], case_sensitive=False))
def run_command(method, tau, sig):
    """
    METHOD: The causal discovery methode to use (CBNB_w, CBNB_e, NBCB_w, NBCB_e, GCMVL, PCMCI, PCGCE, VARLINGAM, TiMINO, DYNOTEARS)
    """
    param_method = method.upper()
    param_tau_max = int(tau)
    param_sig_level = sig
    click.echo(f"Run : tau ={tau}, sig = {sig}, method = {method}")
    run(param_method, param_tau_max, param_sig_level)


def run(param_method, param_tau_max, param_sig_level):
    param_method = param_method  # CBNB_w NBCB_w CBNB_e NBCB_e GCMVL CCM PCMCI PCGCE VarLiNGAM TiMINO Dynotears
    param_tau_max = param_tau_max
    param_sig_level = param_sig_level

    f1_adjacency_list = []
    f1_orientation_list = []
    percentage_of_detection_skeleton = 0

    param_data = pd.read_csv("./data/Storm_Ingestion_Activity/storm_data_normal.csv", delimiter=',', index_col=0, header=0)

    param_data.columns = param_data.columns.str.replace(' ', '_')
    print(param_data)

    three_col_format = np.loadtxt("./data/Storm_Ingestion_Activity/storm_structure.txt",
                                  delimiter=' ', dtype=str)

    summary_matrix = pd.DataFrame(np.zeros([param_data.shape[1], param_data.shape[1]]), columns=param_data.columns,
                                  index=param_data.columns)
    for i in range(three_col_format.shape[0]):
        c = three_col_format[i, 0]
        e = three_col_format[i, 1]
        summary_matrix[e].loc[c] = 1

    list_nodes = []
    for col_i in param_data.columns:
        list_nodes.append(GraphNode(col_i))
    causal_graph_true = GeneralGraph(list_nodes)
    for col_i in summary_matrix.columns:
        for col_j in summary_matrix.columns:
            if (summary_matrix[col_j].loc[col_i] != 0) and (summary_matrix[col_i].loc[col_j] != 0):
                causal_graph_true.add_edge(Edge(GraphNode(col_i), GraphNode(col_j), Endpoint.ARROW, Endpoint.ARROW))
            elif summary_matrix[col_j].loc[col_i] != 0:
                causal_graph_true.add_edge(Edge(GraphNode(col_i), GraphNode(col_j), Endpoint.TAIL, Endpoint.ARROW))
            elif summary_matrix[col_i].loc[col_j] != 0:
                causal_graph_true.add_edge(Edge(GraphNode(col_j), GraphNode(col_i), Endpoint.TAIL, Endpoint.ARROW))

    if param_method == "NBCB_W":
        nbcb = NBCBw(param_data, param_tau_max, param_sig_level, model="linear",  indtest="linear", cond_indtest="linear")
        nbcb.run()
        causal_graph_hat = nbcb.causal_graph
    elif param_method == "CBNB_W":
        cbnb = CBNBw(param_data, param_tau_max, param_sig_level, model="linear", indtest="linear",
                     cond_indtest="linear")
        cbnb.run()
        causal_graph_hat = cbnb.causal_graph
    elif param_method == "NBCB_E":
        nbcb = NBCBe(param_data, param_tau_max, param_sig_level, model="linear", indtest="linear",
                     cond_indtest="linear")
        nbcb.run()
        causal_graph_hat = nbcb.causal_graph
    elif param_method == "CBNB_E":
        cbnb = CBNBe(param_data, param_tau_max, param_sig_level, model="linear", indtest="linear",
                     cond_indtest="linear")
        cbnb.run()
        causal_graph_hat = cbnb.causal_graph
    elif param_method == "GCMVL":
        causal_graph_hat = Algorithms.algorithms.granger_lasso(param_data, tau_max=param_tau_max, sig_level=param_sig_level)
    elif param_method == "CCM":
        causal_graph_hat = Algorithms.algorithms.ccm(param_data, tau_max=param_tau_max)
    elif param_method == "PCMCI":
        causal_graph_hat = Algorithms.algorithms.pcmciplus(param_data, tau_max=param_tau_max, sig_level=param_sig_level)
    elif param_method == "PCGCE":
        causal_graph_hat = Algorithms.algorithms.pcgce(param_data, tau_max=param_tau_max, sig_level=param_sig_level)
    elif param_method == "VARLINGAM":
        causal_graph_hat = Algorithms.algorithms.varlingam(param_data, tau_max=param_tau_max, sig_level=param_sig_level)
    elif param_method == "TIMINO":
        causal_graph_hat = Algorithms.algorithms.run_timino_from_r([[param_data, "data"], [param_sig_level, "alpha"], [param_tau_max, "nlags"]])
    elif param_method == "DYNOTEARS":
        causal_graph_hat = Algorithms.algorithms.dynotears(param_data, tau_max=param_tau_max, sig_level=param_sig_level)
    else:
        causal_graph_hat = None
    print(causal_graph_hat)
    plot_graph_with_false_positives(causal_graph_hat, param_data.columns, causal_graph_true, dict_colname_to_texname)

    fa = f1_score(causal_graph_hat, causal_graph_true, ignore_orientation=True)
    fo = f1_score(causal_graph_hat, causal_graph_true, ignore_orientation=False)
    print("F1 adjacency with desired graph= " + str(fa))
    print("F1 orientation with desired graph = " + str(fo))
    f1_adjacency_list.append(fa)
    f1_orientation_list.append(fo)

    if causal_graph_true.get_graph_edges() == causal_graph_hat.get_graph_edges():
        percentage_of_detection_skeleton = percentage_of_detection_skeleton + 1

    print("#############################################")
    print("F1 adjacency with desired graph= " + str(np.mean(f1_adjacency_list)) + " +- " + str(np.var(f1_adjacency_list)))
    print("F1 orientation with desired graph= " + str(np.mean(f1_orientation_list)) + " +- " + str(np.var(f1_orientation_list)))
    print("Percentage of detection with desired graph= " + str(percentage_of_detection_skeleton/100))


if __name__ == '__main__':
    run_command()
