#!/usr/bin/env python
import numpy 
from PIL import ImageFilter, Image

class Img_Normalize(object):
    """
    Normalize the illumination of the image. 
    """
    
    @staticmethod    
    def normalize_with_std(gray_arr):
        std = numpy.std(gray_arr)
        mean = numpy.mean(gray_arr)
        res = ((gray_arr-mean)/std)

        ##arrange to [0-255]
        maxV = numpy.max(res)
        minV = numpy.min(res)
        res = ((res-minV)*255 / (maxV-minV)).astype(numpy.uint8)
        
        return res

        
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
    
    savePath = "%s_res.bmp"%(os.path.splitext(imgPath)[0])
    #process
    srcImg = Image.open(imgPath)
    if 'RGBA' == srcImg.mode or 'RGB' == srcImg.mode:
        srcImg = srcImg.convert('L') 

    if bIsShow: 
        srcImg.show(title='src')

    dstImg = Img_Normalize.normalize_with_std(numpy.asarray(srcImg))
    dstImg = Image.fromarray(dstImg)
        
    if bIsShow: 
        dstImg.show(title='dst')
        
    dstImg.save(savePath)
    return 

if '__main__' == __name__:
    main()

    
    
