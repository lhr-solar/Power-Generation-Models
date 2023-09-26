# SYSTEM DESIGN

The system design revolves around the simulation of the entire power generation
chain, modeling the environment all the way to the load. In this simulation
software, the system design allows us to control aspects of the system, in
particular:

- Creation of environmental test regimes,
- Design of a photovoltaic system that mimics that on expected real-world
  deployment,
- Translation of the PV system across the environment through space and time to
  simulate various environmental and shading effects,
- Test topologies and control schemes of the conversion hardware that leverage
  PV generation into usable energy, and
- Analyze output effects into resistive, inductive, and capacitive loads.

---

## High Level Overview

```mermaid
flowchart
    ENV(Environment)
    SRC(Source)
    CONV(Converter)
    CONT(Controller)
    LOAD(Load)
    ANA([Analysis])

    ENV--->SRC
    SRC-->CONV
    CONT<---->CONV
    LOAD-->CONV

    ENV----->ANA
    SRC---->ANA
    CONV--->ANA
    LOAD-->ANA
```

---

## Low Level Overview

```mermaid
flowchart
  subgraph Environment
  ENV(Environment)
  end

  subgraph Source
  PV(PV System)
  CEL(Cell)
  3CEL(Three Param)
  5CEL(Five Param)
  DIO(Diode)
  MOD(Module)
  PAN(Panel)
  end

  subgraph Converter
  SEN(Sensor)
  CON(Controller)
  ACT(Actuator)
  PRO(Process)
  end

  subgraph Load
  LEAD(Lead Acid)
  LNMC(LiNiMnCo)
  LION(Lithium Ion)
  BATT(Battery System)
  end

  subgraph Controller Algorithms
  MPPT(MPPT)
  SUBL(Sublocal)
  LOCL(Local)
  GLOB(Global)
  end

  ENV   -->     PV
  3CEL  -->     CEL
  5CEL  -->     CEL
  CEL   -->     MOD
  DIO   -->     MOD
  MOD   -->     PAN
  CEL   -->     PV
  MOD   -->     PV
  PAN   -->     PV

  LEAD  -->     BATT
  LNMC  -->     BATT
  LION  -->     BATT

  PV    -->     SEN
  BATT  ------->     SEN
  SEN   -->     CON
  CON   -->     ACT
  ACT   -->     PRO
  PRO   -->     SEN

  SUBL  -->     LOCL
  LOCL  -->     GLOB
  LOCL  -->     MPPT
  GLOB  -->     MPPT
  MPPT  -->     CON

  subgraph Analysis
  STAB(Stability)
  EFF(Efficiency)
  POW(Power)
  end

  ENV   -->     POW
  PV    -->     POW
  BATT  -->     POW
  CON   -->     EFF
  PRO   -->     STAB
```
