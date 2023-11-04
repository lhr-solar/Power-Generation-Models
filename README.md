# :sunny: Models - Modeling the Power Generation System.

- [:sunny: Models - Modeling the Power Generation System.](#sunny-models---modeling-the-power-generation-system)
  - [Repository Structure](#repository-structure)
  - [Maintainers](#maintainers)
  - [Versioning](#versioning)
  - [TODO](#todo)
    - [Models](#models)
      - [PV](#pv)
      - [Converter](#converter)

---

## Repository Structure

- **documents** - contains relevant datasheets, papers, and notes about modeling
  various aspects of the power generation system. 
- **common** - shared python utilities for unit testing and graphics
  visualization. 
- **environment** - modeling external environmental effects on photovoltaics, in
  particular irradiance and surface temperature over time.
- **pvs** - modeling photovoltaics, from solar cells to modules to solar arrays.
- **mppt** - modeling the hardware of the MPPT as well as the MPPT algorithms.
- **load** - modeling the loads that may be attached to the MPPT, in particular
  the batteries.

---

## Maintainers

The current maintainer of this project is Matthew Yu as of 07/17/2023. His email
is [matthewjkyu@gmail.com](matthewjkyu@gmail.com).

Contributors to the SW encompass many dedicated students, including:

- Afnan Mir
- Roy Mor

Special thanks to Professor Gary Hallock, who supervised the development and
design of this project.

---

## Versioning

This SW is on version `0.1.0`. We use [semantic
versioning](https://semver.org/) to denote between versions. See the
[changelog](./docs/CHANGELOG.md) for more details.

---

## TODO

### Models

#### PV

- [ ] pv
  - [x] modify get_edge to support user specified current, voltage range.
  - [ ] docs for vis
  - [x] support supply experimental data overlay
  - [x] support returning a widget
  - [ ] support returning a sweep across external/internal parameters
  - [ ] support multiple graphs
  - [x] docs for _set_params_and_fit

- panel/panel
- pv_system

#### Converter

- [ ] sensor
  - [ ] voltage sensor
  - [ ] current sensor
- [ ] controller
  - [ ] mppt algorithms
- [ ] actuator
  - [ ] boost converter
- [ ] process

- three_param_cell
  - test_sanity
    - verify is reasonable
  - test_equiv
    - bug where get_current not equiv to get_voltage
  - test_fit_data
    - implement fit data, verify reasonable parameters generated against prior
      data from data folder  
  - main
    - verify visualization for [-10, 10]A, [-1.0, 1.0]V.
- bypass diode
  - test_sanity
    - verify is reasonable
  - test_equiv
    - verify for correctness
  - test_fit_data
    - implement fit data, no test data to use.
  - main
    - verify visualization for [-1, 1]A, [-0.5, 0.5]V.
- module
- panel
- pv_system