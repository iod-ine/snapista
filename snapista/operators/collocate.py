""" This file contains the definition of the Collocate operator.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

import lxml.etree

from snapista.operators import Operator


class Collocate(Operator):
    """ Collocate two products based on their geo-codings.

    Attributes:
        master_component_pattern (str): The text pattern to be used when renaming master components.
        master_product_name (str): The name of the master product.
        rename_master_components (bool): Whether components of the master shall be renamed in the target product.
        rename_slave_components (bool): Whether components of the slave shall be renamed in the target product.
        resampling_type (str): The method to be used when resampling the slave grid onto the master grid.
        slave_component_pattern (str): The text pattern to be used when renaming slave components.
        source_product_paths (list): A list of file paths specifying the source products.
        target_product_type (str): The product type string for the target product (informal).

    Examples:
        ```python
        data = pathlib.Path('Data')
        products = [data / f for f in os.listdir(data) if 'chl' in f]
        products.sort()

        collocate = snapista.operators.Collocate()
        collocate.master_product_name = products[0].stem
        collocate.source_product_paths = products
        collocate.rename_master_components = False
        collocate.slave_component_pattern = '${ORIGINAL_NAME}_${SLAVE_NUMBER_ID}'

        graph = snapista.Graph()
        graph.add_node(collocate)

        gpt = snapista.GPT(gpt_path)

        gpt.run(
            graph,
            products[0],
            output_folder='../Data/export',
            format_='GeoTIFF',
            output_file_name='chl_stack',
        )
        ```

    """

    def __init__(self):
        super(Collocate, self).__init__(name='Collocate', short_name='Collocate')

        self.master_component_pattern = '${ORIGINAL_NAME}_M'
        self.master_product_name = None
        self.rename_master_components = True
        self.rename_slave_components = True
        self.resampling_type = 'NEAREST_NEIGHBOUR'
        self.slave_component_pattern = '${ORIGINAL_NAME}_S${SLAVE_NUMBER_ID}'
        self.source_product_paths = []
        self.target_product_type = 'COLLOCATED'

    def get_parameters_as_xml_node(self):
        """ Generate the <parameters> node to include in the graph. """

        assert self.master_product_name is not None
        assert len(self.source_product_paths) > 0

        parameters = lxml.etree.Element('parameters')

        source_product_paths = lxml.etree.SubElement(parameters, 'sourceProductPaths')
        source_product_paths.text = ','.join(map(str, self.source_product_paths))

        master_product_name = lxml.etree.SubElement(parameters, 'masterProductName')
        master_product_name.text = str(self.master_product_name)

        target_product_type = lxml.etree.SubElement(parameters, 'targetProductType')
        target_product_type.text = self.target_product_type

        rename_master_components = lxml.etree.SubElement(parameters, 'renameMasterComponents')
        rename_master_components.text = 'true' if self.rename_master_components else 'false'

        rename_slave_components = lxml.etree.SubElement(parameters, 'renameSlaveComponents')
        rename_slave_components.text = 'true' if self.rename_slave_components else 'false'

        master_component_pattern = lxml.etree.SubElement(parameters, 'masterComponentPattern')
        master_component_pattern.text = self.master_component_pattern

        slave_component_pattern = lxml.etree.SubElement(parameters, 'slaveComponentPattern')
        slave_component_pattern.text = self.slave_component_pattern

        resampling_type = lxml.etree.SubElement(parameters, 'resamplingType')
        resampling_type.text = self.resampling_type

        return parameters
