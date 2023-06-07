import socket
#import cv2
import time
import numpy as np
from HCSR04_lib import HCSR04
import time
from gpiozero import AngularServo


import RPi.GPIO as GPIO
import time
from cryptography.fernet import Fernet

# Set up GPIO pins

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)

TRIG = 4
ECHO = 13

GPIO.setup(TRIG, GPIO.OUT)

instance = HCSR04(TRIG_pin=TRIG, ECHO_pin=ECHO)  # BCM17

instance.init_HCSR04()


# Motor 1 pins
MOTOR1_PIN1 = 17
MOTOR1_PIN2 = 27
MOTOR1_PWM_PIN = 22

# Motor 2 pins
MOTOR2_PIN1 = 23
MOTOR2_PIN2 = 24
MOTOR2_PWM_PIN = 25

# Set up motor pins as outputs
GPIO.setup(MOTOR1_PIN1, GPIO.OUT)
GPIO.setup(MOTOR1_PIN2, GPIO.OUT)
GPIO.setup(MOTOR1_PWM_PIN, GPIO.OUT)

GPIO.setup(MOTOR2_PIN1, GPIO.OUT)
GPIO.setup(MOTOR2_PIN2, GPIO.OUT)
GPIO.setup(MOTOR2_PWM_PIN, GPIO.OUT)

# Create PWM objects for motor control
MOTOR1_PWM = GPIO.PWM(MOTOR1_PWM_PIN, 1000)  # 100 Hz frequency
MOTOR2_PWM = GPIO.PWM(MOTOR2_PWM_PIN, 1000)

# Start PWM with duty cycle of 0 (stopped)
MOTOR1_PWM.start(0)
MOTOR2_PWM.start(0)
GPIO.output(MOTOR1_PIN1, GPIO.LOW)
GPIO.output(MOTOR1_PIN2, GPIO.LOW)
GPIO.output(MOTOR2_PIN1, GPIO.LOW)
GPIO.output(MOTOR2_PIN2, GPIO.LOW)

servo_pin=16
GPIO.setup(16, GPIO.OUT)
pwm=GPIO.PWM(16, 50)
pwm.start(0)
pwm.ChangeDutyCycle(10)
time.sleep(1)

magnet=21
GPIO.setup(magnet, GPIO.OUT)
mag_sig=GPIO.PWM(magnet, 1000)
mag_sig.start(0)

# Define functions to set the motor speed and direction
    
def forward():
    GPIO.output(MOTOR1_PIN1, GPIO.LOW)
    GPIO.output(MOTOR1_PIN2, GPIO.HIGH)
    GPIO.output(MOTOR2_PIN1, GPIO.LOW)
    GPIO.output(MOTOR2_PIN2, GPIO.HIGH)
    MOTOR1_PWM.ChangeDutyCycle(50)
    MOTOR2_PWM.ChangeDutyCycle(50)
    time.sleep(0.2)
    MOTOR1_PWM.ChangeDutyCycle(0)
    MOTOR2_PWM.ChangeDutyCycle(0)
def backward():
    GPIO.output(MOTOR1_PIN1, GPIO.HIGH)
    GPIO.output(MOTOR1_PIN2, GPIO.LOW)
    GPIO.output(MOTOR2_PIN1, GPIO.HIGH)
    GPIO.output(MOTOR2_PIN2, GPIO.LOW)
    MOTOR1_PWM.ChangeDutyCycle(50)
    MOTOR2_PWM.ChangeDutyCycle(50)
    time.sleep(0.35)
    MOTOR1_PWM.ChangeDutyCycle(0)
    MOTOR2_PWM.ChangeDutyCycle(0)
def right():
    GPIO.output(MOTOR1_PIN1, GPIO.LOW)
    GPIO.output(MOTOR1_PIN2, GPIO.HIGH)
    GPIO.output(MOTOR2_PIN1, GPIO.HIGH)
    GPIO.output(MOTOR2_PIN2, GPIO.LOW)
    MOTOR1_PWM.ChangeDutyCycle(70)
    MOTOR2_PWM.ChangeDutyCycle(70)
    time.sleep(0.2)
    MOTOR1_PWM.ChangeDutyCycle(0)
    MOTOR2_PWM.ChangeDutyCycle(0)
def left():
    GPIO.output(MOTOR1_PIN1, GPIO.HIGH)
    GPIO.output(MOTOR1_PIN2, GPIO.LOW)
    GPIO.output(MOTOR2_PIN1, GPIO.LOW)
    GPIO.output(MOTOR2_PIN2, GPIO.HIGH)
    MOTOR1_PWM.ChangeDutyCycle(70)
    MOTOR2_PWM.ChangeDutyCycle(70)
    time.sleep(0.2)
    MOTOR1_PWM.ChangeDutyCycle(0)
    MOTOR2_PWM.ChangeDutyCycle(0)
def turn_around():
    
                                             
    GPIO.output(MOTOR1_PIN1, GPIO.LOW)
    GPIO.output(MOTOR1_PIN2, GPIO.HIGH)
    GPIO.output(MOTOR2_PIN1, GPIO.HIGH)
    GPIO.output(MOTOR2_PIN2, GPIO.LOW)    
    MOTOR1_PWM.ChangeDutyCycle(75)
    MOTOR2_PWM.ChangeDutyCycle(75)
    time.sleep(0.2)
    MOTOR1_PWM.ChangeDutyCycle(0)
    MOTOR2_PWM.ChangeDutyCycle(0)
def turn_about():
    
                                             
    GPIO.output(MOTOR1_PIN1, GPIO.LOW)
    GPIO.output(MOTOR1_PIN2, GPIO.HIGH)
    GPIO.output(MOTOR2_PIN1, GPIO.HIGH)
    GPIO.output(MOTOR2_PIN2, GPIO.LOW)    
    MOTOR1_PWM.ChangeDutyCycle(75)
    MOTOR2_PWM.ChangeDutyCycle(75)
    time.sleep(1.6)
    MOTOR1_PWM.ChangeDutyCycle(0)
    MOTOR2_PWM.ChangeDutyCycle(0)

def stop_wheels():
    GPIO.output(MOTOR1_PIN1, GPIO.LOW)
    GPIO.output(MOTOR1_PIN2, GPIO.LOW)
    GPIO.output(MOTOR2_PIN1, GPIO.LOW)
    GPIO.output(MOTOR2_PIN2, GPIO.LOW)    
    MOTOR1_PWM.ChangeDutyCycle(0)
    MOTOR2_PWM.ChangeDutyCycle(0)
    time.sleep(0.2)

def pick_object():
    print("PICKING UP")
    turn_about()
    mag_sig.ChangeDutyCycle(100)
    for i in [9.5,9,8.5,8,7.5,7,6.5,6]:
        pwm.ChangeDutyCycle(i)
        time.sleep(0.3)
    for i in [6.5,7,7.5,8,8.5,9,9.5,10]:
        pwm.ChangeDutyCycle(i)
        time.sleep(0.3)
    forward()
    forward()

def drop_object():
    print("Dropping object")
    turn_about()
    for i in [9.5,9,8.5,8,7.5,7,6.5,6]:
        pwm.ChangeDutyCycle(i)
        time.sleep(0.3)
    mag_sig.ChangeDutyCycle(0)
    time.sleep(1)
    for i in [6.5,7,7.5,8,8.5,9,9.5,10]:
        pwm.ChangeDutyCycle(i)
        time.sleep(0.3)
    forward()
    forward()


# Load the secret key from the file
with open('secret.key', 'rb') as f:
    key = f.read()
print("key read: ", key)

userid=('192.168.1.62',5000) #user ip
serverid=('192.168.1.33',4000) #server ip
host='192.168.1.17'
port=4005
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.setblocking(1)
s.settimeout(0.2)
s.bind((host,port))   
    
while True:  
   
    
    print("Waiting for start command....")
    while True:
        try:
            data,addr=s.recvfrom(1024)
            if addr!=serverid or addr!=userid:
                continue
            #Decrypt message
            data=Fernet(key).decrypt(data)
            print(data.decode())
            print(addr)
            if data.decode()=='start':
                print("STARTING PROCESS")
                s.sendto("got message".encode(),addr)
                break
        except socket.timeout:
            pass
    
    count=0
    msg=b'send next'
    msg=Fernet(key).encrypt(msg)
    
    s.sendto(msg,serverid)
    
    
    pick_flag=0
    while True:
        distance=instance.measure_distance()
        
        if distance>15 and pick_flag==0: #Object not picked up yet
            data=''
            
            
            try:
                                           
                data,addr=s.recvfrom(1024)
                if addr!=serverid or addr!=userid:
                    continue
                #Decrypt message
                data=Fernet(key).decrypt(data)

                print(data.decode('utf-8'))
                if data:
                    data=data.decode('utf-8')
                    if data=='Red Straight':
                        forward()
                        print('Red Straight')
                    elif data=='Red Left':
                        left()
                        print('Red Left')
                    elif data=='Red Right':
                        right()
                        print('Red Right')
                    elif data=='Turn around':
                        turn_around()
                        print('Turn Around')
                    else:
                        turn_around()
                    
                
                else:
                
                    print('No data')
                    #turn_around()
                msg=b'send next'
                msg=Fernet(key).encrypt(msg)
                s.sendto(msg,serverid)
                
            except socket.timeout:
                pass
        elif distance<15 and pick_flag==0:
            pick_object()
            pick_flag=1
            print("picked up object")
            msg=b'send next'
            msg=Fernet(key).encrypt(msg)
            s.sendto(msg,serverid)
            
        elif distance>15 and pick_flag==1: #Already picked up object
            data=''
            
            
            try:
                
                
                data,addr=s.recvfrom(1024)
                if addr!=serverid or addr!=userid:
                    continue
                #Decrypt message
                data=Fernet(key).decrypt(data)

                print(data.decode('utf-8'))
                if data:
                    data=data.decode('utf-8')
                    if data=='Green Straight':
                        forward()
                        print('Green Straight')
                    elif data=='Green Left':
                        left()
                        print('Green Left')
                    elif data=='Green Right':
                        right()
                        print('Green Right')
                    elif data=='Turn around':
                        turn_around()
                        print('Turn Around')
                    else:
                        turn_around()
                    
                
                else:
                
                    print('No data')
                    #turn_around()
                msg=b'send next'
                msg=Fernet(key).encrypt(msg)
                s.sendto(msg,serverid)
                
            except socket.timeout:
                pass
        elif distance<15 and pick_flag==1:
            drop_object()
            print("Dropped the object Object")
            msg=b'finished'
            msg=Fernet(key).encrypt(msg)
            s.sendto(msg,serverid)
            s.sendto(msg,userid)
            break
    print("FINISHED")
    

