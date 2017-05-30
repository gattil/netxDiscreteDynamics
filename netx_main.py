#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

# Import section (built-in modules|third-party modules)

import random as rnd
import progressbar
import numpy as np
import sys
from networkx.readwrite import json_graph
import json
import time
import datetime

from netx_plot import *
from netx_popdynamics import *
from netx_parser import *

# Authorship information

__project__ = 'symeventflow'
__product__ = 'netx_main'
__editor__ = 'PyCharm'
__author__ = 'lorenzogatti'
__copyright__ = "Copyright 2017, Applied Computational Genomics Team (ACGT)"
__credits__ = ["Lorenzo Gatti"]
__license__ = "GPL"
__date__ = '23.05.17'
__version__ = "1.0"
__maintainer__ = "Lorenzo Gatti"
__email__ = "lorenzo.gatti@zhaw.ch"
__status__ = "Development"


# Main code

def main(args):

    # -----------------------------------------------------------------------
    data = dict()
    tsdata = dict()

    # -----------------------------------------------------------------------
    # Consider node population
    mod_node_population = args.input_considerpopulation
    # Plot engine
    network_plot = args.input_plot

    # -----------------------------------------------------------------------
    # Simulated time
    periods = args.input_cycles  # 1000
    # Technical replicates
    experiments = args.input_repetitions  # 5
    # Initial population
    initial_population = args.input_initpop
    # Automatically increase population at fixed time intervals
    fixed_time = np.ceil(np.linspace(periods/4, periods, 5))
    # Amount new population to introduce
    pop_increase_size = initial_population * args.input_size_increase  # 0.1 for the 10% of the initial population
    # Increase location
    pop_increase_location = [i for i in args.input_location_increase if i is not ',']   # ['A','D']

    # -----------------------------------------------------------------------
    # Main routine
    G = initialise_network(experiments, periods,
                           init_pop=initial_population,
                           edge_file=args.input_edge_file,
                           node_file=args.input_node_file)

    with progressbar.ProgressBar(max_value=periods*experiments) as bar:
        for e in range(experiments):
            for i in range(1, periods+1):
                # Increase the population at fixed intervals:
                if bool(args.input_addlinearincrease):
                    if i in fixed_time:
                        introduce_new_population(G, time=[e, i], size=pop_increase_size, nodes=pop_increase_location)
                # Per each node, evaluate the firing probabilty of each edge to fire
                for n in G.nodes_iter():
                    for edge in list(G.out_edges(n)):
                        r = rnd.uniform(0, 1)  # indipendent firing for each edge
                        n_sour = edge[0]
                        n_dest = edge[1]

                        if r <= G.edge[n_sour][n_dest]['p_fire']:

                            if mod_node_population:
                                if G.node[n_sour]['ts'][e][i] is not None:
                                    if G.node[n_sour]['ts'][e][i] <= 1:
                                        continue
                                else:
                                    if G.node[n_sour]['ts'][e][i-1] <= 1:
                                        continue

                            # record the event
                            G.edge[n_sour][n_dest]['c_events'][e][i] = 1
                            G.edge[n_sour][n_dest]['r_time'].append(i)

                            # update the source node events
                            G.node[n_sour]['out_events'] -= 1
                            # propagate the event to the final node
                            G.node[n_dest]['in_events'] += 1

                            # Population update
                            if mod_node_population:
                                # Do not count in case of self loop
                                if n_sour == n_dest:
                                    continue

                                else:
                                    # For all the other cases
                                    if G.node[n_sour]['ts'][e][i] is None:
                                        G.node[n_sour]['ts'][e][i] = G.node[n_sour]['ts'][e][i-1] - 1
                                    else:
                                        G.node[n_sour]['ts'][e][i] = G.node[n_sour]['ts'][e][i] - 1

                                    if G.node[n_dest]['ts'][e][i] is None:
                                        G.node[n_dest]['ts'][e][i] = G.node[n_dest]['ts'][e][i-1] + 1
                                    else:
                                        G.node[n_dest]['ts'][e][i] = G.node[n_dest]['ts'][e][i] + 1

                    # Population update
                    if mod_node_population:
                        if G.node[n]['ts'][e][i] is None:
                            G.node[n]['ts'][e][i] = G.node[n]['ts'][e][i-1]

                    # Compute the increment
                    start_value = G.node[n]['ts'][e][i-1]
                    end_value = G.node[n]['ts'][e][i]
                    increment = (end_value-start_value)/start_value
                    G.node[n]['ts_i'][e][i] = increment

            # Total amount of firing events for network edges
            t_e_events = sum([sum(filter(None, G.get_edge_data(edge[0], edge[1])['c_events'][e])) for edge in G.edges()])

            d = {edge[0] + '-' + edge[1]: sum(filter(None, G.get_edge_data(edge[0], edge[1])['c_events'][e]))/t_e_events for
                 edge in G.edges()}

            for k in d:
                if not k in data:
                    data[k] = list()
                data[k].append(d[k])

            bar.update(e*i)

    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M_%S')

    if  args.input_plot:
        plot_population_dynamics(G, object='ts', outputfilename=args.output_json+'_plot_pdts_'+st+'.png')
        plot_population_dynamics(G, object='ts_i', outputfilename=args.output_json+'_plot_pdts_i_'+st+'.png')
        plot_edge_dynamics(data, outputfilename=args.output_json+'_plot_edge_'+st+'.png')

    # Store parameters in JSON
    with open(args.output_json+'_'+st+'_nodes.json', "w") as f:
        json_nodes = dict()
        for node in G.nodes():
            json_nodes[node]= G.node[node]['ts']
        f.write(json.dumps(json_nodes, sort_keys=True, indent=4))

    with open(args.output_json+'_'+st+'_edges.json', "w") as f:
        f.write(json.dumps(data, sort_keys=True, indent=4))

    return 0

if __name__ == "__main__":

    # --------------------------------------------------------------------------------------------
    # Parse execution arguments
    args = arg_parser()
    # ---------------------

    main(args)

    # --------------------------------------------------------------------------------------------
    # Exit program
    sys.exit(0)
