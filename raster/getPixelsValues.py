import sys, gc
from osgeo import gdal, ogr, osr

sys.path.append(".") # Set path to the roots

from function.ogrFunction import orgDatasets
from function.gdalFunction import gdalDatasets

class getPixelsValues:
    __slots__ = [
        "layerPath", "layerName", "layerRef",
        "rasterPath", "projection", "geotrans", "ref",
        "orgDatasets", "gdalDatasets"
    ]
    
    def __init__(self, rasterPath: str | None = None, layer: str | tuple[str, str] | None = None):
        """
        Initialize the class.
        """
        gdal.UseExceptions()
        gdal.SetConfigOption("GDAL_NUM_THREADS", "ALL_CPUS")
        self.rasterPath: str | None = None
        self.layerName: str | None = None
        self.orgDatasets = orgDatasets
        self.gdalDatasets = gdalDatasets

        if rasterPath is not None:
            self.updateRasterInfo(rasterPath)
        if layer is not None:
            self.updateLayerInfo(layer)


    def updateLayerInfo(self, layer: str | tuple[str, str]) -> None:
        layerDs = False
        try:
            if type(layer) is str:
                self.layerPath = layer
                with self.orgDatasets(self.layerPath, close=False) as layerDs:
                    layer = layerDs.GetLayer(0)
                    if not isinstance(layer, ogr.Layer):
                        raise RuntimeError("Failed to get layer from layer dataset.")
                    self.layerName = layer.GetName()
            else:
                self.layerPath, layerName = layer
                with self.orgDatasets(self.layerPath, close=False) as layerDs:
                    layer = layerDs.GetLayerByName(layerName)
                    if not isinstance(layer, ogr.Layer):
                        raise RuntimeError("Failed to get layer \'{}\' from layer dataset.".format(layerName))
                    self.layerName = layerName
            
            self.layerRef = layer.GetSpatialRef()
            if not isinstance(self.layerRef, osr.SpatialReference):
                raise RuntimeError("Failed to get spatial reference from layer dataset.")
        
        except:
            raise RuntimeError
        finally:
            if layerDs:
                layerDs.Destroy()
            gc.collect()  # Force garbage collection

        return
    
    def updateRasterInfo(self, rasterPath: str) -> None:
        self.rasterPath = rasterPath
        with self.gdalDatasets(rasterPath) as rasterDs:
            self.projection = rasterDs.GetProjection()
            self.geotrans = rasterDs.GetGeoTransform()
            self.ref = rasterDs.GetSpatialRef()

        return

# Debugging and testing
if __name__ == "__main__":
    a = getPixelsValues("C:\\0_PolyU\\flooding\\SumDays.tif")