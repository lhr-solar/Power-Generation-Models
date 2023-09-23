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

```python
def __init__(filepath: str, hierarchy: str) -> None
def load_pv(filepath: str) -> None
def save_pv(filepath: str) -> None

# Building and adjusting the photovoltaic.
# Only one of these is accessible after setting the hierarchy.
def add_cell(id: int, cell: Cell, X: int, Y: int) -> bool
def add_module(id: int, module: Module, X: int, Y: int) -> bool
def add_string(id: int, string: String, X: int, Y: int) -> bool
def rem_item(id: int) -> bool
def set_item_position(id: int, X: int, Y: int) -> None
def set_pv_position(X: int, Y: int) -> None

# Running the models and extracting the result.
def get_item_current(id: int, item_voltage: float, env: Environment, time: int) -> float
def get_item_iv(id: int, env: Environment, time: int) -> [float, float]
def get_item_edge(id: int, env: Environment, time: int) -> (float, float), (float, float), float
def get_pv_current(pv_voltage: float, env: Environment, time: int) -> float
def get_pv_iv(env: Environment, time: int) -> [float, float]
def get_pv_edge(env: Environment, time: int) -> (float, float), (float, float), float

# Model fit.
# def load_data(filepath: str, raw_data: pd.DataFrame) -> None
# def norm_data()
# def fit_parameters()
# def get_parameters()

# Visualization
def vis_item(id: int, env: Environment, time_range: [int, int]) -> None
def vis_pv(env: Environment, time_range: [int, int]) -> None
```

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

### Solar Cell Set Model

### Bypass Diode Models

---

## Solar Panel Model

The solar panel model is the largest model and consists of solar modules in
series.

---

## Interaction with the Environment

The environment is 