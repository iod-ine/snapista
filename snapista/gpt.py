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

    def run(self, graph, input_, output_folder='proc', format_='BEAM-DIMAP', date_only=False, date_time_only=False,
            prefix=None, suffix=None, suppress_stderr=True):
        """ Run the graph for the input.

         Args:
             graph (Graph): A snapista Graph object.
             input_ (str, os.PathLike, or list): Input or list of inputs.
             output_folder (str): Folder to save the output to.
             format_ (str): The extension of the output, e.g. 'GeoTIFF', 'HDF5', 'BEAM-DIMAP'.
             date_only (bool): Drop everything except the date (and suffix) from the output name.
             date_time_only (bool): Drop everything except the date and time (and suffix) from the output name.
             prefix (str): Prefix to use for output.
             suffix (str): Suffix to use for output. By default, will consist of a list of applied operators.
             suppress_stderr (bool): Capture stderr without printing it.

         """

        if isinstance(input_, list):
            for product in input_:
                self.run(
                    graph=graph,
                    input_=product,
                    output_folder=output_folder,
                    format_=format_,
                    date_only=date_only,
                    date_time_only=date_time_only,
                    prefix=prefix,
                    suffix=suffix,
                    suppress_stderr=suppress_stderr,
                )
            return

        input_ = pathlib.Path(input_)

        with tempfile.TemporaryDirectory() as temp_dir:
            base = pathlib.Path(temp_dir)
            graph_file = base / 'graph.xml'
            prefix = '' if prefix is None else prefix
            suffix = graph.suffix if suffix is None else suffix

            output_file = pathlib.Path(output_folder)
            output_file.mkdir(exist_ok=True)

            if date_only:
                date_regex = re.compile(r'(\d{4})(\d{2})(\d{2})T\d{6}')
                date = date_regex.findall(str(input_))[0]
                output_file = output_file / '{}{}-{}-{}{}'.format(prefix, *date, suffix)
            elif date_time_only:
                date_time_regex = re.compile(r'(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})')
                date_time = date_time_regex.findall(str(input_))[0]
                output_file = output_file / '{}{}-{}-{}T{}-{}-{}{}'.format(prefix, *date_time, suffix)
            else:
                output_file = output_file / f'{prefix}{input_.stem}{suffix}'

            # Sentinel-3 is a special snowflake in terms of reading in the products.
            # GPT and SNAP refuse to open Sentinel-3 archives and only open the xfdumanifest.xml
            # file that is within the product folder.

            # TODO: replace the full name with a short summary, i.e. S3 OLCI WFR from <date>
            print(f'⏳ {input_.stem}')

            if input_.match('*S3*.zip'):
                with zipfile.ZipFile(input_) as zf:
                    zf.extractall(temp_dir)
                input_ = base / (input_.stem + '.SEN3') / 'xfdumanifest.xml'
            elif input_.match('*S3*.SEN3'):
                input_ = input_ / 'xfdumanifest.xml'

            graph.save(graph_file)

            process = subprocess.run(
                [self.gpt, str(graph_file), f'-Ssource={input_}', '-t', output_file, '-f', format_],
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

                # when stderr is not suppressed, it is not captured and the error is visible anyway
                if suppress_stderr:
                    error_regex = re.compile(r'Error: (.*)')
                    error = error_regex.findall(process.stderr.decode())[0]
                    error = '\n'.join(f'    {line}' for line in textwrap.wrap(error, width=66))
                    print(error)
