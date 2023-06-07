import RPi.GPIO as GPIO
from MFRC522_IOT import MFRC522_IOT
import time
import socket
from cryptography.fernet import Fernet

host='192.168.1.72' #user ip
port=5000

serverid=('192.168.1.33',4000) #Server ip
clientid=('192.168.1.17',4005) #Robot ip
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setblocking(1)
s.settimeout(1)


reader = MFRC522_IOT()


# Load the secret key from the file
with open('secret.key', 'rb') as f:
    key = f.read()
print("key read: ", key)

clientid=('192.168.1.17',4005) #Robot ip

serverid=('192.168.1.33',4000)

s.bind((host,port))

def start_process():
        
        print("Trying to connect to SERVER")
        while True:
                try:    
                        msg=b"start"
                        msg=Fernet(key).encrypt(msg)
                        s.sendto(msg,serverid)
                        
                        d1,add=s.recvfrom(1024)

                        
                        if d1:  
                                if add!=serverid:
                                        continue
                                else:
                                        print("server got message")
                                        break
                        
                        
                        
                except socket.timeout:
                        pass
        time.sleep(1)
        print("Trying to connect to Robot")
        time.sleep(2)
        
        while True:
                
                try:                        
                        msg=b"start"
                        msg=Fernet(key).encrypt(msg)
                        s.sendto(msg,clientid)
                        
                        
                        d2,add=s.recvfrom(1024)
                        
                        if d2:
                                if add!=clientid:
                                        continue
                                else:
                                        
                                        print("Robot got message")
                                        break
                        
                except socket.timeout:
                        pass
        print("START MESSAGE SENT")
      
def wait_process_end():
        print("Robot is performing the task. Waiting for the process to end")
        while True:
                try:
                        d,add=s.recvfrom(1024)

                        if d:
                                if add!=clientid:
                                        continue
                                else:
                                        d=Fernet(key).decrypt(d).decode()
                                        if d=="finished":
                                                print("process ended. start new......\n")
                                                break
                except socket.timeout:
                        pass



try:
        while True:
                wrong_count=0
                print("place your tag for reading")
                id, text = reader.read()
                
                text=text.split(' ')[0]

             
                while True:
                        if text=="alnahian_koyshi":
                                print("Welcome ",text)
                                pwd=input("\nPlease type your password: ")
                                if pwd=='iot':
                                        
                                        start_process()
                                        wait_process_end()
                                        
                                        break
                                else:
                                        print("wrong password")
                                        wrong_count+=1
                                        if wrong_count==3:
                                                print("You have exceeded the maximum number of tries. wating for 60 seconds")
                                                time.sleep(6)
                                                wrong_count=0
                                                
                        else: 
                                print("Unknown ID. Freezing for 60 seconds")
                                time.sleep(6)
                                break
                        
        
finally:
        GPIO.cleanup()
        print("clean up")
