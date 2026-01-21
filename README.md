# openlibrary - bootstrapper library for processing YML files

## Overview
The `openlibrary` library provides a bootstrapper library that loads a particular Python library referenced in a `yml` file/url and then runs the library on the `yml` file. It can be used to create separate custom Python libraries that operate on parameters stored in a `yml` file while ensuring the necessary external library is installed at runtime.

For example, the following command would install the Python library referenced in `opendem_conf.yml` and then run the library using `opendem_conf.yml` as the configuration file:
```
openlibrary opendem_conf.yml
```

## Purpose
The purpose of `openlibrary` is to build a modular approach to GIS dataset processing so standalone `yml` configuration files can be hosted on open data portals. When the `openlibrary` library is run on these `yml` files, it will install the core external libraries referenced in the `yml` and then run the dataset processing on the same `yml` file. 

Possible uses with existing external libraries:
- **opendem**: Download and process Digital Elevation Models (DEM) to produce vector slope or direction layers for renewable energy mapping.
- **openinspire**: Download and amalgamate INSPIRE land parcels to produce a single GPKG file that can be used for GIS data analysis.

## Installation

```
pip install git+https://github.com/SH801/openlibrary.git
```

To use the library, enter:

```
openlibrary http://domain/conf.yml

# OR

openlibrary /path/to/local/conf.yml

```

## Configuration file

The mandatory `.yml` configuration file provided on the command line should have the following format:

```
# Link to GitHub library code repository
codebase:
  https://github.com/[github_username]/[projectname].git 

# Library-specific parameters
...

```

For example:

```
codebase:
  https://github.com/SH801/opendem.git 

...

```
