import cv2
import time
import numpy as np
import mouse

def passFunction(x):
    pass

cap = cv2.VideoCapture(0)
res = np.zeros([int(cap.get(4)), int(cap.get(3))], dtype='uint8')
cTime = pTime = 0

cv2.namedWindow("HSV Trackbars")

cv2.createTrackbar("L - H", "HSV Trackbars", 0, 179, passFunction)
cv2.createTrackbar("L - S", "HSV Trackbars", 0, 255, passFunction)
cv2.createTrackbar("L - V", "HSV Trackbars", 0, 255, passFunction)
cv2.createTrackbar("U - H", "HSV Trackbars", 179, 179, passFunction)
cv2.createTrackbar("U - S", "HSV Trackbars", 255, 255, passFunction)
cv2.createTrackbar("U - V", "HSV Trackbars", 255, 255, passFunction)

while cap.isOpened():
    l_h = cv2.getTrackbarPos("L - H", "HSV Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "HSV Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "HSV Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "HSV Trackbars")    
    u_s = cv2.getTrackbarPos("U - S", "HSV Trackbars")    
    u_v = cv2.getTrackbarPos("U - V", "HSV Trackbars")
    lower_color = np.array([l_h, l_s, l_v])
    upper_color = np.array([u_h, u_s, u_v])

    # print(f"HSV values (lower treshold):{lower_color}")
    # print(f"HSV values (upper treshold):{upper_color}")
    
    ret, frame = cap.read()
#    blurred_frame = cv2.GaussianBlur(frame, (9,9), 0)
    blurred_frame = cv2.medianBlur(frame, 9)
    hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    visible_frame = cv2.bitwise_and(blurred_frame, blurred_frame, mask=mask)

    if not ret:
        break
        print("Could not read more frames")

    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        M = cv2.moments(contour)
        try:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if cv2.contourArea(contour) > 3000 and cv2.contourArea(contour) < 20000:
                #cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                maskb = np.zeros([int(cap.get(4)), int(cap.get(3))], np.uint8)
                cv2.drawContours(maskb, [contour], -1, 255, thickness=cv2.FILLED)
                res = cv2.bitwise_and(mask, mask, mask=maskb)
                print(cX, cY)
        except:
            if cv2.contourArea(contour) > 1000 and cv2.contourArea(contour) < 20000:
                cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)

    cv2.putText(frame, str(fps), (10, 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 255), 3)
    cv2.imshow("Camera frame", frame)
    cv2.imshow("HSV frame", mask)
    cv2.imshow("Masked frame", visible_frame)
    cv2.imshow("Result", res)

    key = cv2.waitKey(1)

    if key==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()