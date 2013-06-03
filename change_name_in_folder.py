#!/usr/bin/env python

import sys, os

pyVersion = sys.version[0]
print('python version : %s'%pyVersion)

import getopt


def usage():
    print('-----------------------------------')
    print('[[Usage]]::')
    print('./change_filename_in_folder path --[file_format/-f]=jpg [--prefix/-p]=img, [--beginNum/-b]=0 , [--verbose/-v]')
    print('\n[[para]]::')
    print('\t path             : The path of the file which will be renamed')
    print('\t --file_format/-f : optional Para. Default value is "jpg"')
    print('\t --prefix/-p      : optional Para. Default value is "img"')
    print('\t --beginNum/-b    : optional Para. Default value is 0')
    print('\t --verbose/-v     : only print the paras if set')
    print('-----------------------------------')

def changeName(basePath, file_format, prefix, beginNum):

    num = int(beginNum)
    if not os.path.exists(basePath):
        print("ERRORS:: The path doesn't exist")
        return 
    
    if os.path.isfile(basePath):
        print('ERROR :: Open %s failed'%(basePath))
        return
    else:
        for fileName in os.listdir(basePath):
            if file_format == os.path.splitext(fileName)[1]:
                oldName = "%s/%s"%(basePath, fileName)
                newName = "%s/%s_%07d%s"%(basePath, prefix, num, file_format)
                num = num+1                
                os.rename(oldName, newName)
             
            else:
                continue

    print("Rename  %d files"%(num - int(beginNum)))
           
def main():
    if(len(sys.argv)<2):
        print("The input Para is wrong")
        usage()
        return
    #opts=[]
    try:
        opts, args = getopt.getopt(sys.argv[2:], "f:p:b:v", ["file_format=", "prefix=", "beginNum=", "verbose"])
  
    except getopt.GetoptError:
        print("ERROR:: Errors occur in getting option Paras")
        usage()
        return 

    file_format = 'jpg'
    prefix = "img"
    beginNum = 0
    verbose = 0
    for op, arg in opts:
        if op in ("-f", "--file_format"):
            file_format = ".%s"%(arg)
        elif op in ("-p", "--prefix"):
            prefix = arg
        elif op in ("--beginNum","-b"):
            beginNum = arg
        elif op in ("--verbose","-v"):
            verbose = 1
    
    path = sys.argv[1]        

    if 1 == verbose:
        print(file_format, prefix, beginNum, path)
    else:
        changeName(path, file_format, prefix, beginNum)

        
    print ("Finished")

main()

    
    



