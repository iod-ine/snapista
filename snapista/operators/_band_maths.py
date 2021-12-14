""" This file contains the definition of the BandMaths operator.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

import collections

import lxml.etree

from snapista.operators import Operator

TargetBand = collections.namedtuple(
    typename='TargetBand',
    field_names=('name', 'expression', 'type', 'description', 'unit', 'no_data_value')
)


class BandMaths(Operator):
    """ Create a product with one or more bands using mathematical expressions.

    Notes:
        Add bands to the output product by calling the .add_target_band() method.
        Parameters of target bands are:
            name (str): Name of the new band.
            expression (str): Mathematical expression for the new band, as in SNAP GUI.
            type_ (str): Data type of the new band, i.e. float32, uint8, etc.
            description (str): Description for the band.
            unit (str): Unit of the band.
            no_data_value (str or float or int): What value to use for NaN pixels.

    """

    def __init__(self):
        super(BandMaths, self).__init__(name='BandMaths', short_name='BandMaths')

        self._target_bands = []

    def add_target_band(self, name, expression, type_='float32', description=None, unit=None, no_data_value='NaN'):
        """ Add a target band to the output product. """

        self._target_bands.append(TargetBand(name, expression, type_, description, unit, no_data_value))

    def _get_parameters_as_xml_node(self):
        """ Generate the <parameters> node to include in the graph. """

        parameters = lxml.etree.Element('parameters')
        target_bands = lxml.etree.SubElement(parameters, 'targetBands')
        variables = lxml.etree.SubElement(parameters, 'variables')  # haven't figured out what this is for yet

        for band in self._target_bands:
            target_band = lxml.etree.SubElement(target_bands, 'targetBand')

            name = lxml.etree.SubElement(target_band, 'name')
            name.text = band.name

            type_ = lxml.etree.SubElement(target_band, 'type')
            type_.text = band.type

            expression = lxml.etree.SubElement(target_band, 'expression')
            expression.text = band.expression

            if band.description is not None:
                description = lxml.etree.SubElement(target_band, 'description')
                description.text = band.description

            if band.unit is not None:
                unit = lxml.etree.SubElement(target_band, 'unit')
                unit.text = band.unit

            no_data_value = lxml.etree.SubElement(target_band, 'noDataValue')
            no_data_value.text = str(band.no_data_value)

        return parameters
