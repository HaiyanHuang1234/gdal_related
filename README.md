# Geospatial Raster Processing Utilities

A collection of Python utilities for common geospatial raster processing tasks using GDAL. The repository currently includes tools for mosaicking large GeoTIFF datasets and reprojecting rasters to a common coordinate reference system.

---

## Repository Structure

```text
.
├── merge_big_geotif.py
├── reproject_two_geotifs.py
└── README.md
```

### Files

| File                       | Description                                                                               |
| -------------------------- | ----------------------------------------------------------------------------------------- |
| `merge_big_geotif.py`      | Merge multiple GeoTIFF files into a single compressed BigTIFF mosaic.                     |
| `reproject_two_geotifs.py` | Reproject one GeoTIFF to match the projection, resolution, and extent of another GeoTIFF. |
| `README.md`                | Repository documentation.                                                                 |

---

## Features

### merge_big_geotif.py

* Merge hundreds or thousands of GeoTIFF files.
* Uses GDAL Virtual Raster (VRT) for memory-efficient processing.
* Supports very large output mosaics through BigTIFF.
* Produces tiled and compressed GeoTIFF outputs.
* Suitable for:

  * HLS products
  * Landsat mosaics
  * Sentinel-2 mosaics
  * Classification products
  * Burned area maps

### reproject_two_geotifs.py

* Reproject rasters to a common coordinate reference system.
* Match spatial resolution and alignment.
* Generate analysis-ready datasets.
* Simplify multi-sensor raster comparisons.

---

## Requirements

### Python Packages

```bash
pip install numpy
pip install GDAL
```

or

```bash
pip install numpy gdal
```

### Verify GDAL Installation

```python
from osgeo import gdal

print(gdal.VersionInfo())
```

---

## Example: Merge Multiple GeoTIFFs

```python
from merge_big_geotif import merge_big_geotif

files = [
    "tile_01.tif",
    "tile_02.tif",
    "tile_03.tif"
]

merge_big_geotif(
    files,
    "mosaic.tif"
)
```

### Output

```text
Mosaic written to: mosaic.tif
```

---

## Example: Merge an Entire Directory

```python
import glob

from merge_big_geotif import merge_big_geotif

files = glob.glob("tiles/*.tif")

merge_big_geotif(
    files,
    "north_america_mosaic.tif"
)
```

---

## Example: Reproject a GeoTIFF

```python
from reproject_two_geotifs import reproject_two_geotifs

reproject_two_geotifs(
    "input.tif",
    "reference.tif",
    "output.tif"
)
```

### Typical Applications

* Harmonized Landsat Sentinel-2 (HLS)
* Landsat Collection 2
* Sentinel-2
* PlanetScope
* MODIS products
* Burned area mapping
* Land-cover classification
* Multi-sensor data fusion
* 

---

## Performance Notes

### Mosaic Generation

The mosaic utility uses:

```text
GDAL BuildVRT
      ↓
GDAL Warp
      ↓
Compressed BigTIFF
```

This approach is significantly more memory efficient than loading all rasters into memory simultaneously.

### Output Options

The generated mosaics use:

```text
TILED=YES
COMPRESS=LZW
BIGTIFF=YES
```

which provides:

* Faster raster access
* Reduced storage requirements
* Support for files larger than 4 GB

---

## Applications

These utilities are particularly useful for:

* Remote sensing workflows
* Earth observation products
* Large-scale raster mosaics
* Geospatial preprocessing
* Machine learning data preparation
* Cloud and HPC processing environments

---

## Author

Haiyan Huang



---

## License

This repository is provided for research and educational purposes.
