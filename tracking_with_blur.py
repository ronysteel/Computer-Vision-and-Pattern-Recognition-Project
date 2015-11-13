import os
import numpy as np
import cv2
import copy


# def find_if_close(cnt1,cnt2):
#    row1,row2 = cnt1.shape[0],cnt2.shape[0]
#    for i in xrange(row1):
#        for j in xrange(row2):
#            dist = np.linalg.norm(cnt1[i]-cnt2[j])
#            if abs(dist) < 10 :
#                return True
#            elif i==row1-1 and j==row2-1:
#                return False

# def removeOverlaps(cnts):
#     for i,cnt1 in enumerate(cnts):
#         if i < len(cnts)-2:
#             for j,cnt2 in enumerate(cnts[i+1:]):
#                 (x, y, w, h) = cv2.boundingRect(cnt1)
#                 (x1, y1, w1, h1) = cv2.boundingRect(cnt2)
#                 if((x1<x<x1+w1 and (y<y1<y+h or y<y1+h1<y+h or (y1+h1>y+h and y1<y)) or  ))
#
#
#
#                 if ((x1 > x and x1 < x+w ) or (x1+w1 > x and x1+w1 < x+w) or (y1+h1 > y and y1+h1 < y+h) or (y1 > y and y1<y+h)):
#                     cnts[j] = 0
#     return cnts


 
cap = cv2.VideoCapture(os.getcwd() + "/stitchedVideo.mov")
firstFrame = cv2.imread(os.getcwd()+ "/background.jpg")
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])
lower_red = np.array([0,140,110])
upper_red = np.array([20,200,255])
lower_white = np.array([42,10,130])
upper_white = np.array([65,17,211])
lower_yellow = np.array([30,150,200])
upper_yellow = np.array([100,255,255])
# lower_green = np.array([40,200,200])
# upper_green = np.array([71,255,255])
# for referees
lower_green = np.array([30,150,200])
upper_green = np.array([100,255,255])

#lower_green = np.array([40,110,55])
# upper_green = np.array([40,120,128])


# lower_yellow = np.array([0,155,215])
# # bright green
# upper_yellow = np.array([100,255,255])
cv2.namedWindow("Final", 0)

#cv2.resizeWindow("Final", 1200,500)
height,width,layers = firstFrame.shape
maskImg = np.ones(firstFrame.shape[:2], dtype="uint8") * 255
# clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4,4))
for i in range (0,100):
    _,frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    kernel = np.ones((5,5),np.uint8)    
        
    # find blue players
    maskBlue = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(frame,frame, mask=maskBlue)
    image = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(image, (33,33),1)
    # cv2.imshow('blur',blurred)
    # cv2.waitKey(0)
    dilation = cv2.dilate(blurred,kernel,iterations = 6)
    # cv2.imshow('dilation',dilation)
    # cv2.waitKey(0)
    _,threshBlue = cv2.threshold(dilation,10,255, cv2.THRESH_BINARY)
    (cntsBlue, _) = cv2.findContours(threshBlue,cv2.cv.CV_RETR_TREE,cv2.cv.CV_CHAIN_APPROX_SIMPLE)

    # find red players
    maskRed = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame,frame, mask=maskRed)
    image = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(image, (33,33),1)
    # cv2.imshow('blur',blurred)
    # cv2.waitKey(0)
    dilation = cv2.dilate(blurred,kernel,iterations = 6)
    # cv2.imshow('dilation',dilation)
    # cv2.waitKey(0)
    _,threshRed = cv2.threshold(dilation,10,255, cv2.THRESH_BINARY)
    (cntsRed, _) = cv2.findContours(threshRed,cv2.cv.CV_RETR_TREE,cv2.cv.CV_CHAIN_APPROX_SIMPLE)

    # find yellow players
    maskYellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res = cv2.bitwise_and(frame,frame, mask=maskYellow)
    image = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(image, (33,33),1)
    dilation = cv2.dilate(blurred,kernel,iterations = 6)
    _,threshYellow = cv2.threshold(dilation,10,255, cv2.THRESH_BINARY)
    (cntsYellow, _) = cv2.findContours(threshYellow,cv2.cv.CV_RETR_TREE,cv2.cv.CV_CHAIN_APPROX_SIMPLE)
    
    # find green players
    maskGreen = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(frame,frame, mask=maskGreen)
    image = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(image, (33,33),1)
    # cv2.imshow('blur',blurred)
    # cv2.waitKey(0)
    dilation = cv2.dilate(blurred,kernel,iterations = 6)
    # cv2.imshow('dilation',dilation)
    # cv2.waitKey(0)
    _,threshGreen = cv2.threshold(dilation,10,255, cv2.THRESH_BINARY)
    (cntsGreen, _) = cv2.findContours(threshGreen,cv2.cv.CV_RETR_TREE,cv2.cv.CV_CHAIN_APPROX_SIMPLE)
    
    
    maskWhite = cv2.inRange(hsv, lower_white, upper_white)
    res = cv2.bitwise_and(frame,frame, mask=maskWhite)
    image = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(image, (33,33),1)
    # cv2.imshow('blur',blurred)
    # cv2.waitKey(0)
    dilation = cv2.dilate(blurred,kernel,iterations = 6)
    # cv2.imshow('dilation',dilation)
    # cv2.waitKey(0)
    _,threshWhite = cv2.threshold(dilation,10,255, cv2.THRESH_BINARY)
    (cntsWhite, _) = cv2.findContours(threshWhite,cv2.cv.CV_RETR_TREE,cv2.cv.CV_CHAIN_APPROX_SIMPLE)
                         
    for c in cntsBlue:
        # if cv2.contourArea(c) < 100:
        #     # move to next contour
        #     continue
        M = cv2.moments(c)
        if (M['m00'] != 0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(frame, (cx,cy), 15,(255,0,0),2)
            
    for c in cntsRed:
        M = cv2.moments(c)
        if (M['m00'] != 0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(frame, (cx,cy), 15,(0,0,255),2)

    for c in cntsYellow:
        M = cv2.moments(c)
        if (M['m00'] != 0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(frame, (cx,cy), 15,(0,255,255),2)
            
    for c in cntsGreen:
        M = cv2.moments(c)
        if (M['m00'] != 0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(frame, (cx,cy), 15,(0,255,0),2)
    
    for c in cntsWhite:
        if cv2.contourArea(c) < 500 and cv2.contourArea(c) > 800:
            # move to next contour
            continue       
        M = cv2.moments(c)
        if (M['m00'] != 0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(frame, (cx,cy), 15,(255,255,255),2)        
            
                    

    resizedImage = cv2.resize(frame,(2451,270))
    cv2.imshow("Final", resizedImage)
    cv2.waitKey(30)
cv2.waitKey(0)
cv2.destroyAllWindows()
cap.release()
