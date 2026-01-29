<!-- start docs-include-index -->

# geodesy

[![PyPI](https://img.shields.io/pypi/v/geodesy)](https://img.shields.io/pypi/v/geodesy)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/geodesy)](https://pypi.org/project/geodesy/)
[![CI](https://github.com/sgraaf/geodesy/actions/workflows/ci.yml/badge.svg)](https://github.com/sgraaf/geodesy/actions/workflows/ci.yml)
[![Test](https://github.com/sgraaf/geodesy/actions/workflows/test.yml/badge.svg)](https://github.com/sgraaf/geodesy/actions/workflows/test.yml)
[![Documentation Status](https://readthedocs.org/projects/geodesy/badge/?version=latest)](https://geodesy.readthedocs.io/en/latest/?badge=latest)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/11851/badge)](https://www.bestpractices.dev/projects/11851)

*geodesy* is a zero-dependency, pure Python package for handling coordinates. It can convert coordinates for a point from one Coordinate Reference System (CRS) to another, and also calculate distance and bearing between points.

<!-- end docs-include-index -->

## Installation

<!-- start docs-include-installation -->

*geodesy* is not yet available on [PyPI](https://pypi.org/project/geodesy/). Install with [uv](https://docs.astral.sh/uv/) or your package manager of choice:

```shell
uv add "geodesy @ git+https://github.com/sgraaf/geodesy"
```

<!-- end docs-include-installation -->

## Documentation

Check out the [*geodesy* documentation](https://geodesy.readthedocs.io/en/stable/) for the [User's Guide](https://geodesy.readthedocs.io/en/stable/usage.html) and [API Reference](https://geodesy.readthedocs.io/en/stable/api.html).

## Usage

<!-- start docs-include-usage -->

### Add one

```python
from geodesy import add_one


# add one to 3
four = add_one(3)
```

<!-- end docs-include-usage -->
