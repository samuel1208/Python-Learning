#!/home/fshen/Install_samuel/Python/python3.2.3/bin/python3
#coding UTF-8
######################################################################################
##                      only for image search on google.hk                          ##
##                  Not consider sometime it'll crash on google                     ##
######################################################################################
import sys

pyVersion = sys.version[0]
print('python version : %s'%pyVersion)


import multiprocessing
import urllib

if '2' == pyVersion:
    import  urllib2
elif '3' == pyVersion:
    import urllib.request

import re
import threading
import time


URL='https://www.google.com.hk/search?q=pet&num=10&hl=en&newwindow=1&safe=active&qscrl=1&site=imghp&tbm=isch&sout=1&biw=1124&bih=725'
baseURL = 'https://www.google.com.hk' 
maxDepth = 2
savePATH='/home/fshen/samuel/image/'
#some global pattern of regular expression

##  the image url in the website
reP0 = re.compile(r'imgurl=(.*?)&')

##  get the next page url
reP1 = re.compile(r'<a href.*?</a>')
reP2 = re.compile(r'.*?Next.*?')
reP3 = re.compile(r'<a href="(.*?)"')
reP4 = re.compile(r'amp;')

reP5 = re.compile(r'[^/]*$') 

def Download(URLs):
    for url in URLs :
        imgPath = re.findall(reP5,url)
        imgPath = savePATH + imgPath[0]
        try:
            print (url)
            if '2' == pyVersion:
                urllib.urlretrieve(url, imgPath)
            elif '3' == pyVersion:
                urllib.request.urlretrieve(url, imgPath)
            print ("ok")
        except: 
            print ('download file failed : %s'%url)
            pass
    return 


def AnalysisWeb(url, cpuNum, depth) :

    if '2' == pyVersion :
        req = urllib2.Request(url)
    elif '3' == pyVersion :
        req=urllib.request.Request(url)
    #simulate the brower
    req.add_header('User-agent','Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')
    try :
        if '2' == pyVersion :
            handle = urllib2.urlopen(req)
        elif '3' == pyVersion:            
            handle = urllib.request.urlopen(req)
    except:
        print("Open %s failed"%url)
        return

    content= handle.read()
    if '3' == pyVersion :
        content = content.decode()#python3 need to tranfer bytes to str
    handle.close()
    del handle
    #get the image url first
    imgURLs=re.findall(reP0, content)
  
    if 1 == cpuNum : 
        Download(imgURLs)
    else :
        urlLen = len(imgURLs)
        subLen = urlLen // cpuNum # inter divide(not float)
        threads=[]
        for i in range(cpuNum):
            t = threading.Thread(target=Download, args=[imgURLs[i*subLen:min(i*subLen+(subLen),urlLen)]])
            threads.append(t)

        for t in threads: # start threads
            t.start()
        for t in threads: # wait for all
            t.join() # threads to finish

    del imgURLs
    del req
    #welther need to serch the next website
    global maxDepth
    print("\n The %drd page has been done \n"%(depth))
    depth += 1
    if depth <= maxDepth :
        #get the next page url
        tempURL = re.findall(reP1, content)
        tempURL.reverse()# the next url mostly in the bottom
        
        for u  in tempURL :
            nextURL= re.findall(reP2, u)
            if len(nextURL) :
                break
        nextURL = re.findall(reP3, nextURL[0])    
        nextURL = baseURL + re.sub(reP4,'', nextURL[0])
        
        #release some buffer
        del content
        del tempURL
        AnalysisWeb(nextURL, cpuNum, depth)        
    return

def main():
    cpuNum = multiprocessing.cpu_count()
    print('CPU Number : %d'%cpuNum)
    start = time.time()
    AnalysisWeb(URL, cpuNum, 1)
    end = time.time()
    print("consume time : %fs"%(end-start))

main()
