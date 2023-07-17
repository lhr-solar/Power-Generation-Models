# :sunny: Models - Modeling the Power Generation System.

- [:sunny: Models - Modeling the Power Generation System.](#sunny-models---modeling-the-power-generation-system)
  - [Repository Structure](#repository-structure)

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

### 