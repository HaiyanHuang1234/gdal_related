# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import earthpy.plot as ep
from plot_without_border import plot_without_border
from rasterio.warp import reproject, Resampling, calculate_default_transform
from rasterio.enums import Compression
import os, re, glob, rasterio


def reproj_match(in_file, match_file, out_file,scale_factor=None,resampling=None):

    if scale_factor is None:scale_factor=1

    if resampling is None:resampling=1

    # open input
    with rasterio.open(in_file) as src:
        src_transform = src.transform

        #print(src_transform)
        tags1=src.tags()

        # open input to match
        with rasterio.open(match_file) as match:
            dst_crs = match.crs
            
            # calculate the output transform matrix
            dst_transform, dst_width, dst_height = calculate_default_transform(
                src.crs,     # input CRS
                dst_crs,     # output CRS
                match.width/scale_factor,   # input width
                match.height/scale_factor,  # input height
                *match.bounds,  # unpacks input outer boundaries (left, bottom, right, top)
            )
                    
        # set properties for output
        dst_kwargs = src.meta.copy()
        dst_kwargs.update({"crs": dst_crs,
                           "transform": dst_transform,
                           "width": dst_width,
                           "height": dst_height})

        #print("Coregistered to shape:", dst_height, dst_width,'\n Affine',dst_transform)


        # open output
        with rasterio.open(out_file,
                           "w",
                           **dst_kwargs,
                           compress = Compression.lzw) as dst:
            dst.update_tags(**tags1)

            # iterate through bands and write using reproject function
            #print('src count=', src.count)

            if resampling==1:
                for i in range(1, src.count + 1):
                    reproject(
                        source = rasterio.band(src, i),
                        destination = rasterio.band(dst, i),
                        src_transform = src.transform,
                        src_crs = src.crs,
                        dst_transform = dst_transform,
                        dst_crs = dst_crs,
                        resampling = Resampling.nearest)
            elif resampling==2:
                for i in range(1, src.count + 1):
                    reproject(
                        source = rasterio.band(src, i),
                        destination = rasterio.band(dst, i),
                        src_transform = src.transform,
                        src_crs = src.crs,
                        dst_transform = dst_transform,
                        dst_crs = dst_crs,
                        resampling = Resampling.average)
            elif resampling==3:
                for i in range(1, src.count + 1):
                    reproject(
                        source = rasterio.band(src, i),
                        destination = rasterio.band(dst, i),
                        src_transform = src.transform,
                        src_crs = src.crs,
                        dst_transform = dst_transform,
                        dst_crs = dst_crs,
                        resampling = Resampling.mode)



def change_utm_zone(in_file,target_crs,output_geotiff):
                
    with rasterio.open(in_file) as src:
        transform, width, height = calculate_default_transform(
                        src.crs, target_crs, src.width, src.height, *src.bounds)

        tags1=src.tags()

        kwargs = src.meta.copy()                
        kwargs.update({'crs': target_crs,\
                'transform': transform,\
                'width': width,\
                'height': height
                })

        with rasterio.open(output_geotiff, 'w', **kwargs) as dst:

            dst.update_tags(**tags1)


            for i in range(1, src.count + 1):
                reproject(source=rasterio.band(src, i),\
                        destination=rasterio.band(dst, i),\
                        src_transform=src.transform,\
                        src_crs=src.crs,\
                        dst_transform=transform,\
                        dst_crs=target_crs,\
                        resampling=Resampling.nearest)

        return 0

if __name__=='__main__':

    with rasterio.open(match_file) as f:
        target_crs=f.crs
        print(f.count)

    with rasterio.open(in_file) as f:
        source_crs=f.crs

    output_geotiff='new.tif'
    if source_crs!=target_crs:
        change_utm_zone(in_file,target_crs,output_geotiff)
        out_file='out_file.tif'
        reproj_match(output_geotiff, match_file, out_file)
    else:
        out_file='out_file.tif'
        reproj_match(in_file, match_file, out_file)



