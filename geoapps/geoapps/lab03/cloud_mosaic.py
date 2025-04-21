import typing as t
import geemap
import ee

def cloud_mask(image: ee.Image) -> ee.Image:

    qa60 = image.select("QA60")
    cloud_mask = qa60.bitwiseAnd(1 << 10).eq(0).And(qa60.bitwiseAnd(1 << 11).eq(0))
    
    return image.updateMask(cloud_mask)

def create_cloud_free_mosaic(aoi: ee.Geometry, start_date: t.Union[str, ee.Date], end_date: t.Union[str, ee.Date]) -> geemap.Map:
    
    sentinel2_image = ee.ImageCollection('COPERNICUS/S2_HARMONIZED') \
        .filterBounds(aoi) \
        .filterDate(start_date, end_date)

    cloud_free_image = sentinel2_image.map(cloud_mask).median()

    return cloud_free_image