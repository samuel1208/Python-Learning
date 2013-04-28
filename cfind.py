#!/usr/bin/env python

#todo. skip temp file begin with 
#skip big file
# add some option


import sys, os

pyVersion = sys.version[0]
print('python version : %s'%pyVersion)

import re
import getopt

rehide = re.compile("^\..*", flags=0)

def usage():
    print('./cfind -e "expression" -p path\n')

def IterateFile(basePath, reExp):

    if not os.path.exists(basePath):
        print("The path doesn't exist")
    for fileName in os.listdir(basePath):
        path = basePath + os.sep + fileName
        if len(re.findall(rehide,fileName)) > 0:
            continue
        if os.path.isdir(path) :
            IterateFile(path, reExp)
        try :
            f=open(path)
            lineNum = 1
            for line in f:
                if None != re.search(reExp, line.lower()):
                    print ('file:%s - line:%d \n   : %s'%(path,lineNum ,line))
                lineNum += 1
            f.close()
        except:
            pass

def main():
    expression=sys.argv[1].lower()
    basePath=sys.argv[2]
    reExp = re.compile(expression, flags=0)
    IterateFile(basePath, reExp)
    print ("Finished")

main()

    
    



