""" This file contains the definition of the Operator class – a wrapper for gpt operators.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""


class Operator:
    """ SNAP gpt operator. """

    def __init__(self, name, short_name):
        """ Create an operator for a SNAP gpt graph. """

        self._name = name  # used in graph construction
        self._short_name = short_name  # used for output file suffix

        # some operators have more complicated <sources> than others
        self._additional_sources = []

        # each additional source should be a dictionary, for example:
        # {'lxml_element': <lxml.etree.Element>, 'name': 'collocateWith', 'value': <path>}
        # this way the graph will be able to generate

    def __repr__(self):
        return f'{self._name}'

    def get_parameters_as_xml_node(self):
        """ Each operator should know how to spit out its own <parameters> node for the xml graph. """
        raise NotImplementedError
