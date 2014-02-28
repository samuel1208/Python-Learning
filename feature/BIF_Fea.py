#!/usr/bin/env python
import numpy 
from PIL import Image


class BIF_Fea(object):
    def __init__(self):
        self.patchSizes = [2, 4, 6, 8]
        
        ############################################
        ### The more, the better. Making a tradeoff
        ### between time and result. So choose 250  
        self.numPatchesPerSize = 250
        
    def s1(self):
        pass

    def c1(self):
        pass

    def s2(self):
        pass

    def c2(self):
        pass

    def extract(self, Y_data):
        """
        gray_data must be 2-D [wxh] array
        """
        (height, width) = Y_data.shape

        #First normalize into [0-1]
        Y_data_f = numpy.divide(Y_data, 255.0)
        pass
    



def main():
    ########################################################################
    import os
    import sys
    import getopt
    def usage():
        print("-----------------------------------------------")
        print('-- usage:: {0}  [Options] image'.format(sys.argv[0]))
        print("-- Options :")
        #print("--\tm|mode : ")
    ########################################################################

    try:
        options, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError:  
        usage()
        sys.exit(1)

    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
        
    bIsHelp = False
    
    for opt , arg in options:
        if opt in ('-h', '--help'):
            bIsHelp = True;
   
    if bIsHelp:
        usage()
        sys.exit(1)
        
    imgPath = args[0]
    if not os.path.exists(imgPath):
        print("ERROR:: The input image isn't exist")
        sys.exit(1)   
    
    #process
    srcImg = Image.open(imgPath)
    if 'RGBA' == srcImg.mode or 'RGB' == srcImg.mode:
        srcImg = srcImg.convert('L') 
    srcImg.show(title='src')

    Y_data = numpy.asarray(srcImg, dtype=numpy.uint8)

    fea_extractor = BIF_Fea()
    fea_extractor.extract(Y_data)
    return

if '__main__' == __name__:
    main()
