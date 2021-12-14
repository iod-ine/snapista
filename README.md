# snapista – a frictionless Python wrapper for SNAP GPT
This version of snapista is my personal take on what is originally presented [here](https://github.com/snap-contrib/snapista).

### What's different

- In my vision, the central object of the package is not the graph, but `gpt` itself.
- The `snapista.GPT` object is initiated with a path to `gpt` to avoid any confusions with system's `PATH`. <br/>
- There is no dependence on `snappy`.
Instead, the operators are manually defined through the `snapista.operators` package.
- The descriptions for operators are included into the docstrings, so they are accessible via `help(operator)` or `operator?` in interactive environments.
- The parameters are set by setting the corresponding operator's properties, and they are in Python types (the booleans are `True` and `False` instead of `'true'` and `'false'` and lists are actual Python lists).
- `snapista.GPT.run` method is very flexible in terms of output formatting.

Below is an example of one of my personal workflows that I also used for testing.
```python
import os
import pathlib
import snapista

gpt_path = pathlib.Path('~/.esa-snap/bin/gpt').expanduser()

data = pathlib.Path('Data') / 'raw' / 'MSI'
products = [data / f for f in os.listdir(data) if 'S2' in f]

gpt = snapista.GPT(gpt_path)

resample = snapista.operators.Resample()
resample.reference_band = 'B2'

import_vector = snapista.operators.ImportVector()
import_vector.separate_shapes = False
import_vector.vector_file = '/home/codycofan/Vectors/Land.shp'

land_sea_mask = snapista.operators.LandSeaMask()
land_sea_mask.use_srtm = False
land_sea_mask.geometry = 'Land'
land_sea_mask.invert_geometry = True

graph = snapista.Graph()
graph.add_node(resample)
graph.add_node(import_vector)
graph.add_node(land_sea_mask)

gpt.run(
    graph,
    products,
    output_folder='Data/proc',
    format_='BEAM-DIMAP',
    date_time_only=True,
    prefix='S2_',
    suppress_stderr=True,
)

```

### Installation
I don't have an installation option yet. I will look into uploading it to PyPI as soon as I come with a cool name that makes it clear that that is not the original snapista.
To run tests, I manually insert the path to the local repository into Python's `sys.path`.

```python
import sys
import pathlib

snapista_path = pathlib.Path('~/Projects/snapista/').expanduser()

if str(snapista_path) not in sys.path:
    sys.path.insert(0, str(snapista_path))

import snapista
```
