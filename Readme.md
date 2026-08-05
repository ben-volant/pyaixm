# pyaixm-v

Parses Aeronautical Information Exchange Model (AIXM) xml data to python dataclasses.

This is a fork of [pyaixm](https://github.com/volkerp/pyaixm), developed for the specific requirements of Volant Autonomy Ltd. though is intended to be a general purpose and complete utility.


## Installation and usage

After cloning this repository
```bash
$ pip install .
```

File *example.py*
```python
from pprint import pprint
import sys

import pyaixm

if __name__ == '__main__':
    with open(sys.argv[1], 'rb') as f:
        features = pyaixm.parse(f, resolve_xlinks=True)
        pprint(features)

```
Function *parse()* parses xml from file. If *resolve_links* is true xlink:href referrences are
replaced with the features i.e. dataclasses they refer to. Otherwise the *target* attribute on the XLink
dataclass referrs to the feature.


The package can be executed directly. It dumps the AIXM data as json.
```bash
$ python -m pyaixm aixm_input_file.xml
```


Example aixm data file can be found in
* https://github.com/aixm/donlon
* https://aip.dfs.de/datasets/
* https://github.com/volkerp/aixm
* https://github.com/ben-volant/aixm_procedure_example




