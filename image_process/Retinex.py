#!/usr/bin/env python
import numpy 
from PIL import ImageFilter, Image

class Retinex(object):
    """
    Equalize the illumination of the image. 
    """
    
    @staticmethod
    def normalize(imgArray, mode=1):
        '''
        Function:
            Adjusting the dynamic range of the grayimg to the interval 
        [0,255] when mode=1 or [0,1] when mode=0
    '''
        minV = numpy.min(imgArray)
        maxV = numpy.max(imgArray)
        step = (maxV-minV)*1.0
        
        if 1==mode:
            return numpy.ceil((imgArray-minV)/step*255)
        elif 0==mode:
            return (imgArray-minV)/step
        else :
            print("ERROR::Please provide either 0 or 1 to Para 'mode'.")
    
            
    @staticmethod
    def hist_truncate(img, lHistCut, uHistCut):

        if uHistCut<=0 or uHistCut>=1 or lHistCut<=0 or lHistCut>=1 :
            print("WARNNING:: lHistCut ans uHistCut show in (0,1)")
            return 
        
        sortV = numpy.sort(img, axis=None)
        length = sortV.size
        # get the low value and up value
        index_f = length * lHistCut
        index_i = int(index_f)
        factor = index_f-index_i
        lV = sortV[index_i]*(1-factor) + sortV[index_i+1]*factor

        index_f = (length-1) * (1-uHistCut)
        index_i = int(index_f)
        factor = index_f-index_i
        uV = sortV[index_i]*(1-factor) + sortV[index_i+1]*factor

        # truncate the value
        mask = img < lV
        img[mask] = lV
        mask = img>uV
        img[mask] = uV
    
    
    @staticmethod
    def single_scale_retinex(grayImg, hsize=30):
        '''
        Notes:
            1.The input Image must be a gray image
        '''
        if 'L' != grayImg.mode:
            print("The input image must be a gray image")
            return None            
        
        originImg = numpy.asarray(grayImg)+0.01
        blurImg = numpy.asarray(grayImg.filter(ImageFilter.GaussianBlur(hsize)))
        blurImg = blurImg + 0.01

        dst = numpy.log(originImg/blurImg)
        Retinex.hist_truncate(dst, 0.002, 0.002)
        return Retinex.normalize(dst,1).astype(numpy.uint8)
        


def main():
    ########################################################################
    import os
    import sys
    import getopt
    def usage():
        print("-----------------------------------------------")
        print('-- usage:: {0}  [Options] image'.format(sys.argv[0]))
        print("-- Options :")
        print("--\tm|mode   : Choose the method to process, default is 'ssr'")
        print("--\ts|show   : Show the src and res image ")
        print("--\th|help   : Choose the method to process, default is 'ssr'")
        
    ########################################################################

    try:
        options, args = getopt.getopt(sys.argv[1:], "hm:s", ["help","mode=", "show"])
    except getopt.GetoptError:  
        usage()
        sys.exit(1)

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
        
    supportMode=['SSR']
    bIsHelp = False
    bIsShow = False
    mode = 'SSR'
    
    for opt , arg in options:
        if opt in ('-h', '--help'):
            bIsHelp = True;
        if opt in ('-m', '--mode'):
            mode = arg.upper()
        if opt in ('-s', '--show'):
            bIsShow = True

    if bIsHelp:
        usage()
        sys.exit(1)
    
    if not mode in supportMode:
        print("ERROR:: Invalid process mode")
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

    if 'SSR' == mode:
        dstImg = Retinex.single_scale_retinex(srcImg,50)
        dstImg = Image.fromarray(dstImg)
        
    if bIsShow: 
        dstImg.show(title='dst')
        
    dstImg.save(savePath)
    return 

if '__main__' == __name__:
    main()

    
    
