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
import argparse

# Authorship information

__project__ = 'symeventflow'
__product__ = 'netx_parser'
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

def arg_parser():
    """
    This function parses the arguments passed from the command line to the script
    :returns
        It returns an object containing all the recognised arguments properly formatted
    """

    parser = argparse.ArgumentParser(prog=__product__,
                                     description='Simulate population flowing on a discrete network using directed '
                                                 'edges. ')

    parser.add_argument("-t", "--time", type=int, dest="input_cycles", required=True,
                        help='Simulation time [int]')

    parser.add_argument("-r", "--repetitions", type=int, dest="input_repetitions", required=True,
                        help='Technical replicates [int]')

    parser.add_argument("-p", "--population", type=int, dest="input_initpop", required=True,
                        help='Initial population [int]')

    parser.add_argument("-cp", "--consider-population", type=bool, dest="input_considerpopulation", required=False,
                        help='Consider population flowing [bool]')

    parser.add_argument("-wi", "--with-increase", type=bool, dest="input_addlinearincrease", required=False,
                        default=False,
                        help='Add linear increase [bool]')

    parser.add_argument("-si", "--size-increase", type=float, dest="input_size_increase", required=False,
                        help='Increase population proportion [float]')

    parser.add_argument("-li", "--location-increase", type=list, dest="input_location_increase", required=False,
                        help='Increase population location [list]')

    parser.add_argument("-nf", "--node-file", type=str, dest="input_node_file", required=True,
                        help='Node file definition [str]')

    parser.add_argument("-ev", "--edge-init-values", type=str, dest="input_edge_file", required=True,
                        help='Edge file initial values [str]')

    parser.add_argument("-pl", "--plot", type=bool, dest="input_plot", required=False,
                        help='Plot graphs [bool]')

    parser.add_argument("-o", "--output-json", type=str, dest="output_json", required=False,
                        help='Output JSON file [str]')

    parser.add_argument("-v", "--verbosity", type=str, dest="log_level", required=False,
                        default='DEBUG', help='Input Tree file')

    return parser.parse_args()

