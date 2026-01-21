# openlibrary - bootstrapper library for processing YML files

## Overview
The `openlibrary` library provides a bootstrapper library that loads a particulary library referenced in a `yml` URL and then runs the library on that `yml` file.

## Installation

```
pip install git+https://github.com/SH801/openlibrary.git
```

To use the library, enter:

```
openlibrary http://domain/library.yml
```

## Configuration file

The `.yml` configuration file that is input should have the following format:

```
# ----------------------------------------------------
# sample.yml
# Sample yml configuration file
# ----------------------------------------------------

# Link to GitHub library code repository, for example
  https://github.com/SH801/opendem.git

# Library-specific parameters
...

```

