import socket
import cv2
import time
import numpy as np

from cryptography.fernet import Fernet



# Load the secret key from the file
with open('secret.key', 'rb') as f:
    key = f.read()
print("key read: ", key)



host = '192.168.1.33' #Server ip
port = 4000


clientid=('192.168.1.17',4005) #Robot ip

userid=('192.168.1.62',5000) #user ip

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setblocking(1)
s.settimeout(0.1) 
s.bind((host, port))

while True:


    print("Waiting for start command...")
    while True:
        try:
            
            data, addr = s.recvfrom(1024)

            #Check if the data is from the client or the user
            if addr!=clientid or addr!=userid:
                continue
            data=Fernet(key).decrypt(data)
            print(data.decode())
            
            print(addr)
            if data.decode()=='start':
                print("STARTING THE PROCESS")
                msg=b'got message'
                msg=Fernet(key).encrypt(msg)
                s.sendto(msg,addr)
                break
        except socket.timeout:
            pass

    #START THE PROCESS===============================

    #Taking the video feed from the ip webcam on the robot
    webcam=cv2.VideoCapture('http://192.168.1.59:8080/video')
    while True:
        data=''
        
        try:
            data, addr = s.recvfrom(1024)

            #Check if the data is from the client or the user
            if addr!=clientid or addr!=userid:
                continue

            #Decrypt the data
            data=Fernet(key).decrypt(data)
            if data.decode()!='start':

                print(data.decode())
                print(addr)
            else:
                print("CONTINUING THE PROCESS")
                continue
        except socket.timeout:
            pass
        red_flag=0
        green_flag=0
        
        # Reading the video from the
        # webcam in image frames
        _, imageFrame = webcam.read()

        height, width, _ = imageFrame.shape
        cent_y = int(height/2)
        cent_x = int(width/2)
    
        # Convert the imageFrame in 
        # BGR(RGB color space) to 
        # HSV(hue-saturation-value)
        # color space
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
    

        # Set range for blue color and 
        # define mask
        red_lower = np.array([100, 100, 100], np.uint8)
        red_upper = np.array([130, 255, 255], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    
        # Set range for green color and 
        # define mask
        green_lower = np.array([50, 75, 72], np.uint8)
        green_upper = np.array([80, 255, 255], np.uint8)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    
        
        # Morphological Transform, Dilation
        # for each color and bitwise_and operator
        # between imageFrame and mask determines
        # to detect only that particular color
        kernel = np.ones((8, 8), "uint8")
        
        # For red color
        red_mask = cv2.dilate(red_mask, kernel)
        res_red = cv2.bitwise_and(imageFrame, imageFrame, 
                                mask = red_mask)
        
        # For green color
        green_mask = cv2.dilate(green_mask, kernel)
        res_green = cv2.bitwise_and(imageFrame, imageFrame,
                                    mask = green_mask)
        
        # Creating contour to track blue color
        contours_red, hierarchy_red = cv2.findContours(red_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
        #Get biggest contour only
        contours_red = sorted(contours_red, key = cv2.contourArea, reverse = True)[:1]


        #If blue object is detected, then superimpose on the image
        if contours_red:
            
        
            for pic, contour in enumerate(contours_red):
                area = cv2.contourArea(contour)
                if(area > 200) :
                    red_flag=1
                #if 1:
                    x, y, w, h = cv2.boundingRect(contour)

                
                    cx_red = int(x + w/2)
                    #cx_red = int(x)
                    imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                            (x + w, y + h), 
                                            (0, 0, 255), 2)
                    
                    cv2.putText(imageFrame, "Blue Colour", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                (0, 0, 255))    
        
        # Creating contour to track green color
        contours_green, hierarchy_green = cv2.findContours(green_mask,
                                            cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)
        contours_green = sorted(contours_green, key = cv2.contourArea, reverse = True)[:1]
        
        #If green object is detected, then superimpose on the image
        if contours_green:
            
        
            for pic, contour in enumerate(contours_green):
                area = cv2.contourArea(contour)
                if(area > 200):
                    green_flag=1
                    x, y, w, h = cv2.boundingRect(contour)

                    cx_green = int(x + w/2)
                    #cx_green = int(x)

                    imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                            (x + w, y + h),
                                            (0, 255, 0), 2)
                    
                    cv2.putText(imageFrame, "Green Colour", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                1.0, (0, 255, 0))
        cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
        #When robot says send next, send the next command
        if data:
            data=data.decode('utf-8')
            if data=='send next':    
                if red_flag:
                    print("Blue")
                    red_flag=0
                    
                    if cx_red<cent_x-30:
                        print("Blue Left")
                        #encrypt message before sending
                        msg=Fernet(key).encrypt("Red Left")
                        s.sendto(msg, clientid)

                    
                    elif cx_red>cent_x+30:
                        print("Blue Right")
                        #encrypt message before sending
                        msg=Fernet(key).encrypt("Red Right")
                        s.sendto(msg, clientid)
                        
                    else:
                        print("Blue Straight")
                        #encrypt message before sending
                        msg=Fernet(key).encrypt("Red Straight")
                        s.sendto(msg, clientid)
                        
                elif red_flag==0 and green_flag==0:
                    print("Turn around")
                    #encrypt message before sending
                    msg=Fernet(key).encrypt("Turn around")
                    s.sendto(msg, clientid)
                    
                elif green_flag and red_flag==0:
                    green_flag=0
                    if cx_green<cent_x-30:
                        print("Green Left")
                        #encrypt message before sending
                        msg=Fernet(key).encrypt("Green Left")
                        s.sendto(msg, clientid)
                        

                    elif cx_green>cent_x+30:
                        print("Green Right")
                        #encrypt message before sending
                        msg=Fernet(key).encrypt("Green Right")
                        s.sendto(msg, clientid)
                    
                    else:
                        print("Green Straight")
                        #encrypt message before sending
                        msg=Fernet(key).encrypt("Green Straight")
                        s.sendto(msg, clientid)
            elif data=='finished':
                print("Robot has completed the task")
                break
                    
                


   


