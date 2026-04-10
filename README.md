[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19502867.svg)](https://doi.org/10.5281/zenodo.19502867)

# [LDACS-GeoOpt-Simulator](https://github.com/ComNetsHH/LDACS-GeoOpt-Simulator)

## Copyright and License

This repository is distributed under the GNU Lesser General Public License v3.0 or later.
See [`LICENSE.txt`](LICENSE.txt) for details.

## Overview

`LDACS-GeoOpt-Simulator` is a paper-specific OMNeT++ simulator repository for evaluating
GeoOpt routing in sparse LDACS air-to-air networks. It is focused on the French airspace
equipage-fraction scenario used for the GeoOpt study.

## Main comparison set

The included scenario and scripts are prepared to compare:

- [Greedy-1](https://github.com/ComNetsHH/LDACS-Greedy-K-Hop-Routing)
- [GPSR](https://github.com/ComNetsHH/LDACS-GPSR-Routing)
- [GeoOpt](https://github.com/ComNetsHH/LDACS-GeoOpt-Routing)
- [Dijkstra](https://github.com/ComNetsHH/LDACS-Dijkstra): Implements the Dijkstra's shortest path routing algorithm which serves as a baseline.

## Repository structure

- `scenarios/` — NED network and OMNeT++ configuration files
- `scenarios/results/` — Makefile, plotting environment, and result-processing scripts

## Installation

Clone the repository and run:

```bash
git clone https://github.com/ComNetsHH/LDACS-GeoOpt-Simulator
cd LDACS-GeoOpt-Simulator
bash install.sh
```

The installation prepares the workspace under `omnetpp-5.6.2/workspace/`.

It downloads or clones the required simulator dependencies, including:

- OMNeT++ 5.6.2
- INET 4.2.5
- `LDACS-Abstract-Radio`
- `LDACS-Abstract-TDMA-MAC`
- `LDACS-Greedy-K-Hop-Routing`
- `LDACS-Dijkstra`
- `LDACS-GPSR-Routing`
- `LDACS-GeoOpt-Routing`

## Local execution

```bash
cd scenarios/results
make build-release
make run-paper-simulations-local
make generate-all-equipageFraction-csv
make plot-equipage-fraction-metrics
```

## HPC execution

```bash
cd scenarios/results
make run-all-simulations-from-hpc-equipageFraction
```

## Notes

- The workspace root used by the Makefile and shell helpers is `../../omnetpp-5.6.2/workspace/`.
- The GeoOpt routing implementation is intended to live in its own routing repository.
- The plotting scripts assume OMNeT++ result files are exported into `scenarios/results/simresults/`.
