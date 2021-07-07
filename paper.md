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

Estuarine circulation describes the water exchange between an estuary and the open ocean. The circulation is characterized by an inflow and outflow at different depths. Typically, the brackish water flows into the ocean near the surface, whereas more saline, thus denser, bottom water flows into the estuary. The TEF framework uses a continous isohaline framework rather than spatial coordinates `[@Walin_1977]` and combines it with the bulk concept of `[@Knudsen_1900]`. TEF was first introduced by `@MacCready_2011` and allows a profound understanding of the exchange flow of an estuary. For example, the full salinity range during a tidal cycle is only captured in the bulk values by using the isohaline framework. 
The `pyTEF` package provides the necessary tools to apply the TEF framework and is built on top of `xarray`. The `pyTEF` API allows an easy to use package that guides the user through a typical TEF analysis that can be applied to any given estuary. The implemented functions of `pyTEF` are based on code used for the scientific publications of `@Lorenz_etal_2019; @Lorenz_etal_2020` which have been improved to be quicker by suing the `numpy` library. Further, the package uses a numerically converging method to compute the bulk values which also allows for proper quantifaction of exchange flow of more than two layers as presented in `@Lorenz_etal_2019`. In addition, the package supports the analysis of exchange flow in more than one coordinate, e.g., temperature and salinity coordinates as presented in `@Lorenz_etal_2020`.

# Statement of need

`pyTEF` is an oceangraphic affiliated Python package for analyzing estuarine exchange flows. TEF is a well-established analysis framework in the estuarine community. It has been applied to several estuarine systems and based on it relationships between salt mixing and the exchange flow have been derived `[@MacCready_etal_2018;@Burchard_etal_2019]`. But a consistent application tool is still missing. Due to it's not intuitive nature TEF may be very intimidating to start with. It further takes some time to do the coding that is needed to get the desired results. `pyTEF` tries to solve these issues by providing all necessary functions to successfully apply the method and quantify the exchange flow. This allows a quick and easy analysis within a few lines of code based on open source code. This further leads to an easier and more transparent reproducibility of results. 

# Documentation and Implementation  

The technical, mathematical documentation and their references can be found under https://florianboergel.github.io/pyTEF/ and the accompanied PDF. Furthermore, two detailed examples are included which provide a guide on how to use the functionality of the package.

# Acknowledgements

The authors like to thank INSERT NAMES HERE for testing the package.

# References

