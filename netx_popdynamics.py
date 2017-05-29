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

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

# Import section (built-in modules|third-party modules)
import networkx as nx
import string
import numpy as np


# Authorship information

__project__ = 'symeventflow'
__product__ = 'netx_popdynamics'
__editor__ = 'PyCharm'
__author__ = 'lorenzogatti'
__copyright__ = "Copyright 2017, Applied Computational Genomics Team (ACGT)"
__credits__ = ["Lorenzo Gatti"]
__license__ = "GPL"
__date__ = '29.05.17'
__version__ = "1.0"
__maintainer__ = "Lorenzo Gatti"
__email__ = "lorenzo.gatti@zhaw.ch"
__status__ = "Development"

# Main code

def prepare_array(experiments, cycles, init_pop):
    arr = [[None for x in range(cycles+1)] for y in range(experiments)]
    for r in range(0, len(arr)):
        arr[r][0] = init_pop

    return arr


def generate_prob_matrix(edgedict, up_bound=1):

    parameters = [list(edgedict[key1].values()) for key1 in edgedict.keys()]
    parameters = [val for sublist in parameters for val in sublist]
    parameters = sorted(set(parameters))

    values = np.random.dirichlet(np.ones(len(parameters)) * 1000., size=up_bound)
    values = values.tolist()[0]

    nprob = dict(zip(parameters, values))

    for key1 in edgedict:
        for key2 in edgedict:
            edgedict[key1][key2] = nprob[edgedict[key1][key2]]

    return edgedict


def parse_edge_files(file):
    nnames = string.ascii_uppercase
    edge_dict = dict()

    a_file = open(file, encoding='utf-8')
    i = 0
    gen_dist = False
    for line in a_file:
        line = line.strip('\n')
        edge_dict[nnames[i]] = dict()
        for o in range(0, len(line.split(','))):
            edge_dict[nnames[i]][nnames[o]] = line.split(',')[o]
            if type(line.split(',')[o]) is str:
                gen_dist = True

        i += 1

    return edge_dict, gen_dist


def initialse_edges(G, edge_file, experiments, cycles):

    edge_prob, gen_dist = parse_edge_files(edge_file)

    if gen_dist:
        edge_prob = generate_prob_matrix(edge_prob)

    for fnode in edge_prob:
        for tnode in edge_prob[fnode]:

            G.add_edge(fnode, tnode,
                       p_fire=float(edge_prob[fnode][tnode]),
                       r_events=list(),
                       r_time=list(),
                       c_events=prepare_array(experiments, cycles, 0))


def initialise_nodes(G, node_file, experiments, cycles, init_pop):

    a_file = open(node_file, encoding='utf-8')

    for line in a_file:
        line = line.strip('\n')
        nname, ndesc = line.split(',')

        G.add_node(nname,
                   name=ndesc,
                   in_events=0,
                   out_events=0,
                   population=init_pop,
                   ts=prepare_array(experiments, cycles, init_pop),
                   ts_i=prepare_array(experiments, cycles, 0))


def initialise_network(experiments=50, cycles=1000, init_pop=100, node_file='', edge_file=''):

    # Create a 4-node-directed-acyclic-network
    G = nx.DiGraph()

    initialise_nodes(G, node_file, experiments, cycles, init_pop)
    initialse_edges(G, edge_file, experiments, cycles)

    return G


def introduce_new_population(G, time=[1,1], size=10, nodes=['A','B','C','D']):

    for n in nodes:
        G.node[n]['ts'][time[0]][time[1]-1] += size

