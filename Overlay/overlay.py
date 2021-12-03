#Chea, Cohen, Gao, Hiciano
#CS5800 Spring 2021 Final Project
#Program that outputs best pattern match ratio from matches of an image against images in a directory. 

#pillow aids in Image reading and manipulation 
from PIL import Image, ImageOps
#os to access and work with any user's directory of images
import os

def overlayMatch(newImage, ogImage):
    '''
    Takes in two images and calculates their 'match' percentage. A nested for loop is used to 
    iterate through the x,y coordinates of both equally sized images and compare RGB values.
    '''
    #Open and load the image, convert to grayschool 
    img = Image.open(newImage)
    imgGs = ImageOps.grayscale(img)

    img2 = Image.open(ogImage)
    img2Gs = ImageOps.grayscale(img2)

    print("Comparing " + str(newImage) + " with " + str(ogImage) )

    #Get image type (ie. jpeg, ppm...) and dimenstions
    print(img.format)
    print(img.mode)
    print(img.size)

    #use dimensions of image to determine number of iterations to scan pixels below
    w, h = img.size

    #get pixel format of image (ie. RGB, CMYK)
    print(img.mode)

    totalPixels = 0
    matches = 0

    #traverse row, column of image to access each pixel
    for ycoord in range(h):
        for xcoord in range(w):
            #using x,y tuple, getpixel() returns current pixel's coordinate as a single int value for single band images
            # (x,y) tuple point for multibanded images
            
            val = imgGs.getpixel((xcoord, ycoord)) # new image pixel value
            val2 = img2Gs.getpixel((xcoord, ycoord)) #og image pixel value

            totalPixels += 1 #tracking total pixels assessed
            #if pixel values of both image's are equal at current position, we have found a pattern match
            if val == val2:
                matches += 1

    #in a perfact match (identical images) the number of total pixels across an image is equal to the number of matches
    #print(totalPixels)
    #print(matches)

    #return the percentage of matched pixels between the two images
    return (matches/totalPixels)


def checkImageLibrary(newImage, libraryPath):    
    '''
    Given an image (newImage) and a directory of images (libraryPath): computes the overlay match between the 
    newImage and each image in libraryPath directory and returns the closest match found. 
    '''
    print(libraryPath)
    if os.name == "nt":
        print("nt")
        libraryPath = os.path.join(libraryPath + os.sep, "img")
    else:
        print("not nt")
        libraryPath = os.path.join(libraryPath + os.sep, "img")

    #print(libraryPath) #confirm path

    #intialize list to store the images newImage will be compared against
    libraryImages = []

    #searches img directory for ppm files to store in libraryImages
    for filename in os.listdir(libraryPath):
        print(filename)
        #account for uppercase/lowercase extensions
        if filename.endswith(".ppm") or filename.endswith(".PPM"):
            libraryImages.append(filename)

    #libraryImages = [img for img in directory]
    print(libraryImages) #confirm expected list of images


    # determine overlaymatch ratio of newImage to each image in list and store outputs in new ratios list
    overlayRatios = []
    for image in libraryImages:
        ogImage = os.path.join(libraryPath + os.sep, image)
        # pattern match newImage to current one at iteration, push comparison value to array
        ratio = overlayMatch(newImage, ogImage)
        overlayRatios.append(ratio)
    
    #determine best overall ratio by cross referencing list and maintaining best ratio at each check
    bestRatio = 0
    bestIndex = 0
    for i, ratio in enumerate(overlayRatios):
        if ratio > bestRatio:
            bestRatio = ratio
            bestIndex = i
    
    closestMatch = (libraryImages[bestIndex],bestRatio)

    return closestMatch

#driver code
def main():
    #program expects an img folder in current directory of this program
    filepath = os.getcwd()

    #account for different operating systems' path syntax
    if os.name == "nt":
        print("nt")
        newImage = os.path.join(filepath + os.sep, "img\LightWhale.ppm")
    else:
        print("not nt")
        newImage = os.path.join(filepath + os.sep, "img/LightWhale.ppm")

    print(newImage)    
    closestMatch = checkImageLibrary(newImage, filepath)
    print(closestMatch)

#protect top level code and allows for this program to be called by other programs if needed
if __name__ == "__main__":
    main()
