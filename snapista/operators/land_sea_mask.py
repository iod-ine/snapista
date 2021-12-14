""" This file contains the definition of the Land-Sea-Mask operator.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

import lxml.etree

from snapista.operators import Operator


class LandSeaMask(Operator):
    """ Turn all pixels on land or sea into no-data values.

    Attributes:
        geometry (string): Name of the vector mask to use (as named in the product).
        invert_geometry (bool): Whether to invert the mask. Pixels not covered by the mask are set to NA.
        mask_out_land (bool): Mask out the land (set as False to mask out the water). Only works when use_srtm=True.
        shoreline_extension (int): Extend the shoreline by this many pixels.
        source_bands (list): The list of source bands.
        use_srtm (bool): Use SRTM to infer the separation into land and water.

    Notes:
        Doesn't work on multi-size products, so you have to resample first or select a subset of compatible bands.

        When using a vector as a mask, control what to mask out with invert_geometry parameter, not the mask_out_land
        parameter!

    """

    def __init__(self):
        super(LandSeaMask, self).__init__(name='Land-Sea-Mask', short_name='masked')

        self.geometry = ''
        self.invert_geometry = False
        self.mask_out_land = True
        self.shoreline_extension = 0
        self.source_bands = []
        self.use_srtm = True

    def get_parameters_as_xml_node(self):
        """ Generate the <parameters> node to include in the graph. """

        assert len(self.geometry) > 0 or self.use_srtm

        parameters = lxml.etree.Element('parameters')

        if len(self.source_bands) > 0:
            source_bands = lxml.etree.SubElement(parameters, 'sourceBands')
            source_bands.text = ','.join(self.source_bands)

        land_mask = lxml.etree.SubElement(parameters, 'landMask')
        land_mask.text = 'true' if self.mask_out_land else 'false'

        use_srtm = lxml.etree.SubElement(parameters, 'useSRTM')
        use_srtm.text = 'true' if self.use_srtm else 'false'

        geometry = lxml.etree.SubElement(parameters, 'geometry')
        geometry.text = self.geometry

        invert_geometry = lxml.etree.SubElement(parameters, 'invertGeometry')
        invert_geometry.text = 'true' if self.invert_geometry else 'false'

        shoreline_extension = lxml.etree.SubElement(parameters, 'shorelineExtension')
        shoreline_extension.text = str(self.shoreline_extension)

        return parameters
