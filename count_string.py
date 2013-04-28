#!/usr/bin/env python
import sys
import os
import re
import string

def usage():
    print("---------------------------------------------------")
    print('-- usage:: ./count_string.py inputFile "keyword" --')
    print("---------------------------------------------------")

def main():
    if(len(sys.argv)<3):
        usage()
        sys.exit(1)
    fileName = sys.argv[1]
    keyword = sys.argv[2]
    pattern = re.compile(r"\b%s\b"%(keyword))
    num = 0
        
    #open file
    try:
       f = open(fileName, "rU")
    except (IOError) :
        print("can't open the file : %s"%(fileName))
        sys.exit(1)    
    
    for eachline in f:
        num += len(re.findall(pattern, eachline))

    if 0 == num:
        print("Can't find this string :: %s" % (keyword))
    else :
        print("The string number is : %d " % (num))
main()
