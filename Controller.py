import rospy
import subprocess
import threading
from tkinter import * 
from geometry_msgs.msg import Twist

PI = 3.1415926535897

class App:

    def __init__(self, master=None):

        self._enable = False

        self.bt_up = Button(master, text="UP", width = 10)
        self.bt_down = Button(master, text="DOWN", width = 10)
        self.bt_r_left = Button(master, text="R-LEFT", width = 10)
        self.bt_r_right = Button(master, text="R-RIGHT", width = 10)
        self.bt_enable_servos = Button(master, text="", width = 2, bg = "red", command = self.servos)
        self.lbl_servos = Label(master, text="servos OFF")

        self.bt_up.bind("<Button-1>", self.btn_exec_up)
        self.bt_down.bind("<Button-1>", self.btn_exec_down)
        self.bt_r_left.bind("<Button-1>", self.btn_exec_c_clockwise)
        self.bt_r_right.bind("<Button-1>", self.btn_exec_clockwise)

        self.bt_up.bind("<ButtonRelease-1>", self.stop_all)
        self.bt_down.bind("<ButtonRelease-1>", self.stop_all)
        self.bt_r_left.bind("<ButtonRelease-1>", self.stop_all)
        self.bt_r_right.bind("<ButtonRelease-1>", self.stop_all)

        self.bt_up.grid(row=0, column=0, columnspan=2, sticky=N)
        self.bt_down.grid(row=2, column=0, columnspan=2, sticky=S)
        self.bt_r_left.grid(row=1, column=0, sticky=W)
        self.bt_r_right.grid(row=1, column=1, sticky=E)
        self.bt_enable_servos.grid(row=0, column=2, rowspan = 2, sticky=N+S)
        self.lbl_servos.grid(row=0, column=3, rowspan = 2, sticky=N+S)

    def servos(self):
       self.state = self.bt_enable_servos["relief"]
       if self.state == RAISED:
          self.bt_enable_servos["relief"] = SUNKEN
          self.bt_enable_servos["bg"] = "green"
          self.lbl_servos.configure(text="servos ON")
          self._enable = True
       else:
          self.bt_enable_servos["relief"] = RAISED
          self.bt_enable_servos["bg"] = "red"
          self.lbl_servos.configure(text="servos OFF")
          self._enable = False

    def btn_exec_up(self, event):
        if self._enable == True:
           self.speed = 2
           self.distance = 1
           self.isForward = True
           move_linear(self.speed, self.distance, self.isForward)

    def btn_exec_down(self, event):

        if self._enable == True:
           self.speed = 2
           self.distance = 1
           self.isForward = False
           move_linear(self.speed, self.distance, self.isForward)

    def btn_exec_clockwise(self, event):

        if self._enable == True:
           self.speed = 100
           self.angle = 1
           self.clockwise = True
           move_rotate(self.speed, self.angle, self.clockwise)

    def btn_exec_c_clockwise(self, event):

        if self._enable == True:
           self.speed = 100
           self.angle = 1
           self.clockwise = False
           move_rotate(self.speed, self.angle, self.clockwise)

    def stop_all(self, event):

        move_linear()
        move_rotate()

def init_system():
    subprocess.call(["rosrun", "tkinter_test", "app2.py"])

def init_ros():
    rospy.init_node("tkinter_robot", anonymous=True)
    global velocity_publisher
    global vel_msg
    velocity_publisher = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    vel_msg = Twist()

def move_linear(speed = 0, distance = 0, isForward = 1):

    if(isForward):
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)

    # while not rospy.is_shutdown():
    t0 = rospy.Time.now().to_sec()
    current_distance = 0

    while current_distance < distance:
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_distance = speed * (t1 - t0)

    vel_msg.linear.x = 0
    velocity_publisher.publish(vel_msg)
    # break

def move_rotate(speed = 0, angle = 0, clockwise = 0):

angular_speed = speed * 2 * PI / 360
relative_angle = angle * 2 * PI / 360

if clockwise:
    vel_msg.angular.z = -abs(angular_speed)
else:
    vel_msg.angular.z = abs(angular_speed)

t0 = rospy.Time.now().to_sec()
current_angle = 0

while current_angle < relative_angle:
    velocity_publisher.publish(vel_msg)
    t1 = rospy.Time.now().to_sec()
    current_angle = angular_speed * (t1 - t0)

vel_msg.angular.z = 0
velocity_publisher.publish(vel_msg)
#rospy.spin()


if __name__=="__main__":
    #t = threading.Thread(target=rospy.spin)
    #t.start()
    # init_system()
    init_ros()
    janela = Tk()
    App(janela)
    #janela.geometry("500x300+300+300")
    janela.geometry("")
    janela.title("ROS Control Test")
    janela.mainloop()
