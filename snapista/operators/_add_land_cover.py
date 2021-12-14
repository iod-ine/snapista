""" This file contains the definition of the AddLandCover operator.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

import lxml.etree

from snapista.operators import Operator


class AddLandCover(Operator):
    """ Create a land cover band.

    Attributes:
        external_files (list of str): The external landcover files.
        land_cover_names (list of str): The land cover models.
        resampling_method (str): Resampling method to use.

    """

    def __init__(self):
        super(AddLandCover, self).__init__(name='AddLandCover', short_name=None)

        self.external_files = []
        self.land_cover_names = ['AAFC Canada Sand Pct']
        self.resampling_method = 'NEAREST_NEIGHBOUR'

    @staticmethod
    def get_available_land_cover_names():
        """ Get a list of possible land cover names. """

        dem_names = [
            'AAFC Canada 2000 Crop',
            'AAFC Canada 2009 Prairies Crop',
            'AAFC Canada 2010 Prairies Crop',
            'AAFC Canada 2011 Crop',
            'AAFC Canada 2012 Crop',
            'AAFC Canada 2013 Crop',
            'AAFC Canada 2014 Crop',
            'AAFC Canada 2015 Crop',
            'AAFC Canada 2016 Crop',
            'AAFC Canada 2016 Crop SMAPVEX',
            'AAFC Canada 2017 Crop',
            'AAFC Canada 2018 Crop',
            'AAFC Canada Clay Pct',
            'AAFC Canada Sand Pct',
            'CCILandCover-2015',
            'GLC2000',
            'GlobCover',
            'JaxaForestMap-2016',
            'MODIS 2007 Tree Cover Percentage',
            'MODIS 2010 Tree Cover Percentage',
        ]

        return dem_names

    @staticmethod
    def get_available_resampling_methods():
        """ Get a list of possible resampling methods. """

        dem_resampling_methods = [
            'NEAREST_NEIGHBOUR',
            'BILINEAR_INTERPOLATION',
            'CUBIC_CONVOLUTION',
            'BISINC_5_POINT_INTERPOLATION',
            'BISINC_11_POINT_INTERPOLATION',
            'BISINC_21_POINT_INTERPOLATION',
            'BICUBIC_INTERPOLATION',
        ]

        return dem_resampling_methods

    def _get_parameters_as_xml_node(self):
        """ Generate the <parameters> node to include in the graph. """

        parameters = lxml.etree.Element('parameters')

        if len(self.land_cover_names) > 0:
            land_cover_names = lxml.etree.SubElement(parameters, 'landCoverNames')
            land_cover_names.text = ','.join(self.land_cover_names)

        if len(self.external_files) > 0:
            external_files = lxml.etree.SubElement(parameters, 'externalFiles')
            external_files.text = ','.join(self.external_files)

        resampling_method = lxml.etree.SubElement(parameters, 'resamplingMethod')
        resampling_method.text = self.resampling_method

        return parameters
