import cv2
import time

cap = cv2.VideoCapture(0)
cTime = pTime = 0

while cap.isOpened():
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