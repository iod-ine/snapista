""" This file contains the definition of the c2rcc.msi operator.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

import xml.sax.saxutils

import lxml.etree

from snapista.operators import Operator


class C2RCC_MSI(Operator):
    """ Perform atmospheric correction and IOP retrieval with uncertainties on Sentinel-2 MSI L1C data products.

    Attributes:
        alternative_nn_path (str): Path to an alternative set of neuronal nets.
        atmospheric_aux_data_path (str): Path to the atmospheric auxiliary data directory.  If the auxiliary data is
            not available at this path, the data will automatically be downloaded.
        chl_exp (float): Chlorophyll exponent ( CHL = iop_apig^CHLexp * CHLfac).
        chl_fac (float): Chlorophyll factor ( CHL = iop_apig^CHLexp * CHLfac).
        derive_rw_from_path_and_transmittance (bool): Alternative way of calculating water reflectance.
            Still experimental.
        elevation (float): Used as fallback if elevation could not be taken from GETASSE30 DEM.
            Valid interval is (0, 8500) meters
        net_set (str): Set of neuronal nets for algorithm. One of 'C2RCC-Nets', 'C2X-Nets', 'C2X-COMPLEX-Nets'.

        output_ac_reflectance (bool): Output atmospherically corrected reflectances.
        output_as_rrs (bool): Write remote sensing reflectances instead of water leaving reflectances.
        output_kd (bool): Output irradiance attenuation coefficients (at least I think, gpt description is lacking)
        output_oos (bool): Output out of scope values (at least I think, gpt description is lacking)
        output_r_hown (bool): Output normalized water leaving reflectances (at least I think, gpt description is lacking)
        output_r_path (bool): Output path radiance reflectances (at least I think, gpt description is lacking)
        output_r_toa (bool): Output TOA reflectances (at least I think, gpt description is lacking)
        output_r_tosa_gc (bool): Output gas corrected TOSA reflectances (at least I think, gpt description is lacking)
        output_r_tosa_gc_ann (bool): Output gas corrected TOSA reflectances of auto NN (?)
        output_t_down (bool): Output downward transmittance.
        output_t_up (bool): Output upward transmittance.
        output_uncertainties (bool): Output uncertainties.

        ozone (float): The value used as ozone if not provided by auxiliary data. Valid interval is (0, 1000) DU.
        press (float): The surface air pressure at sea level if not provided by auxiliary data.
            Valid interval is (800, 1040) hPa.
        salinity (float): The value used as salinity for the scene. Valid interval is (0.000028, 43) PSU.
        temperature (float): The value used as temperature for the scene. Valid interval is (0.000111, 36) C.
        threshold_ac_reflectance_oos (float): Threshold for out of scope of nn training dataset flag for AC reflectances
        threshold_cloud_t_down_865 (float): Threshold for cloud test based on down-welling transmittance @865.
        threshold_r_tosa_oos (float): Threshold for out of scope of nn training dataset flag for gas corrected
            top-of-atmosphere reflectances.
        tsm_exp (float): TSM exponent (TSM = TSMfac * iop_btot^TSMexp).
        tsm_fac (float): TSM factor (TSM = TSMfac * iop_btot^TSMexp).
        valid_pixel_expression (str): Defines the pixels which are valid for processing.

    """

    def __init__(self):
        super(C2RCC_MSI, self).__init__(name='c2rcc.msi', short_name='c2rcc')

        self.alternative_nn_path = None
        self.atmospheric_aux_data_path = None
        self.chl_exp = 1.04
        self.chl_fac = 21.0
        self.derive_rw_from_path_and_transmittance = False
        self.elevation = 0.0
        self.net_set = 'C2RCC-Nets'

        self.output_ac_reflectance = True
        self.output_as_rrs = False
        self.output_kd = True
        self.output_oos = False
        self.output_r_hown = True
        self.output_r_path = False
        self.output_r_toa = True
        self.output_r_tosa_gc = False
        self.output_r_tosa_gc_ann = False
        self.output_t_down = False
        self.output_t_up = False
        self.output_uncertainties = True

        self.ozone = 330.0
        self.press = 1000.0
        self.salinity = 35.0
        self.temperature = 15.0
        self.threshold_ac_reflectance_oos = 0.1
        self.threshold_cloud_t_down_865 = 0.955
        self.threshold_r_tosa_oos = 0.05
        self.tsm_exp = 0.942
        self.tsm_fac = 1.06
        self.valid_pixel_expression = 'B8 > 0 && B8 < 0.1'

        self._ncep_start_product = None
        self._ncep_end_product = None
        self._tomsomi_start_product = None
        self._tomsomi_end_product = None

    @property
    def ncep_start_product(self):
        return self._ncep_start_product

    @property
    def ncep_end_product(self):
        return self._ncep_end_product

    @property
    def tomsomi_start_product(self):
        return self._tomsomi_start_product

    @property
    def tomsomi_end_product(self):
        return self._tomsomi_end_product

    # TODO: Implement additional sources

    @ncep_start_product.setter
    def ncep_start_product(self, value):
        self._ncep_start_product = value
        raise NotImplementedError

    @ncep_end_product.setter
    def ncep_end_product(self, value):
        self._ncep_end_product = value
        raise NotImplementedError

    @tomsomi_start_product.setter
    def tomsomi_start_product(self, value):
        self.tomsomi_start_product = value
        raise NotImplementedError

    @tomsomi_end_product.setter
    def tomsomi_end_product(self, value):
        self.tomsomi_end_product = value
        raise NotImplementedError

    def _get_parameters_as_xml_node(self):
        """ Generate the <parameters> node to include in the graph. """

        parameters = lxml.etree.Element('parameters')

        valid_pixel_expression = lxml.etree.SubElement(parameters, 'validPixelExpression')
        valid_pixel_expression.text = self.valid_pixel_expression
        # valid_pixel_expression.text = xml.sax.saxutils.escape(self.valid_pixel_expression)

        salinity = lxml.etree.SubElement(parameters, 'salinity')
        salinity.text = str(self.salinity)

        temperature = lxml.etree.SubElement(parameters, 'temperature')
        temperature.text = str(self.temperature)

        ozone = lxml.etree.SubElement(parameters, 'ozone')
        ozone.text = str(self.ozone)

        press = lxml.etree.SubElement(parameters, 'press')
        press.text = str(self.press)

        elevation = lxml.etree.SubElement(parameters, 'elevation')
        elevation.text = str(self.elevation)

        tsm_fac = lxml.etree.SubElement(parameters, 'TSMfac')
        tsm_fac.text = str(self.tsm_fac)

        tsm_exp = lxml.etree.SubElement(parameters, 'TSMexp')
        tsm_exp.text = str(self.tsm_exp)

        chl_exp = lxml.etree.SubElement(parameters, 'CHLexp')
        chl_exp.text = str(self.chl_exp)

        chl_fac = lxml.etree.SubElement(parameters, 'CHLfac')
        chl_fac.text = str(self.chl_fac)

        threshold_r_tosa_oos = lxml.etree.SubElement(parameters, 'thresholdRtosaOOS')
        threshold_r_tosa_oos.text = str(self.threshold_r_tosa_oos)

        threshold_ac_reflectance_oos = lxml.etree.SubElement(parameters, 'thresholdAcReflecOos')
        threshold_ac_reflectance_oos.text = str(self.threshold_ac_reflectance_oos)

        threshold_cloud_t_down_865 = lxml.etree.SubElement(parameters, 'thresholdCloudTDown865')
        threshold_cloud_t_down_865.text = str(self.threshold_cloud_t_down_865)

        if self.atmospheric_aux_data_path is not None:
            atmospheric_aux_data_path = lxml.etree.SubElement(parameters, 'atmosphericAuxDataPath')
            atmospheric_aux_data_path.text = str(self.atmospheric_aux_data_path)

        if self.alternative_nn_path is not None:
            alternative_nn_path = lxml.etree.SubElement(parameters, 'alternativeNNPath')
            alternative_nn_path.text = str(self.alternative_nn_path)

        net_set = lxml.etree.SubElement(parameters, 'netSet')
        net_set.text = self.net_set

        output_as_rrs = lxml.etree.SubElement(parameters, 'outputAsRrs')
        output_as_rrs.text = 'true' if self.output_as_rrs else 'false'

        derive_rw_from_path_and_transmittance = lxml.etree.SubElement(parameters, 'deriveRwFromPathAndTransmittance')
        derive_rw_from_path_and_transmittance.text = 'true' if self.derive_rw_from_path_and_transmittance else 'false'

        output_r_toa = lxml.etree.SubElement(parameters, 'outputRtoa')
        output_r_toa.text = 'true' if self.output_r_toa else 'false'

        output_r_tosa_gc = lxml.etree.SubElement(parameters, 'outputRtosaGc')
        output_r_tosa_gc.text = 'true' if self.output_r_tosa_gc else 'false'

        output_r_tosa_gc_ann = lxml.etree.SubElement(parameters, 'outputRtosaGcAann')
        output_r_tosa_gc_ann.text = 'true' if self.output_r_tosa_gc_ann else 'false'

        output_r_path = lxml.etree.SubElement(parameters, 'outputRpath')
        output_r_path.text = 'true' if self.output_r_path else 'false'

        output_t_down = lxml.etree.SubElement(parameters, 'outputTdown')
        output_t_down.text = 'true' if self.output_t_down else 'false'

        output_t_up = lxml.etree.SubElement(parameters, 'outputTup')
        output_t_up.text = 'true' if self.output_t_up else 'false'

        output_ac_reflectance = lxml.etree.SubElement(parameters, 'outputAcReflectance')
        output_ac_reflectance.text = 'true' if self.output_ac_reflectance else 'false'

        output_r_hown = lxml.etree.SubElement(parameters, 'outputRhown')
        output_r_hown.text = 'true' if self.output_r_hown else 'false'

        output_oos = lxml.etree.SubElement(parameters, 'outputOos')
        output_oos.text = 'true' if self.output_oos else 'false'

        output_kd = lxml.etree.SubElement(parameters, 'outputKd')
        output_kd.text = 'true' if self.output_kd else 'false'

        output_uncertainties = lxml.etree.SubElement(parameters, 'outputUncertainties')
        output_uncertainties.text = 'true' if self.output_uncertainties else 'false'

        return parameters
