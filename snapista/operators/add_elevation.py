""" This file contains the definition of the AddElevation operator.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

import lxml.etree

from snapista.operators import Operator


class AddElevation(Operator):
    """ Create a DEM band.

    Attributes:
        dem_name (str): The digital elevation model.
        dem_resampling_method (str): Resampling method for the DEM.
        elevation_band_name (str): The elevation band name.
        external_dem_file (str): External DEM file.
        external_dem_no_data_value (str): External DEM no data value.

    """

    def __init__(self):
        super(AddElevation, self).__init__(name='AddElevation', short_name='elev')

        self.dem_name = 'SRTM 3Sec'
        self.dem_resampling_method = 'BICUBIC_INTERPOLATION'
        self.elevation_band_name = 'elevation'
        self.external_dem_file = None
        self.external_dem_no_data_value = 0

    @staticmethod
    def get_available_dem_names():
        """ Get a list of possible DEM names. """

        dem_names = [
            'ACE2_5Min',
            'ACE30',
            'ASTER 1sec GDEM',
            'CDEM',
            'Copernicus 30m Global DEM',
            'Copernicus 90m Global DEM',
            'GETASSE30',
            'SRTM 1sec HGT',
            'SRTM 3sec',
        ]

        return dem_names

    @staticmethod
    def get_available_dem_resampling_methods():
        """ Get a list of possible DEM resampling methods. """

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

    def get_parameters_as_xml_node(self):
        """ Generate the <parameters> node to include in the graph. """

        parameters = lxml.etree.Element('parameters')

        dem_name = lxml.etree.SubElement(parameters, 'demName')
        dem_name.text = self.dem_name

        dem_resampling_method = lxml.etree.SubElement(parameters, 'demResamplingMethod')
        dem_resampling_method.text = self.dem_resampling_method

        if self.external_dem_file is not None:
            external_dem_file = lxml.etree.SubElement(parameters, 'externalDEMFile')
            external_dem_file.text = self.external_dem_file

            external_dem_no_data_value = lxml.etree.SubElement(parameters, 'externalDEMNoDataValue')
            external_dem_no_data_value.text = str(self.external_dem_no_data_value)

        elevation_band_name = lxml.etree.SubElement(parameters, 'elevationBandName')
        elevation_band_name.text = self.elevation_band_name

        return parameters
