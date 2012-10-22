#!/home/fshen/Install_samuel/Python/python3.2.3/bin/python3

import sys, os

pyVersion = sys.version[0]
print('python version : %s'%pyVersion)

import re
import getopt

def usage():
    print('./cfind -e "expression" -p path\n')

def IterateFile(basePath, reExp):

    if not os.path.exists(basePath):
        print("The path doesn't exist")
    for fileName in os.listdir(basePath):
        path = basePath + os.sep + fileName
        if os.path.isdir(path):
            IterateFile(path, reExp)
        try :
            f=open(path)
            lineNum = 1
            for line in f:
                if None != re.search(reExp, line):
                    print ('file:%s - line:%d \n   : %s'%(fileName,lineNum ,line))
                lineNum += 1
            f.close()
        except:
            pass

def main():
    expression=sys.argv[1]
    basePath=sys.argv[2]
    reExp = re.compile(expression, flags=0)
    IterateFile(basePath, reExp)

main()

    
    



