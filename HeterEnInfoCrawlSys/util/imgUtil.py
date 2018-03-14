#coding:utf-8
import cv2
import matplotlib.pyplot as plt
#(x=0,y=345)-->(x=115,y=380)342*380
def slice(img):
    wordimg=img[0:115,345:380]
    dictimg=img[0:340,0:345]
if __name__=='__main__':
    img=cv2.imread('img.png',0)
    # cv2.imshow('imgO',img)
    dictimg =img[0:343,0:345]
    wordimg=img[345:380,0:115]
    # cv2.imshow("imgw",wordimg)
    # cv2.imshow("imgd", dictimg)
    ret,wbin=cv2.threshold(wordimg,127,255,cv2.THRESH_BINARY_INV)
    cv2.imshow('img',wbin)
    s=map(sum,wbin.T)
    # plt.plot(s)
    # plt.show()
    flag=False
    list=[]
    for i in xrange(len(s)):
        if not flag and s[i] > 256 :
            start=i
            flag =True
        if flag and (i-start)>12 and s[i] <=256 :
            end=i
            flag=False
            img=wordimg[:,start:end+1]
            ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
            list.append(img)
    dictbin = cv2.adaptiveThreshold(dictimg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10)
    dictbin=cv2.GaussianBlur(dictbin, (5, 5), 0)

    subCanny=cv2.Canny(dictimg,200,200)
    subimg = cv2.subtract(dictimg, subCanny)
    subimg1 = cv2.adaptiveThreshold(subimg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 10)

    for img in list:
        cv2.imshow("word",img)
        cv2.imshow('dict',subimg1)
        cv2.waitKey(0)
        res=cv2.matchTemplate(subimg1,img,cv2.TM_CCOEFF)
        minV,maxV,minL,maxL=cv2.minMaxLoc(res)
        cv2.rectangle(dictimg,(maxL),(maxL[0]+10,maxL[1]+10),255,1)

        cv2.imshow('img',dictimg)
        cv2.waitKey(0)
