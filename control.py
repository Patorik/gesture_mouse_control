import cv2
import time
import numpy as np

def passFunction(x):
    pass

cap = cv2.VideoCapture(0)
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

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    visible_frame = cv2.bitwise_and(frame, frame, mask=mask)

    if not ret:
        break
        print("Could not read more frames")

    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    cv2.putText(frame, str(fps), (10, 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 255), 3)
    cv2.imshow("Camera frame", frame)
    cv2.imshow("HSV frame", mask)
    cv2.imshow("Masked frame", visible_frame)

    key = cv2.waitKey(1)

    if key==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()