from PIL import Image, ImageStat
from pylab import imshow, show, close

# Parameters...
image_file_name = "2614_1178_10cm_example.tif"


def main():
    """Main program"""

    # Open image and assign it to a var.
    img = Image.open(image_file_name)

    # Print image infos.
    print "Format:", img.format, ", Taille:", img.size, ", Mode:", img.mode

    # Get pixel data from image.
    img_data = img.getdata()

    # Creat Stat module instance
    img_stat = ImageStat.Stat(img)
    
    # Print various stats...
    print img_stat.extrema
    print img_stat.count
    print img_stat.mean
    print img_stat.median
    print img_stat.stddev
    
    img_histo = img.histogram()
    
    print img_histo
    
    #imshow(img)
    #show()
    #identified = raw_input('Please press a key')
    #close()
    
if __name__ == '__main__':
    main()