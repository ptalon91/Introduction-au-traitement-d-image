import numpy as np
import os
from osgeo import gdal
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from matplotlib import pyplot as plt

# Parameters...
raster_data_path = "data/image/2298119ene2016recorteTT.tif"
output_file_name = "classification.tiff"
train_data_path = "data/train/"
validation_data_path = "data/test/"

# A list of "random" colors (for a nicer output)
COLORS = ["#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941"]

def main():
    '''Main program'''
    
    # Extract the geographic info and transform the band’s data into an array...
    raster_dataset = gdal.Open(raster_data_path, gdal.GA_ReadOnly)
    geo_transform = raster_dataset.GetGeoTransform()
    proj = raster_dataset.GetProjectionRef()
        
    # Create new dictionnary.
    bands_data = list()
    
    # Loop
    for b in range(1, raster_dataset.RasterCount+1):
        band = raster_dataset.GetRasterBand(b)
        bands_data.append(band.ReadAsArray())        
    
    bands_data = np.dstack(bands_data)
    rows, cols, n_bands = bands_data.shape

    # Training data processing
    files = [file for file in os.listdir(train_data_path)
             if file.endswith('.shp')]
    classes = [file.split('.')[0] for file in files]
    shapefiles = [os.path.join(train_data_path, file)
                  for file in files if file.endswith('.shp')]

    labeled_pixels = vectors_to_raster(shapefiles, rows, cols, geo_transform,
                                       proj)
    is_train = np.nonzero(labeled_pixels)
    training_labels = labeled_pixels[is_train]
    training_samples = bands_data[is_train]
    
    classifier = RandomForestClassifier(n_jobs=-1)
    classifier.fit(training_samples, training_labels)

    n_samples = rows*cols
    flat_pixels = bands_data.reshape((n_samples, n_bands))
    result = classifier.predict(flat_pixels)
    classification = result.reshape((rows, cols))
    
    f = plt.figure()
    f.add_subplot(1, 2, 2)
    r = bands_data[:,:,3]
    g = bands_data[:,:,2]
    b = bands_data[:,:,1]
    rgb = np.dstack([r,g,b])
    f.add_subplot(1, 2, 1)
    plt.imshow(rgb/255)
    f.add_subplot(1, 2, 2)
    plt.imshow(classification)
    
    plt.imsave("filename.png", classification, format = "png")
    
    write_geotiff(output_file_name, classification, geo_transform, proj)

def create_mask_from_vector(vector_data_path, cols, rows, geo_transform,
                            projection, target_value=1):
    """Rasterize the given vector (wrapper for gdal.RasterizeLayer)."""
    data_source = gdal.OpenEx(vector_data_path, gdal.OF_VECTOR)
    layer = data_source.GetLayer(0)
    driver = gdal.GetDriverByName('MEM')  # In memory dataset
    target_ds = driver.Create('', cols, rows, 1, gdal.GDT_UInt16)
    target_ds.SetGeoTransform(geo_transform)
    target_ds.SetProjection(projection)
    gdal.RasterizeLayer(target_ds, [1], layer, burn_values=[target_value])
    return target_ds


def vectors_to_raster(file_paths, rows, cols, geo_transform, projection):
    """Rasterize the vectors in the given directory in a single image."""
    labeled_pixels = np.zeros((rows, cols))
    for i, path in enumerate(file_paths):
        label = i+1
        ds = create_mask_from_vector(path, cols, rows, geo_transform,
                                     projection, target_value=label)
        band = ds.GetRasterBand(1)
        labeled_pixels += band.ReadAsArray()
        ds = None
    return labeled_pixels


def write_geotiff(fname, data, geo_transform, projection):
    """Create a GeoTIFF file with the given data."""
    driver = gdal.GetDriverByName('GTiff')
    rows, cols = data.shape
    dataset = driver.Create(fname, cols, rows, 1, gdal.GDT_Byte)
    dataset.SetGeoTransform(geo_transform)
    dataset.SetProjection(projection)
    band = dataset.GetRasterBand(1)
    band.WriteArray(data)
    dataset = None  # Close the file
    
if __name__ == '__main__':
    main()