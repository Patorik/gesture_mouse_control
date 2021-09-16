import cv2

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break
        print("Could not read more frames")

    cv2.imshow("Cameraframe", frame)

    key = cv2.waitKey(1)

    if key==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()