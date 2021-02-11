import matlab.engine
eng = matlab.engine.start_matlab()
eng.cd(r'C:\Users\BAB\Desktop\Fotballmaskin-master-python3\src\Fotballmaskin\Pcprogram\optimalisering')
eng.make_init(nargout=0)
## 1. CALIBRATION ##
#Shoot 10m/s, 45 degrees
speed = 10.0
theta = 0.0
psi = 45.0
omega = 0.0
kd_old=1.0
kl_old=1.0
kw_old=1.0
#Make the machine shoot with these conditions
desired_point_string = input("Where did the ball land? Please answer with coordinates X,Y,Z where origin is the machine and Y is the shooting direction.")
desired_point_string_list=list(desired_point_string.split(','))
p_w=matlab.double(list(map(float,desired_point_string_list)))

[x_return] = eng.find_initvalues_speed(p_w,1.0,1.0,1.0,nargout=1)
# print("kd_new: ", kd_new)
# print("kl_new: ", kl_new)
# print("kw_new: ", kw_new)
print("System is calibrated. Ready to shoot")


## 2. RUN ##
#While True/exit button clicked:
p_w = input("What is the desired landing point?") #Erstattes av brukergrensesnitt
[x_return] = eng.find_initvalues_speed(p_w,k_d,k_l,k_w,nargout=1)
print("x_return: ", x_return)
#Shoot
#while calibrate_speed != "Y"
calibrate_speed = input("Do you wish to calibrate the speed?")
if calibrate_speed: 
    [speed]=eng.find_speed(p_w,speed_0,psi_0,k_d,k_l,k_w)
#Shoot



