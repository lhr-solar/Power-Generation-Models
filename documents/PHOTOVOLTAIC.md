# PHOTOVOLTAIC DESIGN

The photovoltaic class instance consists of a hierarchy of components, from
cells to modules to panels. They are executed bottom up, in which lower level
instances affect the operation of higher level instances. The user should be
able to design a photovoltaic system from a collection these components, and
model them appropriately in relation to environmental conditions.

- Cell : (X, Y) position relative to canvas
- Module : (X, Y) position relative to canvas
  - Cell in module : (X2, Y2) position relative to Module centered around (0, 0)
- Panel : (X, Y) position relative to canvas
  - Module in panel : (X2, Y2) position relative to Panel centered around (0, 0)
    - Cell in module : (X3, Y3) position relative to Module centered around (0, 0)
        
Modifying the position of the module translates the canvas position of all cells
in the module and likewise for modules in a panel.

---

## API

The photovoltaics shall be able to:

- Define a set of parameters that may be used for modeling; these parameters are
  split into **reference parameters** and **fitting parameters**.
  - Reference parameters are measured and provided by the designer. They may
    include things like known exposed irradiance or manufacturer provided open
    circuit voltage.
  - Fitting parameters are analytically derived from the model. They are
    experimental values and may vary between individual PVs.
- Be assigned to an environmental model: the PV may move around in the space or
  canvas that is represented by voxels in the environment, and the output of the
  PV is dependent on the voxel(s) that is associated with the PV component.
  There is only one Environment instance.
- Solve for a PV current given voltage and vice versa. We assume that all
  devices sans bypass diodes are in series: this means that it is easier to
  derive voltage from current than vice versa. However, we can use the relative
  resolution of the model to interpolate current from the voltage after
  generating an I-V curve.
- Generate derivations of the current given voltage; this includes the full I-V
  curve and edge characteristics, including maximum power point and effective
  open circuit voltage/short circuit current.
- Load and save a file representing the PV. This includes values for fitting
  parameters. 
- Load and preprocess a data file representing experimental data at some known
  set of reference parameters. From this data file, we shall be able to perform
  best fit algorithms to optimize fitting parameters.
- Visualize the PV (discrete or whole) I-V curves and key points over time and
  across various conditions. The user should specify these conditions.

---

## Solar Cell Models

Solar cells are the lowest model in the hierarchy. All cells have configurable
properties specific to two sets of factors: **external environmental factors**
and **internal intrinsic factors**.  

- External factors include incident irradiance and surface temperature and are
  generated from the environment model.  
- Internal factors are dependent on cell construction and must be derived from
  (a) manufacturer specifications and/or (b) testing using the I-V Curve
  Tracer PCB. They are tied to the instance of the cell and generally do not
  change unless the cell experiences damage. 
- Cell models can range from simplistic to highly derived and complex; several 
  models are investigated here and should be interchangeable when reloading
  the overall model. All cells should use the same model during runtime. 

### Three Parameter Model

### Modified Three Parameter Model

### Five Parameter Model

### Modified Five Parameter Model

---

## Solar Module Model

The solar module consists of several solar cell models in series; the cells may
experience a variance of irradiance and temperature and this should be reflected
properly in the final model in determining cell matching and final I-V curve
operation. Modules also have a reverse biased bypass diode in parallel with the
set of cells; this diode retains its own model and is calculated against the
module I-V curve.

Current applied through a solar module is checked against the resultant voltage
across the module. If this is driven into the 2nd quadrant (negative voltage,
positive current), then the bypass diode is turned on, distributing current
until the voltage across both devices (cells and bypass diode) are equivalent.

### Solar Cell Set Model

### Bypass Diode Models

---

## Solar Panel Model

The solar panel model is the largest model and consists of solar modules in
series. The only addition to this model is the inclusion of lead resistance,
which a linear voltage drop in proportion to the current driven through the
panel.
