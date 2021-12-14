""" This file contains the definition of the Import-Vector operator.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

import pathlib

import lxml.etree

from snapista.operators import Operator


class ImportVector(Operator):
    """ Import a shape file into a product.

    Attributes:
        separate_shapes (bool): Import each shape as a separate mask.
        vector_file (str): Path to the vector file.

    """

    def __init__(self):
        super(ImportVector, self).__init__(name='Import-Vector', short_name=None)

        self.separate_shapes = True
        self.vector_file = ''

    def _get_parameters_as_xml_node(self):
        """ Generate the <parameters> node to include in the graph. """

        assert pathlib.Path(self.vector_file).is_file()

        parameters = lxml.etree.Element('parameters')

        vector_file = lxml.etree.SubElement(parameters, 'vectorFile')
        vector_file.text = str(self.vector_file)

        separate_shapes = lxml.etree.SubElement(parameters, 'separateShapes')
        separate_shapes.text = 'true' if self.separate_shapes else 'false'

        return parameters
