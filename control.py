import cv2
import time
import numpy as np
import autopy as ap


class Controller:
    def __init__(self):
        cv2.namedWindow("HSV Trackbars")
        self.cap = cv2.VideoCapture(0)
        self.res = np.zeros([int(self.cap.get(4)), int(self.cap.get(3))], dtype='uint8')
        self.tX, self.tY = 1920/self.cap.get(3), 1080/self.cap.get(4)
        cv2.createTrackbar("L - H", "HSV Trackbars", 0, 179, self.passFunction)
        cv2.createTrackbar("L - S", "HSV Trackbars", 0, 255, self.passFunction)
        cv2.createTrackbar("L - V", "HSV Trackbars", 0, 255, self.passFunction)
        cv2.createTrackbar("U - H", "HSV Trackbars", 179, 179, self.passFunction)
        cv2.createTrackbar("U - S", "HSV Trackbars", 255, 255, self.passFunction)
        cv2.createTrackbar("U - V", "HSV Trackbars", 255, 255, self.passFunction)

    def passFunction(self, x):
        pass

    def detect_and_control(self):
        while self.cap.isOpened():

            cTime = 0
            pTime = 0

            l_h = cv2.getTrackbarPos("L - H", "HSV Trackbars")
            l_s = cv2.getTrackbarPos("L - S", "HSV Trackbars")
            l_v = cv2.getTrackbarPos("L - V", "HSV Trackbars")
            u_h = cv2.getTrackbarPos("U - H", "HSV Trackbars")    
            u_s = cv2.getTrackbarPos("U - S", "HSV Trackbars")    
            u_v = cv2.getTrackbarPos("U - V", "HSV Trackbars")

            lower_color = np.array([l_h, l_s, l_v])
            upper_color = np.array([u_h, u_s, u_v])

            # Predefined values for trackbars
            #lower_color = np.array([26, 21, 93])
            #upper_color = np.array([52, 255, 255])

            # print(f"HSV values (lower treshold):{lower_color}")
            # print(f"HSV values (upper treshold):{upper_color}")

            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 1)

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
                        maskb = np.zeros([int(self.cap.get(4)), int(self.cap.get(3))], np.uint8)
                        cv2.drawContours(maskb, [contour], -1, 255, thickness=cv2.FILLED)
                        self.res = cv2.bitwise_and(mask, mask, mask=maskb)
                        visible_frame = cv2.bitwise_and(blurred_frame, blurred_frame, mask=maskb)
                        print(cX, cY)
                        #ap.mouse.move(cX*tX,cY*tY)
                        pass
                except:
                    if cv2.contourArea(contour) > 1000 and cv2.contourArea(contour) < 20000:
                        cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)

            cv2.putText(frame, str(fps), (10, 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 255), 3)
            cv2.imshow("Camera frame", frame)
            cv2.imshow("HSV frame", mask)
            cv2.imshow("Masked frame", visible_frame)
            cv2.imshow("Result", self.res)

            key = cv2.waitKey(1)

            if key==ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    controller = Controller()
    controller.detect_and_control()