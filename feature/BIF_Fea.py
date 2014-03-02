#!/usr/bin/env python
#-*-coding:utf-8 -*-

import numpy as NM
from PIL import Image

"""
Please refer to 
"Object Recognition with Features Inspired by Visual Cortex"
"""

def frange(start, stop, step):
     r = start
     if step > 0:
         while r < stop:
             yield r
             r += step
     else:
         while r > stop:
             yield r
             r += step


class BIF_Fea(object):
    def __init__(self):
        self.patchSizes = [2, 4, 6, 8]
        
        ############################################
        ### The more, the better. Making a tradeoff
        ### between time and result. So choose 250  
        self.numPatchesPerSize = 250
        
        #######################################################
        ###             gabor_para
        ###  G(x,y) = exp(-(X^2+γ^2*Y^2)/(2*σ^2))*cos((2π/λ)*X)
        ###  γ(gamma)
        ###  λ(lambda)
        ###  σ(sigma) 
        ###  X= x*cosθ + y*sinθ
        ###  Y=-x*sinθ + y*cosθ
        self.filter_sizes = NM.arange(7, 39, 2)

        self.gabor_thetas = NM.array((0, NM.pi/4, NM.pi/2, NM.pi*3/4))
        self.div = NM.arange(4, 3.2, -0.05)
        self.gabor_lambdas = self.filter_sizes*2 / self.div
        self.gabor_sigmas = self.gabor_lambdas * 0.8
        ###  spatial aspect ratio: 0.23 < gamma < 0.92
        self.gabor_gamma = 0.3 

    def GetGaborFilter(self, filter_size, gabor_theta, gabor_sigma,
                       gabor_lambda, gabor_gamma):

        gabor_filter = NM.empty((filter_size, filter_size),
                                dtype=NM.float64)
        center = int(NM.ceil(filter_size/2.0))
        filter_size_L = center -1
        filter_size_R = filter_size - filter_size_L -1
                
        sigma2 = gabor_sigma * gabor_sigma
        gamma2 = gabor_gamma * gabor_gamma  
        for y in xrange(-filter_size_L, filter_size_R+1, 1): 
            for x in xrange(-filter_size_L, filter_size_R+1, 1): 
                if NM.sqrt(x*x+y*y) > filter_size/2.0:
                    E = 0
                else:
                    X = x*NM.cos(gabor_theta) + y*NM.sin(gabor_theta)
                    Y = y*NM.cos(gabor_theta) - x*NM.sin(gabor_theta)
                    temp1 = NM.exp(-(X*X + gamma2*Y*Y)/(2*sigma2))
                    temp2 = NM.cos((2*NM.pi/gabor_lambda)*X)
                    E = temp1*temp2
                gabor_filter[y+filter_size_L,
                             x+filter_size_L] = E
        return gabor_filter
    

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
        Y_data_f = NM.divide(Y_data, 255.0)
        
        ### test
        gabor_filter = self.GetGaborFilter(7,  NM.pi/2,
                                           self.gabor_sigmas[0],
                                           self.gabor_lambdas[0],
                                           0.3)
        return


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

    Y_data = NM.asarray(srcImg, dtype=NM.uint8)

    fea_extractor = BIF_Fea()
    fea_extractor.extract(Y_data)
    return

if '__main__' == __name__:
    main()
