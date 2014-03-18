#!/usr/bin/env python
import numpy 
from PIL import ImageFilter, Image

class HistEqualize(object):
    """
    Equalize the illumination of the image. 
    """
    
    @staticmethod
    def hist_equalize():
        pass


    @staticmethod
    def histeq(im,nbr_bins=256):
        #get image histogram
        imhist,bins = numpy.histogram(im.flatten(),nbr_bins,normed=True)
        cdf = imhist.cumsum() #cumulative distribution function
        cdf = 255 * cdf / cdf[-1] #normalize
        
        #use linear interpolation of cdf to find new pixel values
        im2 = numpy.interp(im.flatten(),bins[:-1],cdf).astype(numpy.uint8)

        return im2.reshape(im.shape), cdf

    @staticmethod
    def hist_equalize_numpy(gray_arr):
        im,cdf = HistEqualize.histeq(gray_arr)
        return im

        
def main():
    ########################################################################
    import os
    import sys
    import getopt
    def usage():
        print("-----------------------------------------------")
        print('-- usage:: {0}  [Options] image'.format(sys.argv[0]))
        print("-- Options :")
        print("--\ts|show   : Show the src and res image ")
        print("--\th|help   : print help informations")
        
    ########################################################################

    try:
        options, args = getopt.getopt(sys.argv[1:], "hs", ["help", "show"])
    except getopt.GetoptError:  
        usage()
        sys.exit(1)

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
        
    bIsHelp = False
    bIsShow = False
    
    for opt , arg in options:
        if opt in ('-h', '--help'):
            bIsHelp = True;
        if opt in ('-s', '--show'):
            bIsShow = True

    if bIsHelp:
        usage()
        sys.exit(1)
    
    imgPath = args[0]
    if not os.path.exists(imgPath):
        print("ERROR:: The input image isn't exist")
        sys.exit(1)
    
    savePath = "%s_res.bmp"%imgPath
    #process
    srcImg = Image.open(imgPath)
    if 'RGBA' == srcImg.mode or 'RGB' == srcImg.mode:
        srcImg = srcImg.convert('L') 

    if bIsShow: 
        srcImg.show(title='src')

    dstImg = HistEqualize.hist_equalize_numpy(numpy.asarray(srcImg))
    dstImg = Image.fromarray(dstImg)
        
    if bIsShow: 
        dstImg.show(title='dst')
        
    dstImg.save(savePath)
    return 

if '__main__' == __name__:
    main()

    
    
