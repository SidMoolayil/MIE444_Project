#!/usr/bin/env python3

import cv2
import matplotlib.pyplot as plt
import numpy as np
import obstacleDetection
import maze


import serial
import time

send_command = b''

if __name__ == "__main__":
    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
        time.sleep(0.1)  # wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))

            images = ["IMG_8151.jpg","IMG_8152.jpg","IMG_8153.jpg","IMG_8154.jpg","IMG_8149.jpg"]
            resolution = [4032,3024]

            # maze = maze.generate_maze()
            maze = maze.get_maze()
            ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
            ser.reset_input_buffer()
            count = 0

            while True:
                for img in images:
                    image_path = "/home/pi/MIE444_Code/" + img  # IMG_8151.jpg"  # IMG_8149.jpg" #IMG_8154.jpg" #IMG_8153.jpg"
                    image = cv2.imread(image_path)
                    # cv2.imshow('img',image)

                    if (len(image) == resolution[0]) and (len(image[0]) == resolution[1]):
                        send_command = obstacleDetection.path_planning(image, maze)
                        arduino.write(send_command.encode())
                        # cv2.waitKey(1)
                    else:
                        print("INVALID IMAGE SIZE")
                    if arduino.inWaiting() > 0:
                        answer = arduino.readline()
                        print(answer)
                        arduino.flushInput()
