import logging
from pathlib import Path
from typing import Any, Optional

import geopandas as gpd
import rasterio.features as riofeat
import rioxarray
from shapely.geometry import shape

logger = logging.getLogger(__name__)

def polygonize(raster_path: Path, band_name: Any) -> Optional[gpd.GeoDataFrame]:
    logger.info("Polygonize...")
    data = rioxarray.open_rasterio(raster_path)
    data = data.sel(band=band_name) 
    data = data.where(data == 0, 1) # homogenize all pixel value beside 0 to 1
    shapes = list(riofeat.shapes(data, transform=data.rio.transform()))

    geoms = []
    values = []
    for geom, value in shapes:
        if value == 1:
            geoms.append(shape(geom))
            values.append(value)

    if not geoms:
        logger.warning(f"No geometry found!")
        return

    polygon_gdf = gpd.GeoDataFrame(data={"value": values}, geometry=geoms, crs=data.rio.crs)
    polygon_gdf.geometry = polygon_gdf.geometry.convex_hull
    return polygon_gdf

def main() -> None:
    RASTER_DIR = Path("./raster") # set the directory contain tiff files
    OUTPUT_DIR = Path("./output") # set the output directory to save the output shapefile

    raster_paths = sorted(RASTER_DIR.glob("*.tif"))
    for i, raster_path in enumerate(raster_paths):
        logger.info(f"({i+1}/{len(raster_paths)}) {raster_path}")
        polygon_gdf = polygonize(raster_path, band_name=1) # in this case, band name in the tiff files is grayscale and contain 1 band only
        if polygon_gdf is not None:
            output_path = OUTPUT_DIR / f"{raster_path.stem}.shp"
            polygon_gdf.to_file(output_path)
            logger.info(f"Saved to {output_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    main()

