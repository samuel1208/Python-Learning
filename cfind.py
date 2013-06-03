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
    print('-----------------------------------')
    print('./cfind  "expression"  [path]/[or a file] -p')
    print('-p  :  print the content in the file when search in path mode')
    print('-----------------------------------')

def IterateFile(basePath, reExp, isPrint):

    if not os.path.exists(basePath):
        print("The path doesn't exist")
        return
    
    if os.path.isfile(basePath):
        try :
            f=open(basePath)
            lineNum = 1
            for line in f:
                if None != re.search(reExp, line.lower()):
                    print ('file:%s - line:%d \n   : %s'%(basePath,lineNum ,line))
                lineNum += 1
            f.close()
        except:
            print('ERROR :: Open %s failed'%(basePath))
            return
    else:
        for fileName in os.listdir(basePath):
            path = basePath + os.sep + fileName
            if len(re.findall(rehide,fileName)) > 0:
                continue
            if os.path.isdir(path) :
                IterateFile(path, reExp, isPrint)
            try :
                f=open(path)
                isFound = False
                lineNum = 1
                for line in f:
                    if None != re.search(reExp, line.lower()):
                        if isPrint:
                            print ('file:%s - line:%d \n   : %s'%(path,lineNum ,line))
                        else:
                            isFound = True
                            break
                    lineNum += 1
                if isFound and  False==isPrint:
                    print('file : %s '%(path))

                f.close()
            except:
                pass

def main():
    if(len(sys.argv)<3):
        print("The input Para is wrong")
        usage()
        return
    expression=sys.argv[1].lower()
    basePath=sys.argv[2]
    if(len(sys.argv)==4):
        isPrint = sys.argv[3] == "-p"
    else:
        isPrint = False
    reExp = re.compile(expression, flags=0)
    IterateFile(basePath, reExp, isPrint)
    print ("Finished")

main()

    
    



