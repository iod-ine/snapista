""" This file contains the definition of the BandSelect operator.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

import lxml.etree

from snapista.operators import Operator


class BandSelect(Operator):
    """ Create a new product with only selected bands.


    Attributes:
        band_name_pattern (str): Band name regular expression pattern.
        selected_polarizations (list): The list of polarizations.
        source_bands (str): The list of source bands.

    """

    def __init__(self):
        super(BandSelect, self).__init__(name='BandSelect', short_name='BandSelect')

        self.band_name_pattern = None
        self.selected_polarizations = []
        self.source_bands = []

    def _get_parameters_as_xml_node(self):
        """ Generate the <parameters> node to include in the graph. """

        parameters = lxml.etree.Element('parameters')

        if len(self.selected_polarizations) > 0:
            selected_polarizations = lxml.etree.SubElement(parameters, 'selectedPolarisations')
            selected_polarizations.text = ','.join(self.selected_polarizations)

        if len(self.source_bands) > 0:
            source_bands = lxml.etree.SubElement(parameters, 'sourceBands')
            source_bands.text = ','.join(self.source_bands)

        if self.band_name_pattern is not None:
            band_name_pattern = lxml.etree.SubElement(parameters, 'bandNamePattern')
            band_name_pattern.text = self.band_name_pattern

        return parameters
