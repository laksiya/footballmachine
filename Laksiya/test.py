#Start with Raspberry Pi 
from roboclaw_3 import Roboclaw
import numpy as np
import matlab.engine
import time

address = [0x80]
roboclaw = Roboclaw("/dev/ttyS0", 38400)
roboclaw.Open()

roboclaw.ForwardM1(address[0],64) #range is 0 - 127
roboclaw.ForwardM2(address[0],64)
time.sleep(2)

def init_all_motors():
    roboclaw.ForwardM1(address[0],0) #range is 0 - 127
    roboclaw.ForwardM2(address[0],0)
    # roboclaw.ForwardM1(address[1],0)
    # roboclaw.ForwardM2(address[1],0)

def get_optimal_settings():
    eng = matlab.engine.start_matlab()
    eng.cd(r'C:\Users\BAB\Desktop\Fotballmaskin-master-python3\src\Fotballmaskin\Pcprogram\optimalisering')
    eng.make_init(nargout=0)

    #GUI
    print("""What is the desired landing point?\nThe machine is in origin 
    and Y is shooting direction\nReply in following format:\nX,Y,Z\n""") 
    desired_point_string = input() 

    #Format input
    desired_point_string_list=list(desired_point_string.split(','))
    p_w=matlab.double(list(map(float,desired_point_string_list)))

    #Calculate optimal settings
    k_d=1.0
    k_l=1.0
    k_w=1.0

    [x_return] = eng.find_initvalues_speed(p_w,k_d,k_l,k_w,nargout=1)
    print("x_return: ", x_return) #(9x1)[velocity,theta,psi,omega,lambda,gamma,kd,kl,kw]
    return x_return

def calibrate_speed():
    #Work in progress
    calibM1=1
    calibM2=1
    roboclaw.ForwardM1(address[0],127) #range is 0 - 127
    roboclaw.ForwardM2(address[0],127)
    time.sleep(5)
    print("insert the ball")
    enc1 = roboclaw.ReadEncM1(address[0])
    enc2 = roboclaw.ReadEncM2(address[0])
    print(("max speed for m1 is"+str(enc1*0.1*2*np.pi)))
    calibM1=1+(1-(-1*enc1*(0.1*2*np.pi))/fart) # QPPS
    print(calibM1)
    calibM2=1+(1-(-1*enc2*(0.1*2*np.pi))/fart)
    print(calibM2)
    roboclaw.ForwardM1(address[0],0) #range is 0 - 127
    roboclaw.ForwardM2(address[0],0)
    return calibM1,calibM2


def set_ball_speed(speed):
    radius = 0.1
    rotation_speed = speed/(radius*2*np.pi)
    #The wheels must have the desired physical speed 
    speed_max = 100/(radius*2*np.pi) #QPPS real speed
    speed_min = 0
    range_min = 0
    range_max = 127

    digital_speed = ((rotation_speed - speed_min) / (speed_max - speed_min))* (range_max - range_min) + range_min
    
    try: 
        roboclaw.SetM1Speed(address[0], digital_speed)
        roboclaw.SetM2Speed(address[0], digital_speed)
        return True
    except:
        print("error: set_ball_speed")
        return False

def set_angle(angle):
    speed_max = 0 
    speed_min = 80
    range_min = 0
    range_max = 127

    digital_speed = ((speed - speed_min) / (speed_max - speed_min))* (range_max - range_min) + range_min
    
    #Default accel deccel value is 655360. Tweak this to get desired behaviour
    #The value of 32768 is equal to 100% and the motor controller will reach the target value in one second.
    #raw_value = ( percentage / 100 ) x 32768
    #accel = raw_value
    #deccel = raw_value
    #SpeedAccelDeccelPositionM1(self,address,accel,speed,deccel,position,buffer)
    #roboclaw.SpeedAccelDeccelPositionM1(0x80,10000,2000,10000,15000,0)
    #roboclaw.SpeedAccelDeccelPositionM1(0x80,32000,12000,32000,50000,0)
    #roboclaw.SpeedAccelDeccelPositionM1(0x80,32768,12000,32768,50000,0)