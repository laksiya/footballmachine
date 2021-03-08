from roboclaw_3 import Roboclaw
import matlab.engine
import numpy as np

eng = matlab.engine.start_matlab()
eng.cd(r'C:\Users\BAB\Desktop\Fotballmaskin-master-python3\src\Fotballmaskin\Pcprogram\optimalisering')
eng.make_init(nargout=0)
roboclaw = Roboclaw('COM5', 115200)
roboclaw.Open()


## RUN ##
k_d=1.0
k_l=1.0
k_w=1.0


#While True/exit button clicked:
print("""What is the desired landing point?\nThe machine is in origin and Y is shooting direction\nReply in following format:\nX,Y,Z\n""")
desired_point_string = input() #Erstattes av brukergrensesnitt
desired_point_string_list=list(desired_point_string.split(','))
p_w=matlab.double(list(map(float,desired_point_string_list)))
[x_return] = eng.find_initvalues_speed(p_w,k_d,k_l,k_w,nargout=1)
print("x_return: ", x_return) #(9x1)[velocity,theta,psi,omega,lambda,gamma,kd,kl,kw]


if int(theta:=x_return[2])!= 0: 
    #Convert theta to position in encoder
    roboclaw.SpeedAccelDeccelPositionM1(0x80,10000,2000,10000,15000,1) #SpeedAccelDeccelPositionM2(address,accel,speed,deccel,position,buffer)


def set_speed_ball(self,velocity):
        spin=-velocity/(0.1*2*np.pi)
        spinM1=self.calibM1*spin
        spinM2=self.calibM2*spin
        if spinM1<-184879 or spinM2<-178401:
            print("speed is to high!")
            return False
        flagM1=self.set_speedM1(spinM1)
        flagM2=self.set_speedM2(spinM2)
        if not flagM1 and flagM2:
            return False
        return True





#Shoot
#while calibrate_speed != "Y"
# calibrate_speed = input("Do you wish to calibrate the speed?")
# if calibrate_speed: 
#     [speed]=eng.find_speed(p_w,speed_0,psi_0,k_d,k_l,k_w)
# #Shoot



