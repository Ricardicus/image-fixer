import math
import random
import sys
import imageio
import numpy
import traceback
import argparse
from progress.bar import Bar

class ImageHandler:

    def rescaleImage(self, image_path, out_path, scale):
        im = imageio.v2.imread(image_path)
        dimensions = im.shape
        
        if scale < 0:
            scale = -scale
            outndarray = numpy.zeros((int(dimensions[0]/scale), int(dimensions[1]/scale), dimensions[2]),dtype=numpy.uint8)
            outdim = outndarray.shape
            bar = Bar('Processing...', max=(outdim[0]*outdim[1]))
            print("{}x{} => {}x{}".format(dimensions[0], dimensions[1], outdim[0], outdim[1]))
            for x in range(outdim[0]):
                for y in range(outdim[1]):
                    for z in range(outdim[2]):
                        outndarray[x][y][z] = im[x*scale][y*scale][z]
                    bar.next()
            bar.finish()
            imageio.v2.imwrite(out_path, outndarray)
            return

        if scale > 1:
            outndarray = numpy.zeros((int(dimensions[0]*scale), int(dimensions[1]*scale), dimensions[2]),dtype=numpy.uint8)
            outdim = outndarray.shape

            bar = Bar('Processing...', max=(outdim[0]*outdim[1]))
            print("{}x{} => {}x{}".format(dimensions[0], dimensions[1], outdim[0], outdim[1]))
            for x in range(dimensions[0]):
                for y in range(dimensions[1]):
                    for xx in range(scale):
                        for yy in range(scale):
                            for z in range(outdim[2]):
                                outndarray[x*scale + xx][y*scale + yy][z] = im[x][y][z]
                            bar.next()
            bar.finish()
            imageio.v2.imwrite(out_path, outndarray)
        
        return
    def cropImage(self, image_path, out_path, cropleft, cropright, cropup, cropdown):
        im = imageio.v2.imread(image_path)
        dimensions = im.shape
        outndarray = numpy.zeros((dimensions[0]-cropup-cropdown, dimensions[1]-cropright-cropleft, dimensions[2]),dtype=numpy.uint8)
        outdim = outndarray.shape
        
        bar = Bar('Processing...', max=(outdim[0]*outdim[1]))
        print("{}x{} => {}x{}".format(dimensions[0], dimensions[1], outdim[0], outdim[1]))
        for x in range(outdim[0]):
            for y in range(outdim[1]):
                for z in range(outdim[2]):
                    outndarray[x][y][z] = im[x+cropup][y+cropright][z]
                bar.next()
        bar.finish()
        imageio.v2.imwrite(out_path, outndarray)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate pixelimages')

    parser.add_argument('-o','--output', help='Output file (.png)',
            type=str, default='out.png')
    parser.add_argument('-i','--input', help='Input image, see the "samples" folder',
            default='samples/Flowers.png', type=str)
    parser.add_argument('--downscale', help='Image down scaling',
            default=1, type=int)
    parser.add_argument('--upscale', help='Image up scaling',
            default=1, type=int)
    parser.add_argument('--keepup', help='Mirror upper parts of the image with the original', action='store_true')
    parser.add_argument('--keepdown', help='Mirror lower parts of the image with the original', action='store_true')
    parser.add_argument('--compress', help='Compress content of input image', action='store_true')
    parser.add_argument('--cropleft', help="crop right (pixels)", type=int, default=0)
    parser.add_argument('--cropright', help="crop left (pixels)", type=int, default=0)
    parser.add_argument('--cropup', help="crop up (pixels)", type=int, default=0)
    parser.add_argument('--cropdown', help="crop down (pixels)", type=int, default=0)

    args = parser.parse_args()
    outputFile = args.output
    inputFile = args.input
    downScale = args.downscale
    upScale = args.upscale
    keepup = args.keepup
    keepdown = args.keepdown
    compress = args.compress
    cropleft = args.cropleft
    cropright = args.cropright
    cropup = args.cropup
    cropdown = args.cropdown
    
    ih = ImageHandler()

    if downScale > 1:
        print("Downscaling {} => {} ...".format(inputFile, outputFile))
        ih.rescaleImage(inputFile, outputFile, -downScale)
        print("Done!")
    if upScale > 1:
        print("Upscaling {} => {} ...".format(inputFile, outputFile))
        ih.rescaleImage(inputFile, outputFile, upScale)
        print("Done!")

    if cropleft or cropright or cropup or cropdown:
        print("Cropping {} => {} ...".format(inputFile, outputFile))
        ih.cropImage(inputFile, outputFile, cropleft, cropright, cropup, cropdown)
        print("Cropped!")
        sys.exit(0)

    
