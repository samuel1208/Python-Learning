#!/usr/bin/python
import sys
import os
import re
import string

def usage():
    print("./count_time.py file keyword")

def main():
    if(len(sys.argv)<3):
        usage()
        sys.exit(1)
    fileName = sys.argv[1]
    testPart = sys.argv[2]
    pattern = re.compile(testPart.upper())
    subPattern = re.compile("\d+\.\d*(?=\D*$)")
	
    time = 0
    count = 0
        
    #open file
    try:
       f = open(fileName, "rU")
    except (IOError) :
        print("can't open the file : %s"%(fileName))
        sys.exit(1)    
	#anysis
    for eachline in f :
        m = re.search(pattern, eachline.upper())        
        if(m is not None) :
            subString = re.search(subPattern, eachline)
            if subString is not None : 
                time += string.atof(subString.group())
                count += 1
    if 0 == count :
        print("Can't found the %s's time" % (testPart))
    else :
        print("average time : %d ms" % (time/count))
main()
