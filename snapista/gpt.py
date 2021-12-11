""" This file contains the definition of the GPT class – a wrapper for SNAP gpt.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

 In my vision, the central object of the package is not the graph, but gpt itself.
 The GPT object is initiated with a path to gpt, and it does not rely on snappy to get information about operators.
 Instead, the operators are manually added to the Operators package.

"""

import re
import pathlib
import zipfile
import tempfile
import textwrap
import subprocess


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

    def run(self, graph, input_file, output_folder='proc', extension='dim', date_only=False, date_time_only=False,
            suffix=None, suppress_stderr=True):
        """ Run the graph for the input.

         Args:
             graph (Graph): A snapista Graph object.
             input_file (str): Path to the input file.
             output_folder (str): Folder to save the output to.
             extension (str): The extension of the output.
             date_only (bool): Drop everything except the date (and suffix) from the output name.
             date_time_only (bool): Drop everything except the date and time (and suffix) from the output name.
             suffix (str): Suffix to use for output. By default, will consist of a list of applied operators.
             suppress_stderr (bool): Capture stderr without printing it.

         """

        input_file = pathlib.Path(input_file)

        with tempfile.TemporaryDirectory() as temp_dir:
            base = pathlib.Path(temp_dir)
            graph_file = base / 'graph.xml'
            suffix = graph.suffix if suffix is None else suffix

            output_file = pathlib.Path(output_folder)
            output_file.mkdir(exist_ok=True)

            if date_only:
                date_regex = re.compile(r'(\d{4})(\d{2})(\d{2})T\d{6}')
                date = date_regex.findall(str(input_file))[0]
                output_file = output_file / f'{date[0]}-{date[1]}-{date[2]}{suffix}.{extension}'
            elif date_time_only:
                date_time_regex = re.compile(r'(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})')
                date_time = date_time_regex.findall(str(input_file))[0]
                output_file = output_file / ('{}-{}-{}T{}-{}-{}'.format(*date_time) + f'{suffix}.{extension}')
            else:
                output_file = output_file / (input_file.stem + f'{suffix}.{extension}')

            # Sentinel-3 is a special snowflake in terms of reading in the products.
            # GPT and SNAP refuse to open Sentinel-3 archives and only open the xfdumanifest.xml
            # file that is within the product folder.

            # TODO: replace the full name with a short summary, i.e. S3 OLCI WFR from <date>
            print(f'⏳ {input_file.stem}')

            if input_file.match('*S3*.zip'):
                with zipfile.ZipFile(input_file) as zf:
                    zf.extractall(temp_dir)
                input_file = base / (input_file.stem + '.SEN3') / 'xfdumanifest.xml'
            elif input_file.match('*S3*.SEN3'):
                input_file = input_file / 'xfdumanifest.xml'

            graph.save(graph_file)

            process = subprocess.run(
                [self.gpt, str(graph_file), f'-Ssource={input_file}', '-t', output_file],
                stderr=subprocess.PIPE if suppress_stderr else None,
            )

            if suppress_stderr:
                # move at the beginning of 3rd line up, clear line
                print(f'\033[3F\033[J', end='')

            if process.returncode == 0:
                # green checkmark, reset color
                print(f'\033[32m✔\033[0m {output_file.name}')
            else:
                # red cross, reset color
                print(f'\033[31m✗\033[0m {output_file.name}')
                error_regex = re.compile(r'Error: (.*)')
                error = error_regex.findall(process.stderr.decode())[0]
                error = '\n'.join(f'    {line}' for line in textwrap.wrap(error, width=66))
                print(error)

    def run_iter(self, graph, input_list, output_folder='proc', extension='dim', date_only=False, date_time_only=False,
                 suffix=None, suppress_stderr=True):
        """ Run the graph for every input on the input list.

         Args:
             graph (Graph): A snapista Graph object.
             input_list (list of str): List of input paths.
             output_folder (str): Folder to save the output to.
             extension (str): The extension of the output.
             date_only (bool): Drop everything except the date (and suffix) from the output name.
             date_time_only (bool): Drop everything except the date and time (and suffix) from the output name.
             suffix (str): Suffix to use for output. By default, will consist of a list of applied operators.
             suppress_stderr (bool): Capture stderr without printing it.

         """

        for input_ in input_list:
            self.run(graph, input_, output_folder, extension, date_only, date_time_only, suffix, suppress_stderr)
