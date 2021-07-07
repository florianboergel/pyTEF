---
title: 'pyTEF: A Python package for the Total Exchange Flow (TEF) analysis framework'
tags:
  - Python
  - estuary
  - dynamics
  - exchange flow
  - salinity
  - temperature
authors:
  - name: Marvin Lorenz^[co-first author] # note this makes a footnote saying 'co-first author'
    orcid: 0000-0002-9853-7775
    affiliation: 1 # (Multiple affiliations must be quoted)
  - name: Florian Börgel^[co-first author]
    orcid: 0000-0003-3294-667X
    affiliation: 1
affiliations:
 - name: Leibniz Institute for Baltic Sea Research Warnemünde, Rostock, Germany
   index: 1
date: 07 July 2021
bibliography: paper.bib
---

# Summary

Estuarine circulation describes the water exchange between an estuary and the open ocean. The circulation is characterized by an inflow and outflow at different depths. Typically, the upper layer consists of brackish water flowing into the ocean, whereas the bottom layer consists of more saline, thus denser, water flowing into the estuary. The TEF framework uses a continous isohaline framework rather than spatial coordinates (Walin, 1977) and combines it with the bulk concept of Knudsen (1900). TEF was first introduced by MacCready (2011) and allows a profound understanding of the exchange flow of an estuary. For example, the full salinity range during a tidal cycle is only captured in the bulk values by using the isohaline framework. The pyTEF package provides the necessary tools to apply the TEF framework and is built on top of xarray.

# Statement of need

`pyTEF` is an oceangraphic affiliated Python package for analyzing estuarine exchange flow. The `pyTEF` API allows an easy to use package that guides the user through a typical TEF analysis that can be applied to any give estuary. Further, the package uses non-trivial mathematical application that have been proven to be numerical stable (Lorenz et al., 2019). TEF is a well established analyis framework in the estuarine community but a consisted application tool is still missing.

The implemented functions of `pyTEF` alreay have been used in a number of scientific publications. Further, the functions rely heavilly on the  Python library `numpy` which uses an underlying C implementation allowing a rather fast execution of high computational tasks.

# Documentation and Implementation  

The technical and mathematical documentation and their references can be found under https://florianboergel.github.io/pyTEF/ and the accompanied PDF.

# References TODO

- Burchard, H., et al. (2018) The Knudsen theorem and the Total Exchange
Flow analysis framework applied to the Baltic Sea. Progress in Oceanography,
10.1016/j.pocean.2018.04.004.

- Lorenz, M., Klingbeil, K., and Burchard, H. (2020) Numerical Study of the Persian Gulf using an Extended Total Exchange Flow Analysis Framework, J. Geophys. Res. Oceans, 125, e2019JC015527, https://doi.org/10.1029/2019JC015527

- Lorenz, M., Klingbeil, K., MacCready, P., and Burchard, H. (2019) Numerical issues of the Total Exchange Flow (TEF) analysis framework for quantifying estuarine circulation, Ocean Sci., 15, 601-614, https://doi.org/10.5194/os-15-601-2019
