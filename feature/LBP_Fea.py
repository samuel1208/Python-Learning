#!/usr/bin/env python
#-*-coding:utf-8 -*-

import numpy as NM
from scipy.ndimage import filters as scipy_f
from scipy.ndimage import morphology as scipy_morp
from PIL import Image


class LBP_Fea(object):
    def __init__(self, radius, neighbor, mode = "NONE"):
        self.radius = radius
        self.neighbor = neighbor
        self.mode = mode 
        self.supported_modes =["NONE","ROI_U2", "U2"]

        if self.mode.upper() not in self.supported_modes:
            raise Exception("ERROR:: Don't support this mode")
        if self.radius < 1:
            raise Exception("ERROR:: radius must > 0")
        if  self.neighbor < 8:
            raise Exception("ERROR:: radius must be equal to 8 or 16")
                    
    def gen_lookup_table(self):
        neighbor = self.neighbor
        mode = self.mode

        lbp_table_len = (1<<neighbor)
        lbp_table = NM.empty(lbp_table_len, dtype=NM.int)
        
        if "NONE" == mode.upper():
            for i in xrange(0, lbp_table_len):
                lbp_table[i] = i
            return lbp_table
        
        ### init with -1
        lbp_table[:] = -1
        ### set the 0 with 0
        label = 0
        lbp_table[0] = label
        label +=1        

        for one_num in xrange(1,neighbor+1):
            ### get the value first
            val = 0
            for i in xrange(one_num):
                val = val << 1 ;
                val += 1;
            
            lbp_table[val] = label
            label += 1
            
            if one_num == neighbor:
                continue

            ### make a circle move
            for i in xrange(1, neighbor):
                val_base = (1<<neighbor)-1
                ### get the circle move value
                highestBit = val >> (neighbor-1);
                val = val<<1;
                val = (val & val_base) + highestBit;
                lbp_table[val] = label
                if "U2" == mode.upper():
                    label = label+1
                elif "ROI_U2" == mode.upper():
                    pass
            
        mask = (lbp_table == -1)
        lbp_table[mask] = label
        return lbp_table

    
    def extractLBPImg(self, grayArr):
        """
        grayArr must be a 2-D NM.arrry
        """
        if 8==self.neighbor and 1==self.radius:
            return self.extractLBPImg_8_1(grayArr)        
        
        lbp_lookup_table = self.gen_lookup_table()
        height, width = grayArr.shape
        lbpImg = NM.empty((height, width), dtype=NM.int8)
        neighbor = self.neighbor
        
        for i in xrange(0, self.radius):
            lbpImg[:, i] = 0
            lbpImg[:, width-(i+1)] = 0
            lbpImg[i, :] = 0
            lbpImg[height-(i+1), :] = 0

        #### one by one
        offset = NM.empty((neighbor, 2), dtype=NM.float64)
        for n in xrange(0, neighbor):            
            offset[n,0]=float(-self.radius*NM.sin(2.0*NM.pi*n/(float)(neighbor)))
            offset[n,1]=float(self.radius*NM.cos(2.0*NM.pi*n/(float)(neighbor)))

        for h in xrange(self.radius, height-self.radius):
            for w in xrange(self.radius, width-self.radius):
                val_c = grayArr[h,w]
                val_lbp = 0
                for n in xrange(0, neighbor):            
                    x = offset[n,0]+w
                    y = offset[n,1]+h
                    x1  = int(x)
                    y1 =  int(y)
                    x2 = min(x1+1, width-1)
                    y2 = min(y1+1, height-1)
                    fc_x = x-x1
                    fc_y = y-y1
                    v1 = grayArr[y1, x1]
                    v2 = grayArr[y1, x2]
                    v3 = grayArr[y2, x1]
                    v4 = grayArr[y2, x2]
                    val_h1 = (1-fc_x)*v1 + fc_x*v2
                    val_h2 = (1-fc_x)*v3 + fc_x*v4
                    val_f = (1-fc_y)*val_h1 + fc_y*val_h2
                    if val_f>val_c or NM.fabs(val_f-val_c)<0.0000001:
                        val_lbp += 1<<n;
                lbpImg[h,w] = lbp_lookup_table[val_lbp]     

        return lbpImg

    def extractLBPImg_8_1(self, grayArr):
        """
        grayArr must be a 2-D NM.arrry
        """
        lbp_lookup_table = self.gen_lookup_table()
        height, width = grayArr.shape
        lbpImg = NM.empty((height, width), dtype=NM.int8)
        neighbor = self.neighbor
        
        lbpImg[:, 1] = 0
        lbpImg[:, width-1] = 0
        lbpImg[1, :] = 0
        lbpImg[height-1, :] = 0

        #### one by one
        for h in xrange(1, height-1):
            for w in xrange(1, width-1):
                val_c = grayArr[h,w]
                val_lbp = 0

                val = grayArr[h-1, w-1]
                if val>=val_c:
                    val_lbp += 1;
                val = grayArr[h-1, w]
                if val>=val_c:
                    val_lbp += 2;
                val = grayArr[h-1, w+1]
                if val>=val_c:
                    val_lbp += 4;
                val = grayArr[h, w+1]
                if val>=val_c:
                    val_lbp += 8;                    
                val = grayArr[h+1, w+1]
                if val>=val_c:
                    val_lbp += 16;
                val = grayArr[h+1, w]
                if val>=val_c:
                    val_lbp += 32;
                val = grayArr[h+1, w-1]
                if val>=val_c:
                    val_lbp += 64;
                val = grayArr[h, w-1]
                if val>=val_c:
                    val_lbp += 128;

                lbpImg[h,w] = lbp_lookup_table[val_lbp]     
        return lbpImg

def main():
    ########################################################################
    import os
    import sys
    import getopt
    def usage():
        print("-----------------------------------------------")
        print('usage:: {0}  [Paras] image_path'.format(sys.argv[0]))
        print("Paras::")
        print("\t--radius|-r  :  radius of the neighbor")
        print("\t--neighbor|-n:  neighbor number")
        print("\t--mode|-m    :  [none, roi_u2, u2]. Default is u2")
        print("\t--show|-s    :  If need to show the temporary result")
        print("\t--help|-h    :  print the help info")
    ########################################################################

    try:
        options, args = getopt.getopt(sys.argv[1:], "hr:n:m:s", 
                                      ["help", "radius=", 
                                       "neighbor=", "mode=", "show"])
    except getopt.GetoptError:  
        usage()
        sys.exit(1)

    if len(sys.argv) < 2:
        usage()
        return
        
    bIsHelp = False
    bIsShow = False
    radius = None
    neighbor = None
    mode = "NONE"
    
    for opt , arg in options:
        if opt in ('-r', '--radius'):
            radius = int(arg)
        elif opt in ('-n', '--neighbor'):
            neighbor = int(arg)
        elif opt in ('-m', '--mode'):
            mode = arg
        elif opt in ('-s', '--show'):
            bIsShow = True;
        elif opt in ('-h', '--help'):
            bIsHelp = True;
   
    if bIsHelp:
        usage()
        return
        
    imgPath = args[0]
    if not os.path.exists(imgPath):
        print("ERROR:: The input image isn't exist")
        return
    
    #process
    try:
        srcImg = Image.open(imgPath)
        if 'RGBA' == srcImg.mode or 'RGB' == srcImg.mode:
            srcImg = srcImg.convert('L') 
    except:
        print("ERROR::Open %s Failed"%(imgPath))
        return 
    
    if bIsShow:
        srcImg.show(title='src')

    Y_data = NM.asarray(srcImg, dtype=NM.uint8)

    LBPExtractor =  LBP_Fea(radius, neighbor, mode)
    lbpArr = LBPExtractor.extractLBPImg(Y_data)

    if 'NONE'==mode and neighbor>8:
        fractor = 1<<neighbor - 1
        lbpArr = (lbpArr/fractor).astype(NM.uint8)

    lbpImg = Image.fromarray(lbpArr, 'L')
    if bIsShow:
        # max_v = LBPExtractor.gen_lookup_table()[-1]
        # temp_img = Image.fromarray((lbpArr*255.0/max_v).astype(NM.uint8),"L")
        # temp_img.show(title='res')
        lbpImg.show(title='res')

    lbpImg = Image.fromarray(lbpArr, 'L')
    fileName = os.path.splitext(imgPath)[0]
    lbpImg.save("%s_lbp.bmp"%fileName)
    
    
    del Y_data
    del lbpArr
    return

if '__main__' == __name__:
    main()
