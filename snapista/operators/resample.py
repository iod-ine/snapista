""" This file contains the definition of the Resample operator.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

import lxml.etree

from snapista.operators import Operator


class Resample(Operator):
    """ Resample a multi-size source product to a single-size target product.

    Attributes:
        downsampling (str): The method used for aggregation (downsampling to a coarser resolution).
                            One of 'First', 'Min', 'Max', 'Mean', 'Median'.
        flag_downsampling (str): The method used for aggregation (downsampling to a coarser resolution) of flags.
                                 One of 'First', 'FlagAnd', 'FlagOr', 'FlagMedianAnd', 'FlagMedianOr'.
        reference_band (str): The name of the reference band. All other bands will be re-sampled to match it.
        resample_on_pyramid_levels (bool): Will increase performance when viewing the image, but accurate resampling is
                                           only retrieved when zooming in on a pixel.
        target_height (int): The height that all bands of the target product shall have.
        target_width (int): The width that all bands of the target product shall have.
        target_resolution (int): The resolution that all bands of the target product shall have.
        upsampling (str):  The method used for interpolation (upsampling to a finer resolution).
                           One of 'Nearest', 'Bilinear', 'Bicubic'.

    Notes:
        Either set the reference_band or target_resolution, target_width, and target_height.

        Unused parameters: bandResamplings, resamplingPreset.

    """

    def __init__(self):
        super(Resample, self).__init__(name='Resample', short_name='resampled')

        self._mandatory_source_name = 'sourceProduct'

        self.downsampling = 'First'
        self.flag_downsampling = 'First'
        self.reference_band = None
        self.resample_on_pyramid_levels = True
        self.target_height = None
        self.target_resolution = None
        self.target_width = None
        self.upsampling = 'Nearest'

    def get_parameters_as_xml_node(self):
        """ Generate the <parameters> node to include in the graph. """

        parameters = lxml.etree.Element('parameters')

        if self.reference_band is not None:
            reference_band = lxml.etree.SubElement(parameters, 'referenceBand')
            reference_band.text = self.reference_band
        else:
            target_width = lxml.etree.SubElement(parameters, 'targetWidth')
            target_width.text = str(self.target_width)

            target_height = lxml.etree.SubElement(parameters, 'targetHeight')
            target_height.text = str(self.target_height)

            target_resolution = lxml.etree.SubElement(parameters, 'targetResolution')
            target_resolution.text = str(self.target_resolution)

        upsampling = lxml.etree.SubElement(parameters, 'upsampling')
        upsampling.text = self.upsampling

        downsampling = lxml.etree.SubElement(parameters, 'downsampling')
        downsampling.text = self.downsampling

        flag_downsampling = lxml.etree.SubElement(parameters, 'flagDownsampling')
        flag_downsampling.text = self.flag_downsampling

        resample_on_pyramid_levels = lxml.etree.SubElement(parameters, 'resampleOnPyramidLevels')
        resample_on_pyramid_levels.text = 'true' if self.resample_on_pyramid_levels else 'false'

        return parameters
