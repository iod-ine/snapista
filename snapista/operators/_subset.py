""" This file contains the definition of the Subset operator.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

import lxml.etree

from snapista.operators import Operator


class Subset(Operator):
    """ Create a spatial and/or spectral subset of a data product.

    Attributes:
        copy_metadata (bool): Whether to copy the metadata of the source product.
        full_swath (bool): Forces the operator to extend the subset region to the full swath.
        geo_region (str): The subset region in geographical coordinates using WKT-format.
            If not given the entire scene is used.
        reference_band (str): The band used to indicate the pixel coordinates.
        source_bands (list): The list of source bands.
        sub_sampling_x (int): The pixel sub-sampling step in X (horizontal image direction).
        sub_sampling_y (int): The pixel sub-sampling step in Y (vertical image direction).
        tie_point_grid_names (list): The list of names of tie-point grids to be copied.
            If not given, all bands are copied.

    Notes:
        Unused parameters: region.

    """

    def __init__(self):
        super(Subset, self).__init__(name='Subset', short_name='Subset')

        self.copy_metadata = False
        self.full_swath = False
        self.geo_region = None
        self.reference_band = None
        self.source_bands = []
        self.sub_sampling_x = 1
        self.sub_sampling_y = 1
        self.tie_point_grid_names = []

    def _get_parameters_as_xml_node(self):
        """ Generate the <parameters> node to include in the graph. """

        parameters = lxml.etree.Element('parameters')

        if len(self.source_bands) > 0:
            source_bands = lxml.etree.SubElement(parameters, 'sourceBands')
            source_bands.text = ','.join(self.source_bands)

        if self.reference_band is not None:
            reference_band = lxml.etree.SubElement(parameters, 'referenceBand')
            reference_band.text = self.reference_band

        if self.geo_region is not None:
            geo_region = lxml.etree.SubElement(parameters, 'geoRegion')
            geo_region.text = self.geo_region

        sub_sampling_x = lxml.etree.SubElement(parameters, 'subSamplingX')
        sub_sampling_x.text = str(self.sub_sampling_x)

        sub_sampling_y = lxml.etree.SubElement(parameters, 'subSamplingY')
        sub_sampling_y.text = str(self.sub_sampling_y)

        full_swath = lxml.etree.SubElement(parameters, 'fullSwath')
        full_swath.text = 'true' if self.full_swath else 'false'

        if len(self.tie_point_grid_names) > 0:
            tie_point_grid_names = lxml.etree.SubElement(parameters, 'tiePointGridNames')
            tie_point_grid_names.text = ','.join(self.tie_point_grid_names)

        copy_metadata = lxml.etree.SubElement(parameters, 'copyMetadata')
        copy_metadata.text = 'true' if self.copy_metadata else 'false'

        return parameters
