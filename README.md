# pyTEF
> pyTEF is a Python package that can be used to apply the Total Exchange (TEF) analysis framework to analyze the exchange flow of an estuary.


To do so TEF analyzes the exchange flow in salinity and/or temperature coordinates rather than spatial coordinates. This package provides the necessary tools to use the TEF framework and is built on top of xarray.

## Installing


To install use

`git clone https://github.com/florianboergel/pyTEF.git` and then 

`pip install -e pyTEF`

## How to use

`00_tef_core.ipynb` contains the TEF framework and all documentation.

`01_calc.ipynb` mainly contains the coordinate transformation of the transport terms and the calculation of the bulk values

Further you find different examples on how to use the TEF framework.

- `02_example_analytical.ipynb` - validation of the pyTEF package

- `03_example_persian_gulf.ipynb` - example TEF analysis applied to the Persian Gulf


## Learn about TEF

The TEF analysis framework (MacCready, 2011; Lorenz et al., 2019) allows a consistent calculation of the transports and salinities of an exchange flow in salinity space (or every other coordinate). The main idea of TEF is that transports of volume and salinity in and out the estuary of the same salinity partially compensate since only the net exchange changes salinity and volume of the estuary.

The reader is referenced to the following literature:

- [PhD thesis of Marvin Lorenz](http://rosdok.uni-rostock.de/resolve/id/rosdok_disshab_0000002489?_search=89c68482-f7cc-4363-89af-58ddebb819c2&_hit=0)

- MacCready, P., 2011: Calculating estuarine exchange flow using isohaline coordinates. Journal of Physical Oceanography, 41 (6), 1116–1124.

- Lorenz, M., Klingbeil, K., MacCready, P., and Burchard, H. (2019) Numerical issues of the Total Exchange Flow (TEF) analysis framework for quantifying estuarine circulation, Ocean Sci., 15, 601-614, https://doi.org/10.5194/os-15-601-2019

- Lorenz, M., Klingbeil, K., and Burchard, H. (2020) Numerical Study of the Persian Gulf using an Extended Total Exchange Flow Analysis Framework, J. Geophys. Res. Oceans, 125, e2019JC015527, https://doi.org/10.1029/2019JC015527


## What's new 

### v1.0 (15.07.2021)

- updated README.md 
- ready for submission (JOSS)

### v0.3 (07.07.2021)

- improvements in code and documentation
    - examples are completed
    - documentation of the functions and examples 

### v0.2 (07.06.2021)

- first version of pyTEF ready for testing
    - example cases added
    - calculation of bulk values
    - algorithm that finds minima and maxima in a given Q profile
    - added documentation

### v0.1 (25.05.2021)

- implementation of 2D sorting
