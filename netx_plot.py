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
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Authorship information

__project__ = 'symeventflow'
__product__ = 'netx_plot'
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

def colorscale(graph):
    colors = cm.rainbow(np.linspace(0, 1, graph.number_of_nodes()))
    color_set = dict(zip(graph.nodes(), colors))

    return color_set

def plot_edge_dynamics(data, outputfilename=''):
    all_data = list(data.values())
    fig, axes = plt.subplots(figsize=(15, 4))
    bplot1 = axes.boxplot(all_data, vert=True, patch_artist=True)
    plt.setp(axes, xticks=[y + 1 for y in range(len(all_data))], xticklabels=list(data.keys()))
    if outputfilename:
        plt.savefig(outputfilename)
    else:
        plt.show()

def plot_population_dynamics(G, object='ts', outputfilename=''):
    cset = colorscale(G)

    fig, ax = plt.subplots(figsize=(15, 4))
    for node in G.nodes():
        t = np.array(G.node[node][object])


        data_mean = np.mean(t, axis=0)
        data_std = np.std(t, axis=0)
        data_max = data_mean + data_std
        data_min = data_mean - data_std

        x = range(1, len(data_mean)+1)
        ax.plot(x, data_mean, 'b-', label=node, color=cset[node])
        ax.fill_between(x, data_min, data_max, alpha=0.5, edgecolor=cset[node],
                        facecolor=cset[node])

    ax.legend(loc='best')

    if outputfilename:
        fig.savefig(outputfilename)
    else:
        fig.show()


