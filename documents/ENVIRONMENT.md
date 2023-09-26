# ENVIRONMENT DESIGN

The environment class instance consists of a set of voxels arranged along the
following axes: 
- X space (125 mm)
- Y space (125 mm)
- Time (seconds)

For each voxel, there are two outputs:
- Experienced surface irradiance, in W/m^2
- Experienced surface temperature, in C

The current datastructure implementation is a numpy array with a matched Pandas
Dataframe; numpy arrays are used for fast row merging and addition; dataframes
are for output.

The environment can be represented as a fixed grid of solar cells (125 mm x 125
mm) with the bottom left corner as (0, 0).  

---

## API

The environment shall be able to:

- Load and save a file representing the environment.
- Add and retrieve a voxel or voxels to and from the environment.
- Generate from a function a set of voxels that are added to the environment.
- Interpolate voxels between space and between time.
- Visualize these voxels in a 2D space over time.
