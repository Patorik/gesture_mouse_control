# Gesture mouse control

This repository makes it possible to control mouse using object detection based on HSV filter.

## Software requirements
- Python 3.8.10
- OpenCV (contrib version 4.5.2)
- autopy (4.0.0)
- numpy (1.20.3)
- screeninfo package
- camera for input image

## How to use
To get the detection work you need to set up the software's HSV values using the trackbars. To start the software in "setup mode" you need to launch it with the following arguments:<br>
`python3 control.py --setup`<br>
Use the trackbars in the middle to set up the HSV values to detect your tool that you want to use for mouse controlling.
You'll see if it's successfull if a green rectangle appears around it with a whit dot in the middle. If you're finished, just press *'q'* to stop the setup. All necessary values of HSV (upper and lower limits) will be saved in a *.txt* file.<br>
After a successfull setup you'll be able to move the mouse with the help of your tool you chose. All you have to do now is to start the program like that:<br>
`python3 control.py`<br>
Now you'll see that the trackbars did not appear but the HSV values are read from the *txt* file. You can start to move your tool in front of the camera to move your mouse around the screen.