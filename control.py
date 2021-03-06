import cv2
import time
import numpy as np
import autopy as ap
import argparse
from screeninfo import get_monitors
import os

class Controller:
    def __init__(self):
        self.capResolution = (640, 360)
        self.screen = get_monitors()[0]
        self.toggleSave = False
        self.cap = cv2.VideoCapture(0)
        ratio = (self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)/self.capResolution[0] , self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/self.capResolution[1])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.capResolution[1])
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.capResolution[0])
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.res = np.zeros([self.capResolution[1], self.capResolution[0]], dtype='uint8')
        self.tX, self.tY = self.screen.width/self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)*ratio[0], self.screen.height/self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)*ratio[1]

    def passFunction(self, x):
        pass

    def initTrackbar(self):
        cv2.namedWindow("HSV Trackbars")
        cv2.moveWindow("HSV Trackbars", int(self.screen.width/2.5), int(self.screen.height/2.5))
        cv2.createTrackbar("L - H", "HSV Trackbars", 0, 179, self.passFunction)
        cv2.createTrackbar("L - S", "HSV Trackbars", 0, 255, self.passFunction)
        cv2.createTrackbar("L - V", "HSV Trackbars", 0, 255, self.passFunction)
        cv2.createTrackbar("U - H", "HSV Trackbars", 179, 179, self.passFunction)
        cv2.createTrackbar("U - S", "HSV Trackbars", 255, 255, self.passFunction)
        cv2.createTrackbar("U - V", "HSV Trackbars", 255, 255, self.passFunction)

    def triggerSave(self):
        self.toggleSave = True

    def saveHSVData(self, l_h, l_s, l_v, u_h, u_s, u_v):
        result = str(l_h) + "\n" + str(l_s) + "\n" + str(l_v) + "\n" + str(u_h) + "\n" + str(u_s) + "\n" + str(u_v)
        with open("HSV_DATA.txt", "w") as file:
            file.write(result)
    
    def readHSVData(self):
        data = []
        with open("HSV_DATA.txt", "r") as file:
            data = file.read().rstrip('\n').split('\n')
        i = 0
        while i<len(data):
            data[i] = int(data[i])
            i+=1
        return data

    def detectAndControl(self):
        cTime = 0
        pTime = 0
        while self.cap.isOpened():
            
            if self.toggleSave:
                l_h = cv2.getTrackbarPos("L - H", "HSV Trackbars")
                l_s = cv2.getTrackbarPos("L - S", "HSV Trackbars")
                l_v = cv2.getTrackbarPos("L - V", "HSV Trackbars")
                u_h = cv2.getTrackbarPos("U - H", "HSV Trackbars")    
                u_s = cv2.getTrackbarPos("U - S", "HSV Trackbars")    
                u_v = cv2.getTrackbarPos("U - V", "HSV Trackbars")
            else:
                # Predefined values for trackbars
                l_h, l_s, l_v, u_h, u_s, u_v = self.readHSVData()

            lower_color = np.array([l_h, l_s, l_v])
            upper_color = np.array([u_h, u_s, u_v])
            # print(f"HSV values (lower treshold):{lower_color}")
            # print(f"HSV values (upper treshold):{upper_color}")

            ret, frame = self.cap.read()
            if not ret:
                break
                print("Could not read more frames")
            frame = cv2.flip(frame, 1)

            # blurred_frame = cv2.GaussianBlur(frame, (9,9), 0)
            blurred_frame = cv2.medianBlur(frame, 9)
            hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_frame, lower_color, upper_color)
            visible_frame = cv2.bitwise_and(blurred_frame, blurred_frame, mask=mask)


            cTime = time.time()
            fps = int(1/(cTime-pTime))
            pTime = cTime
            cv2.putText(frame, str(fps), (10, 70), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 255), 3)
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
                        #print(self.tX*cX, self.tY*cY)
                        if not self.toggleSave:
                            ap.mouse.move(cX*self.tX,cY*self.tY)
                        pass
                except:
                    if cv2.contourArea(contour) > 1000 and cv2.contourArea(contour) < 20000:
                        cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
            
            cv2.imshow("Camera frame", frame)
            cv2.imshow("HSV frame", mask)
            cv2.imshow("Masked frame", visible_frame)
            cv2.imshow("Result", self.res)

            cv2.moveWindow("Camera frame", 0, 0)
            cv2.moveWindow("HSV frame", int(self.screen.width-self.capResolution[0]),0)
            cv2.moveWindow("Masked frame", 0, int(self.screen.height-self.capResolution[1]))
            cv2.moveWindow("Result", int(self.screen.width-self.capResolution[0]), int(self.screen.height-self.capResolution[1]))

            key = cv2.waitKey(1)

            if key==ord('q'):
                break
        
        if self.toggleSave:
            self.saveHSVData(l_h, l_s, l_v, u_h, u_s, u_v)
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--setup', action='store_true', help="This argument tells if we're in testig mode or not.")
    args = parser.parse_args()
    if not os.path.isfile('HSV_DATA.txt'):
        ap.alert.alert("""Welcome!
        This software is a project for Computer Vision subject in my university.
        Let's get Started!
        First you need to set up the upper and lower limits of HSV values. Use the trackbars!
        After you've done it press 'q' and restart the program.
        """)
    controller = Controller()
    if args.setup or not os.path.isfile('HSV_DATA.txt'):
        controller.triggerSave()
        controller.initTrackbar()
        controller.detectAndControl()
    else:
        controller.detectAndControl()