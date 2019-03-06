import cv2 as cv
import numpy as np
import matplotlib

going = False #Wurde der erste Punkt gesetzt?


def click(event, x, y, flags, param): 
    
    if event == cv.EVENT_LBUTTONDOWN:
        global going, pt2x, pt1x, pt1y
        if going == True:
            cv.circle(img, (350, 90), 20, (200, 200, 255), -1)
            cv.circle(img, (x, y), 5, (0, 255,0), -1)
            pt2x = x
            pt2y = y
            cv.circle(img, (int((pt2x + pt1x) / 2), pt1y), 5, (0,0,0), -1) #Mittelpunkt der gesetzten Punkte drawn
            going = False
           

        else:
            cv.circle(img, (350, 40), 20, (200, 200, 255), -1)
            going = True
            print(x, y)
            cv.circle(img, (x, y), 5, (0, 255,0), -1)
            pt1x = x
            pt1y = y
            
FOV = 53 #Sichtwinkel der Kamera in Grad
GPP = FOV/1920

img = cv.imread("Cones.png", cv.IMREAD_GRAYSCALE)
cv.namedWindow("Main")
cv.setMouseCallback("Main", click)

font = cv.FONT_HERSHEY_COMPLEX
cv.putText(img, "Punkt 1 setzen", (50,50), font, 1, (200,255,255), 2, cv.LINE_AA) #Anleitung
cv.putText(img, "Punkt 2 setzen", (50,100), font, 1, (200,255,255), 2, cv.LINE_AA)
cv.putText(img, "Mit C bestätigen", (50,150), font, 1, (200,255,255), 2, cv.LINE_AA)

global pt0 

while True:
    cv.imshow("Main", img)
    key = cv.waitKey(1) & 0xFF
    if key == ord("c"):  
        cv.circle(img, (350, 140), 20, (200, 200, 255), -1)
        pt0 = (int((pt2x + pt1x) / 2))
        break

print(pt0 * GPP)
cv.putText(img, str(pt0 * GPP), (1000,1000), font, 1, (200,255,255), 2, cv.LINE_AA)
cv.waitKey(0)

   


