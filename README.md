# Neural open data

[![Build Status](https://travis-ci.com/seankmartin/PythonTemplate.svg?branch=master)](https://travis-ci.com/seankmartin/PythonTemplate)
[![Documentation Status](https://readthedocs.org/projects/pythontemplate/badge/?version=latest)](https://pythontemplate.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## How to convert to your project

1. Rename the folder `your_package` and edit `your_package/__init__.py`
2. Update `setup.py, version.txt, requirements.txt, dev_requirements.txt, LICENSE` to allow for users to install your package using `pip install .` or uploading to PyPI.
3. Update `README.md`.
4. Add the correct Makefile or batch script etc. to docs to allow for building documentation. Most likely this will use sphinx or pdoc3.
5. Add your tests to the tests folder that can be run with pytest or a similar testing framework.

Optionally, you could also setup continuous integration with CircleCI or similar, and setup git hooks.

Check [my website](https://seankmartin.netlify.app/python/getting-your-code-out-there/#uploading-your-package-to-pypi) for more information.


## Installation

Possibly could include docker later, there are some examples on Allensdk. Probably best to install on my laptop in this way.

Anyway, for non docker. You need Python 3.7 or 3.8. Then

```
pip install allensdk
pip install simuran
```

See [my website](https://seankmartin.netlify.app/computing/using-docker/) for more information on docker

## Dependencies

See `requirements.txt`

## Documentation

Later on read the docs.

## Contributing

Welcome.

## Licensing

MIT - see license file.

## Allen

1. See docs at https://allensdk.readthedocs.io/en/latest/
2. http://observatory.brain-map.org/visualcoding/search/cell_list?area=VISp&sort_field=p_sg&sort_dir=asc - cells from opto.
3. https://allensdk.readthedocs.io/en/latest/examples.html
4. https://allensdk.readthedocs.io/en/latest/visual_behavior_optical_physiology.html