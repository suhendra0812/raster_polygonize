# Raster Polygonize

Polygonizing raster file (GeoTIFF) using `rasterio` and `geopandas`.

## Install dependency
#### Windows
- Install `GDAL` and `Fiona` as rasterio and geopandas dependency using `pipwin`.

```console
$ pip install pipwin
$ pipwin install GDAL
$ pipwin install fiona
```
- Install other dependencies in requirements.txt file
```console
$ pip install -r requirements.txt
```
#### Linux (Ubuntu)
- Follow instructions on [here](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html) to install GDAL in Ubuntu
- Install other dependencies in requirements.txt file
```console
$ pip install -r requirements.txt
```