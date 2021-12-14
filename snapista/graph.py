""" This file contains the definition of the Graph class – a wrapper for xml graphs for gpt.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

import lxml.etree


class Graph:
    """ SNAP gpt graph. """

    def __init__(self):
        """ Initiate a new Graph object. """

        # the xml object is hidden from the user
        self._xml = lxml.etree.Element('graph')
        version = lxml.etree.SubElement(self._xml, 'version')
        version.text = '1.0'

        self._node_ids = []

        # a suffix for the output file, listing the processing steps
        self.suffix = ''

        # keep track of special sources that some operators need to run properly
        self._additional_sources = {}

    def __str__(self):
        return lxml.etree.tostring(self._xml, pretty_print=True).decode()

    def add_node(self, operator, node_id=None):
        """ Add a processing step to the graph.

        Args:
            operator (Operator): The operator to be added.
            node_id (str): Optional. A unique ID for the processing step. Will be auto-generated if not provided.

        """

        if node_id is None:
            index = sum([operator._name in node_id for node_id in self._node_ids])
            node_id = f'{operator._name}{index}'

        node = lxml.etree.SubElement(self._xml, 'node')
        node.set('id', node_id)

        name = lxml.etree.SubElement(node, 'operator')
        name.text = operator._name

        # add sources
        sources = lxml.etree.SubElement(node, 'sources')
        if len(self._node_ids) == 0:
            # if it's the first operator added, its source is ${source}
            source = lxml.etree.SubElement(sources, operator._mandatory_source_name)
            source.text = '${source}'
        else:
            # if not, then its source is grabbed from the previous operator
            source = lxml.etree.SubElement(sources, 'sourceProduct')
            source.set('refid', self._node_ids[-1])

        if len(operator._additional_sources) > 0:
            for additional_source in operator._additional_sources:
                sources.append(additional_source['lxml_element'])
                self._additional_sources[additional_source['name']] = additional_source['value']

        parameters = operator._get_parameters_as_xml_node()

        node.append(parameters)

        self._node_ids.append(node_id)
        if operator._short_name is not None:
            self.suffix += f'_{operator._short_name.lower()}'

    def save(self, file):
        """ Save the graph to a file.

        Args:
            file (str): Name of the file.

        """

        with open(file, 'w') as f:
            f.write(lxml.etree.tostring(self._xml, pretty_print=True).decode())
