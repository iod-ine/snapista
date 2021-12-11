""" This file contains the definition of the Reproject operator.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

import lxml.etree

from snapista.operators import Operator


class Reproject(Operator):
    """ Reproject a source product to a target Coordinate Reference System.

    Attributes:
        add_delta_bands (bool): Whether to add delta longitude and latitude bands.
        crs (str): Text specifying the target CRS, either in WKT or as an authority code.  AUTO authority can be used
            with code 42001 (UTM), and 42002 (Transverse Mercator) where the scene center is used as reference.
            Examples: EPSG:4326, AUTO:42001
        include_tie_point_grids (bool): Whether tie-point grids should be included in the output product.
        resampling (str): The method used for resampling of floating-point raster data: 'Nearest', 'Bilinear', 'Bicubic'

    Notes:
        Unused parameters: easting, elevationModelName, height, noDataValue, northing, orientation, orthorectify,
        pixelSizeX, pixelSizeY, referencePixelX, referencePixelY, tileSizeX, tileSizeY, width, wktFile.

    """

    def __init__(self):
        super(Reproject, self).__init__(name='Reproject', short_name='Reprojected')

        self.add_delta_bands = False
        self.crs = 'EPSG:4326'
        self.include_tie_point_grids = True
        self.resampling = 'Nearest'

    def get_parameters_as_xml_node(self):
        """ Generate the <parameters> node to include in the graph. """

        parameters = lxml.etree.Element('parameters')

        crs = lxml.etree.SubElement(parameters, 'crs')
        crs.text = self.crs

        resampling = lxml.etree.SubElement(parameters, 'resampling')
        resampling.text = self.resampling

        include_tie_point_grids = lxml.etree.SubElement(parameters, 'includeTiePointGrids')
        include_tie_point_grids.text = 'true' if self.include_tie_point_grids else 'false'

        add_delta_bands = lxml.etree.SubElement(parameters, 'addDeltaBands')
        add_delta_bands.text = 'true' if self.add_delta_bands else 'false'

        return parameters
