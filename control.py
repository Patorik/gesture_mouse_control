import cv2
import time
import numpy as np

def passFunction(x):
    pass

cap = cv2.VideoCapture(0)
cTime = pTime = 0

cv2.namedWindow("Trackbars")

cv2.createTrackbar("L - H", "Trackbars", 0, 179, passFunction)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, passFunction)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, passFunction)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, passFunction)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, passFunction)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, passFunction)

while cap.isOpened():
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")    
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")    
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")    
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")    
    lower_color = np.array([l_h, l_s, l_v])
    upper_color = np.array([u_h, u_s, u_v])

    print(f"HSV values (lower treshold):{lower_color}")
    print(f"HSV values (upper treshold):{upper_color}")
    
    ret, frame = cap.read()

    if not ret:
        break
        print("Could not read more frames")

    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    cv2.putText(frame, str(fps), (10, 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 255), 3)
    cv2.imshow("Cameraframe", frame)

    key = cv2.waitKey(1)

    if key==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()