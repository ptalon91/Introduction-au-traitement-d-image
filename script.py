'''Ver 0.2.0'''
from PIL import Image, ImageStat
from pylab import *
from scipy.cluster.vq import *
from scipy.misc import imresize

# Parameters...
image_file_name = "2614_1178_10cm_example.tif"


def main():
    """Main program"""

    # Open image and assign it to a var.
    img = Image.open(image_file_name) #.crop((600, 600, 800, 900))   

    # Print image infos.
    print "Format:", img.format, ", Taille:", img.size, ", Mode:", img.mode

    # Create Stat module instance
    img_stat = ImageStat.Stat(img)
    
    # Print various stats...
    print img_stat.extrema
    print img_stat.count
    print img_stat.mean
    print img_stat.median
    print img_stat.stddev
    
    # The following lines are for image classification using K-means...
    # compute color features for each region
    
    img_array = array(img)
    
    steps = 1000
    dx = img_array.shape[0] / steps
    dy = img_array.shape[1] / steps
    
    features = []
    for x in range(steps):
        for y in range(steps):
            R = mean(img_array[x*dx:(x+1)*dx,y*dy:(y+1)*dy,0])
            G = mean(img_array[x*dx:(x+1)*dx,y*dy:(y+1)*dy,1])
            B = mean(img_array[x*dx:(x+1)*dx,y*dy:(y+1)*dy,2])
            features.append([R,G,B])
    features = array(features,'f') # make into array
    # cluster
    centroids,variance = kmeans(features,6)
    code,distance = vq(features,centroids)
    # create image with cluster labels
    codeim = code.reshape(steps,steps)
    codeim = imresize(codeim,img_array.shape[:2],interp='nearest')
    
    figure()
    imshow(codeim)
    show()

    
    # Convert image in grey shades.
    # img_grey = img.convert("L")
    
    # img_data = list(img_grey.getdata())
    
    # Flatten list of pixel values (not a list of lists anymore)...
    # flatten_img_grey = [y for x in img_grey for y in x]
    
    # Create histogram and show it.
    # figure()
    # hist(flatten_img_grey, 255)
    #show()
    
    #show()
    #identified = raw_input('Please press a key')
    #close()
    
if __name__ == '__main__':
    main()