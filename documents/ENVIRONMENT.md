# ENVIRONMENT DESIGN

The environment class instance consists of a set of voxels arranged along the following axes: 
- X space (125 mm)
- Y space (125 mm)
- Time (seconds)

For each hypervoxel, there are two outputs:
- Experienced surface irradiance, in W/m^2
- Experienced surface temperature, in C

The current datastructure implementation is a numpy array with a matched Pandas
Dataframe; numpy arrays are used for fast row merging and addition; dataframes
are for output.

The environment can be represented as a fixed grid of solar cells (125 mm x 125 mm) with the bottom left corner as (0, 0). 

---

## API

```python
def load_env(self, filepath: str) -> None
def save_env(self, filepath) -> None
def add_voxel(self, X: int, Y: int, T: int, irrad: float, temp: float) -> None
def add_voxels(self, X: list[int], Y: list[int], T: list[int], irrad: list[float], temp: list[float]) -> None
def gen_voxels(self, func) -> None
def interp_voxels(self) -> None
def vis_voxels(self) -> None
def get_voxels(self) -> DataFrame
def get_voxels_slice(self, idx: int, axis: str = "T") -> DataFrame
```

---

## Tests

The required functional tests involve being able to update and display a voxel
surface graph for both irradiance and temperature over time.
