# Total Exchange Flow (TEF)
> TEF analyzes the exchange flow of an estuary in salinity and/or temperature coordinates rather than spatial coordinates since the dynamics of most estuaries are controlled by the salt distribution. 


## Installing

`pip install TotalExchangeFlow`

## How to use

`00_tef_core.ipynb` contains the TEF framework and all documentation.

Further you find different examples on how to use the TEF framework.

- `01_example_persian_gulf.ipynb`

## Learn about TEF

The TEF analysis framework (Burchard et al., 2018; Lorenz et al., 2019; MacCready, 2011) allows a consistent calculation of the transports and salinities of an exchange flow in salinity space. The main idea of TEF is that transports of volume and salinity in and out the estuary of the same salinity partially compensate since only the net exchange changes salinity and volume of the estuary.

The reader is referenced to the follwing literature:

- [PhD thesis of Marvin Lorenz](http://rosdok.uni-rostock.de/resolve/id/rosdok_disshab_0000002489?_search=89c68482-f7cc-4363-89af-58ddebb819c2&_hit=0)

- Burchard, H., et al. (2018) The Knudsen theorem and the Total Exchange
Flow analysis framework applied to the Baltic Sea. Progress in Oceanography,
10.1016/j.pocean.2018.04.004.

- Lorenz, M., Klingbeil, K., and Burchard, H. (2020) Numerical Study of the Persian Gulf using an Extended Total Exchange Flow Analysis Framework, J. Geophys. Res. Oceans, 125, e2019JC015527, https://doi.org/10.1029/2019JC015527

- Lorenz, M., Klingbeil, K., MacCready, P., and Burchard, H. (2019) Numerical issues of the Total Exchange Flow (TEF) analysis framework for quantifying estuarine circulation, Ocean Sci., 15, 601-614, https://doi.org/10.5194/os-15-601-2019

- MacCready, P., 2011: Calculating estuarine exchange flow using isohaline coordinates. Journal of Physical Oceanography, 41 (6), 1116–1124.

## What's new 

### v0.1 (25.05.2021)

- implementation of 2D sorting


All variables have to be in the xarray dataset. variable konsistent benennen
schichtdicke nicht depth
