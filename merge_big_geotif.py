#!/usr/bin/env python
# coding: utf-8

# In[ ]:
#
"""
    Merge multiple GeoTIFF files into a single mosaic GeoTIFF.

    This function creates a GDAL Virtual Raster (VRT) from a collection
    of input GeoTIFF files and then uses GDAL Warp to generate a tiled,
    compressed BigTIFF mosaic. The workflow is memory efficient and
    suitable for mosaicking large raster datasets.

    Parameters
    ----------
    inputfiles : list of str
        List of input GeoTIFF filenames to be merged. All rasters should
        have compatible projections, resolutions, and band structures.

    output_tif : str
        Path to the output mosaic GeoTIFF.

    Returns
    -------
    None

    Raises
    ------
    SystemExit
        If no input files are provided.

    Notes
    -----
    - A temporary VRT file is created with the same basename as the
      output GeoTIFF and a '.vrt' extension.
    - Nearest-neighbor resampling (``resampleAlg='near'``) is used,
      making this function suitable for categorical or classification
      rasters.
    - Output files are written with the following GDAL creation options:

      * ``TILED=YES`` — enables tiled storage for faster access.
      * ``COMPRESS=LZW`` — applies lossless LZW compression.
      * ``BIGTIFF=YES`` — allows output files larger than 4 GB.

    - Input pixels with a value of 0 are treated as NoData and are not
      propagated into the mosaic.

    Examples
    --------
    Merge several GeoTIFF tiles:

    >>> files = [
    ...     "tile_1.tif",
    ...     "tile_2.tif",
    ...     "tile_3.tif"
    ... ]
    >>> merge_big_geotif(files, "mosaic.tif")

"""

import os
import glob
from osgeo import gdal

def merge_big_geotif(inputfiles, output_tif):
    if not files:
        raise SystemExit(f'No TIFF files found in: {input_folder}')

    # Build VRT (in-memory or on-disk)
    vrt_path = os.path.splitext(output_tif)[0] + '.vrt'

    gdal.BuildVRT(vrt_path, files)

    # Warp VRT to final GeoTIFF (streaming)
    # For categorical/class rasters use nearest (or 'mode' if your GDAL build supports it)
    warp_options = gdal.WarpOptions(
        format='GTiff',
        resampleAlg='near',      # use 'mode' if available and you want majority-downsampling
        srcNodata=0,
        dstNodata=0,
        creationOptions=['TILED=YES', 'COMPRESS=LZW', 'BIGTIFF=YES'],
        multithread=True
    )

    gdal.Warp(output_tif, vrt_path, options=warp_options)

    print('Mosaic written to:', output_tif)




if __name__=="__main__":

    outputdir='/mnt/scratch/huangh33/landcovermapping_data/mosaic/DRC/'

    inputdir='/mnt/scratch/huangh33/landcovermapping_data/output/nsamples_894053_median/'
    
    output_tif=outputdir+'drc_'+inputdir.split('/')[-2]+'_median.tif'

    files=glob.glob(inputdir+'Al*tif')

    print(files)
    print(len(files))


    input()





