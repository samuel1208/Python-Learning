#!/usr/bin/env python

import sys, os

pyVersion = sys.version.split()[0]
print('----------------------------------------------------------------')
print('Python Version : %s'%pyVersion)
print('----------------------------------------------------------------')

import getopt

def getBit(num):
    bitNum=1
    while num//10 != 0:
        bitNum = bitNum+1
        num = num//10
    return bitNum

def usage():
    print('----------------------------------------------------------------')
    print('[[Usage]]::')
    print('./change_filename_in_folder [Paras] File_Path')
    print('\n[[para]]::')
    print('\t --file_format/-f : Default value supports all format')
    print('\t --prefix/-p      : Default value is "pre"')
    print('\t --beginNum/-b    : Default value is 0')
    print('\t --bitNum/-d      : Default value is 9')
    print('\t --dry_run/-n     : Just print the process, not excuting')
    print('\t --help/-h        : Print usage info')
    print('----------------------------------------------------------------')

def changeName(basePath, file_format, prefix, beginNum, bitNum, bIsDryRun):

    num = int(beginNum)
    bitNum = int(bitNum)
    renameNum = 0
    if not os.path.exists(basePath):
        print("ERRORS:: The path doesn't exist")
        return 

    if os.path.isfile(basePath):
        print('ERROR :: Open %s failed'%(basePath))
        return
    else:
        fileLists = sorted(os.listdir(basePath))
        for fileName in fileLists:

            cur_file_format = os.path.splitext(fileName)[1]
            if file_format!='all' and file_format!=cur_file_format:
                continue

            zeroStr = '';
            tmpNum = bitNum
            while tmpNum-getBit(num)>0:
                zeroStr = zeroStr+'0'
                tmpNum = tmpNum-1
                
            newFileName="%s_%s%d%s"%(prefix,zeroStr, num, cur_file_format)
            if newFileName == fileName:
                num = num+1
                continue;
        
            # check the file is still in the list
            while 1:
                if newFileName in fileLists:
                    fileLists.remove(newFileName)
                    num = num+1
                    newFileName="%s_%s%d%s"%(prefix,zeroStr,num,cur_file_format)
                else :
                    num = num+1
                    break

            oldName = "%s/%s"%(basePath, fileName)
            newName = "%s/%s"%(basePath, newFileName)
            renameNum = renameNum + 1
            if bIsDryRun:
                print(oldName+'  -->  '+newName)
            else:
                os.rename(oldName, newName)

    print("Rename  %d files"%(renameNum))
           
def main():
    if(len(sys.argv)<2):
        print("ERROR:: The input Para is wrong")
        usage()
        return

    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhnf:p:b:d:", ["verbose", "help","dry-run", "file_format=", "prefix=", "beginNum=", "bitNum="])
  
    except getopt.GetoptError:
        print("ERROR:: Errors occur in getting option Paras")
        usage()
        return 

    file_format = 'all'
    prefix = "pre"
    beginNum = 0
    bitNum = 9
    bIsDryRun = False
    bIsPrintHelp = False
    for op, arg in opts:
        if op in ("-f", "--file_format"):
            file_format = ".%s"%(arg)
        elif op in ("-p", "--prefix"):
            prefix = arg
        elif op in ("--beginNum","-b"):
            beginNum = arg
        elif op in ("--bitNum","-d"):
            bitNum = arg
        elif op in ("--dry-run","-n"):
            bIsDryRun = True
        elif op in ("--help","-h"):
            bIsPrintHelp = True
         
    if bIsPrintHelp:
        usage()
        return
    path = args[0]
    changeName(path, file_format, prefix, beginNum, bitNum, bIsDryRun)
        
    print ("Finished")

if __name__ == '__main__':
    main()

    
    



