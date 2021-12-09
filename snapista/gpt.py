""" This file contains the definition of the GPT class – a wrapper for SNAP gpt.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

 In my vision, the central object of the package is not the graph, but gpt itself.
 The GPT object is initiated with a path to gpt, and it does not rely on snappy to get information about operators.
 Instead, the operators are manually added to the Operators package.

"""

import pathlib
import logging
import zipfile
import tempfile
import subprocess

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)


class GPT:
    """ A wrapper for the SNAP Graph Processing Tool. """

    def __init__(self, gpt):
        """ Initiate a new GPT object.

        When a GPT object os initiated, a call is made to the provided gpt executable using the subprocess module.
        This call guarantees that the path is correct.

        Args:
            gpt (str): Path to the SNAP gpt executable.

        """

        self.gpt = pathlib.Path(gpt)

        try:
            # we can check if the path is legit by calling `gpt -h` and looking at the stdout
            process = subprocess.run([self.gpt, '-h'], capture_output=True, check=True)
            stdout = process.stdout.decode()
            assert stdout.startswith('Usage:\n  gpt <op>|<graph-file> [options]')
        except (AssertionError, PermissionError):
            raise ValueError(f'{self.gpt.as_posix()} is not gpt!')

    def __repr__(self):
        return f'{self.gpt.as_posix()}'

    def run(self, graph, input_file, output_folder='proc', extension='dim'):
        """ Run the graph for the input.

         Args:
             graph (Graph): A snapista Graph object.
             input_file (str): Path to the input file.
             output_folder (str): Folder to save the output to.
             extension (str): The extension of the output.

         """

        input_file = pathlib.Path(input_file)

        with tempfile.TemporaryDirectory() as temp_dir:
            base = pathlib.Path(temp_dir)
            graph_file = base / 'graph.xml'
            output_file = self._get_output_name(input_file, output_folder, graph.suffix, extension)

            if input_file.match('*S3*.zip'):
                logging.debug('Detected Sentinel-3 archive. Extracting to a temporary location...')

                with zipfile.ZipFile(input_file) as zf:
                    zf.extractall(temp_dir)

                input_file = base / (input_file.stem + '.SEN3') / 'xfdumanifest.xml'

                logging.debug(f'Done. Changed input file to {input_file}.')
            elif input_file.match('*S3*.SEN3'):
                logging.debug('Detected Sentinel-3 folder. ')
                input_file = input_file / 'xfdumanifest.xml'

            graph.save(graph_file)

            logging.info('Calling gpt...')
            subprocess.run([self.gpt, str(graph_file), f'-Ssource={input_file}', '-t', output_file])

    def run_iter(self, graph, input_list, output_folder='proc', extension='dim'):
        """ Run the graph for every input on the input list.

         Args:
             graph (Graph): A snapista Graph object.
             input_list (list of str): List of input paths.
             output_folder (str): Folder to save the output to.
             extension (str): The extension of the output.

         """

        for input_ in input_list:
            self.run(graph, input_, output_folder, extension)

    @staticmethod
    def _get_output_name(input_name, output_folder, suffix, extension):
        input_name = str(input_name).split('/')[-1]

        output = pathlib.Path(output_folder)
        output.mkdir(exist_ok=True)

        output /= '.'.join(input_name.split('.')[:-1]) + f'{suffix}.{extension}'

        return output
