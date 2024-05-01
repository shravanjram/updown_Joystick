import serial                                                                                                                                                                                                                               
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Entry,messagebox
from time import strftime
import os
import time
import threading
import math
import multiprocessing

#seral port closing
def serial_close():
    global ser
    global ser_Flag
    ser_Flag=0
    ser.close()       
#to output line
def  draw_line(second_root,row,column,length,orientation,color = 'black'):
        line_frame = tk.Frame(second_root,background = color,width = length)
        line_frame.grid(row = row,column = column,columnspan = 100,sticky = 'ew')
        second_root.columnconfigure(column,weight = 1)
        
#COM port selection console
def update_button_text1(selected_option1,textbox,option_menu1):
    global com_port
    global ser
    global ser_Flag
    com_port = selected_option1
    textbox.config(text=selected_option1)
    option_menu1.pack_forget()
    option_menu1.config(state='disabled')
    ser = serial.Serial(com_port)
    ser.baudrate = 115200
    ser_Flag=1

                        
#for second video console
def on_option_selected():
    global second_root
    global ser_Flag
    global draw_line
    selected_option=selected_option1.get()
    first_root.destroy()
    second_root = tk.Tk()
    second_root.title('Video Tracker Console')
    second_root.geometry('620x650')
    second_root.resizable(False, False)
    window_width = second_root.winfo_width()
    draw_line(second_root,row = 15,column = 0,
              length = window_width,orientation = 'HORIZONTAL')
    label=tk.Label(second_root,
                   text = 'Selected COM Port : ' + selected_option,
                   font = ('calibri',10))
    label.grid(column = 0,row = 1,padx = 5,pady = 5,sticky = "w")


    #receive serial data
    def read_serial_data():
        global data
        global ser
        global Previous_read_serial_data
        Previous_read_serial_data = data
        if ser_Flag:
            if ser.in_waiting > 0:
                try:
                    data = '                             '
                    data = ser.readline().decode().strip()
                    #print(data)
                    #Process the received data here
                except:
                    pass
            ser.flush()
        second_root.after(45,read_serial_data)
        '''serial_thread_4 = threading.Thread(target = read_serial_data, daemon=1)
            serial_thread_4.start()'''
        
    #update receive data function
    def update_rec_data():
        global data
        global Previous_read_serial_data
        disp_value.config(text=data)
        x_textbox1_var.set(data[3:6])
        y_textbox1_var.set(data[9:12])
        x_textbox2_var.set(data[3:6])
        y_textbox2_var.set(data[9:12])
        z_textbox1_var.set(data[13:15])
        track_status()
        #for i in range(10):
         #   temp_var=data[0]
        print(Previous_read_serial_data)
        print(data)
        if Previous_read_serial_data != data:
            textbox2_var.set("OK")
        else:
            textbox2_var.set("No Change")
        
        lb6.after(80,update_rec_data)
        

    #timer
    def update_time():
        string_time = strftime('%H:%M:%S %p')
        lb1.config(text = string_time)
        lb1.after(1000,update_time)
            
    #send data for track enable
    def send_data_1():
        var = ord(ser_data[1])
        var1 = var | 1
        ser_data[1] = chr(var1)
        send_ser_data()

    #send data for track disable
    def send_data_2():
        var = ord(ser_data[1])
        var1 = var & 14
        ser_data[1] = chr(var1)
        send_ser_data()


    #track enable/disable command and status    
    def on_button_click1():       
        if button3.config('text')[-1] == 'Track Enable':
            button3.config(text='Track Disable', fg = 'red')
            '''textbox1.config(state = tk.NORMAL)
            textbox1.delete(0,tk.END)
            textbox1.insert(tk.END,"Track Enabled")          
            textbox1.config(state = tk.DISABLED)'''
            enable_buttons()
            send_data_1()
        else:
            button3.config(text = 'Track Enable', fg = 'green')
            '''textbox1.config(state = tk.NORMAL)
            textbox1.delete(0,tk.END)
            textbox1.insert(tk.END,"Track Disabled")
            textbox1.config(state = tk.DISABLED)'''
            disable_buttons()
            send_data_2()
            
    def enable_buttons():
        for button in buttons:
            button["state"] = "normal"
            retrack_button["state"] = "disabled"

    def disable_buttons():
        for button in buttons:
            button["state"] = "disabled"
        retrack_button["state"] = "disabled"
        search_button["state"] = "disabled"


    #send serial data
    def send_ser_data():
        for i in range(18):
            ser.write(ser_data[i].encode())
        ser.write(new_line.encode())
        
    #different Track algo selection
    def send_data_3():
        var = ord(ser_data[2])
        var1 = var & 0
        var1 = var1 | 0
        ser_data[2] = chr(var1)
        send_ser_data()

    def send_data_4():
        var = ord(ser_data[2])
        var1 = var & 0
        var1 = var1 | 1
        ser_data[2] = chr(var1)
        send_ser_data()

    def send_data_5():
        var = ord(ser_data[2])
        var1 = var & 0
        var1 = var1 | 2
        ser_data[2] = chr(var1)
        send_ser_data()

    def send_data_6():
        var = ord(ser_data[2])
        var1 = var & 0
        var1 = var1 | 3
        ser_data[2] = chr(var1)
        send_ser_data()

    def update_button_text3(option_menu3):
        dropdown=selected_option3.get()
        if option_menu3=="Corelation":
            send_data_3()
        elif option_menu3=="Centroid":
            send_data_4()
        elif option_menu3=="Dual":
            send_data_5()
        elif option_menu3=="SSIM":
            send_data_6()

    #x and y window slider
    def update_values_x(value):
        value = int(value)
        if 0 <= value < 32:
            x_slider.config(troughcolor = "red")
            x_textbox_var.set(" ")
        elif 32 <= value <= 128:
            x_slider.config(troughcolor = "green")
            x_textbox_var.set(str(value))
        elif 128 < value <= 255:
            x_slider.config(troughcolor = "red")
            x_textbox_var.set("")
        value = int(value/8)* 8
        if value <= 32:
            value = int(32)
        if value > 128:
            value = int(128)
        var1 = int(value)
        #print(var1)
        var1 = int(var1/100) #x
        var2 = int(value)
        var2 = int(var2/10)
        var2 = int(var2%10) #y
        var3 = int(value)
        var3 = int(var3%10) #z
        
        ser_data[4] = chr(var1)
        ser_data[5] = chr(var2)
        ser_data[6] = chr(var3)
        send_ser_data()
            
    def update_values_y(value):
        value = int(value)
        if 0 <= value < 32:
            y_slider.config(troughcolor = "red")
            y_textbox_var.set(" ")
        elif 32 <= value <= 128:
            y_slider.config(troughcolor = "green")
            y_textbox_var.set(str(value))
        elif 128 < value <= 255:
            y_slider.config(troughcolor = "red")
            y_textbox_var.set("")
        value = int(value/8)* 8
        if value <= 32:
            value = int(32)
        if value > 128:
            value = int(128)
        var1 = int(value)
        var1 = int(var1/100) #x
        var2 = int(value)
        var2 = int(var2/10)
        var2 = int(var2%10) #y
        var3 = int(value)
        var3 = int(var3%10) #z
        ser_data[7] = chr(var1)
        ser_data[8] = chr(var2)
        ser_data[9] = chr(var3)
        send_ser_data()
       
        
    #different track modes
    def data_default():
        var = ord(ser_data[3])
        var1 = var & 0
        var1 = var1 | 3
        ser_data[3] = chr(var1)
        send_ser_data()
        
    def send_data_7():
        var = ord(ser_data[3])
        var1 = var & 0
        var1 = var1 | 5
        ser_data[3] = chr(var1)
        send_ser_data()

    def send_data_8():
        var = ord(ser_data[3])
        var1 = var & 0
        var1 = var1 | 6
        ser_data[3] = chr(var1)
        send_ser_data()

    def send_data_9():
        var = ord(ser_data[3])
        var1 = var & 0
        var1 = var1 | 7
        ser_data[3] = chr(var1)
        send_ser_data()

    def send_data_10():
        var = ord(ser_data[3])
        var1 = var & 0
        var1 = var1 | 8
        ser_data[3] = chr(var1)
        send_ser_data()

    #track mode command
    def update_text(button_name):
        if entry_var.get() == button_name:
            send_data_default()
            entry_var.set("Normal track")
            enable_buttons()
        else:
             entry_var.set(button_name)
             for button in buttons :
                if button['text'] != button_name:
                    button["state"] = "disable"
                else:
                    button["state"] = "normal"
                    if button_name == "retrack":
                        search_button['state'] = "normal"
                    if button_name == "search":
                         retrack_button['state'] = "normal"
                         search_button['state'] = "disabled"
        if button_name == 'offset':
            send_data_7()
        elif button_name == 'adjust':
            send_data_8()
        elif button_name == 'retrack':
            send_data_9()
        elif button_name == 'search':
            send_data_10()

    #track mode status
    def clear_text():
        entry_var.set("Normal Track")

    #mini joystick
    class Minijoystickapp:
        def __init__(self,master):
            self.master=master
            lbl0 = Label(second_root,text = "")
            lbl0.grid()
            lbl0 = Label(second_root,text = "Track Window position ",font = ('calibri',11))
            lbl0.grid(column = 0,row = 10,padx = 5,pady = 5,sticky="w")
            self.canvas = tk.Canvas(master,width = 100,height = 100,bg = "white")
            self.canvas.grid(row = 10,column = 1,sticky="w")
            self.outer_radius = 45
            self.inner_radius = 10
            self.outer_center = (50,50)
            self.inner_center = (50,50)
            self.outer_circle = self.canvas.create_oval(self.outer_center[0] - self.outer_radius,self.outer_center[1] - self.outer_radius,
                                                      self.outer_center[0] + self.outer_radius,self.outer_center[1] + self.outer_radius,outline = "black")
            self.inner_circle=self.canvas.create_oval(self.inner_center[0] - self.inner_radius,self.inner_center[1] - self.inner_radius,
                                                      self.inner_center[0] + self.inner_radius,self.inner_center[1] + self.inner_radius,outline = "black",fill="red")
            self.canvas.tag_bind(self.inner_circle,"<ButtonPress-1>",self.on_click)
            self.canvas.tag_bind(self.inner_circle,"<B1-Motion>",self.on_drag)
            self.canvas.tag_bind(self.inner_circle,"<ButtonRelease-1>",self.on_release)
        def on_click(self,event):
            self.is_dragging = True
        def on_drag(self,event):
            if self.is_dragging:
                x = event.x-self.outer_center[0]
                y = event.y-self.outer_center[1]
                distance=math.sqrt((x)**2+(y)**2)
                if distance <= self.outer_radius:
                    scaled_x = int((x/self.outer_radius)*255)
                    var = int(scaled_x)
                    if var < 0:
                        var = - (var)
                        ser_data[10] = chr(45)
                        var1 = int(var)
                        var1 = int(var1/100) #x
                        var2 = int(var)
                        var2 = int(var2/10)
                        var2 = int(var2%10) #y
                        var3 = int(var)
                        var3 = int(var3%10) #z
                    else:
                        ser_data[10] = chr(43)
                        var1 = int(var)
                        var1 = int(var1/100) #x
                        var2 = int(var)
                        var2 = int(var2/10)
                        var2 = int(var2%10) #y
                        var3 = int(var)
                        var3 = int(var3%10) #z
                    ser_data[11] = chr(var1)
                    ser_data[12] = chr(var2)
                    ser_data[13] = chr(var3)
                    send_ser_data()
                    scaled_y=int((-y/self.outer_radius)*255)
                    var4 = int(scaled_y)
                    if var4 < 0:
                        var4 = - (var4)
                        ser_data[14] = chr(45)
                        var5 = int(var4)
                        var5 = int(var5/100) #x
                        var6 = int(var4)
                        var6 = int(var6/10)
                        var6 = int(var6%10) #y
                        var7 = int(var4)
                        var7 = int(var7%10) #z
                    else:
                        ser_data[14] = chr(43)
                        var5 = int(var4)
                        var5 = int(var5/100) #x
                        var6 = int(var4)
                        var6 = int(var6/10)
                        var6 = int(var6%10) #y
                        var7 = int(var4)
                        var7 = int(var7%10) #z
                    ser_data[15] = chr(var5)
                    ser_data[16] = chr(var6)
                    ser_data[17] = chr(var7)
                    send_ser_data()
                    print('x:',scaled_x,'y:',scaled_y)
                    self.inner_center = (x+self.outer_center[0],y + self.outer_center[1])
                    self.canvas.coords(self.inner_circle,self.inner_center[0] - self.inner_radius,self.inner_center[1] - self.inner_radius,self.inner_center[0]+self.inner_radius,self.inner_center[1]+self.inner_radius)
        def on_release(self,event):
            self.is_dragging = False
            self.inner_center = self.outer_center
            self.canvas.coords(self.inner_circle,self.outer_center[0] - self.inner_radius,self.outer_center[1] - self.inner_radius,self.outer_center[0] + self.inner_radius,self.outer_center[1] + self.inner_radius)
            ser_data[11] = chr(0)
            ser_data[12] = chr(0)
            ser_data[13] = chr(0)
            ser_data[15] = chr(0)
            ser_data[16] = chr(0)
            ser_data[17] = chr(0)
            send_ser_data()
    #slider output
    def update_values_x1(value1):
        x_textbox1_var.set(str(value1))
    def update_values_y1(value2):
        y_textbox1_var.set(str(value2))
    def update_values_z1(value3):
        y_textbox1_var.set(str(value3))

    #track status
    def track_status():
        if data[0]==str(0):
            textbox1_var.set("Track Disabled")
        elif data[0]==str(1):
            textbox1_var.set("Track Enabled")
            
            
            
     # main3 (3rd level)       
    
    #data
    new_line = '\r\n'
    ser_data = ['\x01','\x00','\x00','\x08','\x00','\x03','\x02','\x00','\x03','\x02','\x01','\x00','\x00','\x00','\x02','\x00','\x00','\x00','\x02']
    
    #global data
    Previous_read_serial_data = 0
    
    #label for console
    lb1 = tk.Label(second_root,text='Video Tracker Command Unit',font = ('calibri',12,'bold'),fg = 'black')
    lb1.grid(row = 0,column = 1,padx = 5,pady = 5,sticky="nsew")

    #label for console
    lb1 = tk.Label(second_root,text='CVT@April 2024',font =('calibri',7,'bold'),fg = 'black')
    lb1.grid(row = 20,column = 4,padx = 5,pady = 5,sticky="se")
    
    #timer status
    lb1 = tk.Label(second_root,font = ('calibri',11,'bold'),fg = 'black')
    lb1.grid(row = 1,column = 4,padx = 5,pady = 5)
    update_time()
    
    #tracking command
    button3 = tk.Button(second_root,text = 'Track Enable',command = on_button_click1)
    button3.grid(column=1,row=3,padx=5,pady=5,sticky="w")
    '''textbox1=tk.Entry(second_root,width=20,state=tk.DISABLED)
    textbox1.grid(column=1,row=4,padx=5,pady=5,sticky="w")'''
    lb6=Label(second_root,text="")
    lb6.grid()
    lb6=Label(second_root,text='Tracker Command',font='calibri')
    lb6.grid(column=0,row=3,padx=5,pady=5,sticky="w")
    '''lb16=Label(second_root,text="")
    lb16.grid()
    lb16=Label(second_root,text='Tracker Status',font='calibri')
    lb16.grid(column=0,row=4,padx=5,pady=5,sticky="w")'''

    #options for track algorithm
    option3=["Corelation","Centroid","Dual","SSIM"]
    selected_option3=tk.StringVar(second_root)
    selected_option3.set(option3[0])
    lb7= Label(second_root,text = "")
    lb7.grid()
    lb7=tk.Label(second_root,text = "Track Algorithm",font=('calibri',11))
    lb7.grid(column=0,row=6,padx=5,pady=5,sticky="w")
    option_menu3=tk.OptionMenu(second_root,selected_option3,*option3,command=update_button_text3)
    option_menu3.config(width=10)
    option_menu3.grid(column=1,columnspan=1,row=6,padx=5,pady=5,sticky="w")
        
    #slider Track Window Size x
    lb8=tk.Label(second_root,text = "Track Window Size    X",font=('calibri',11))
    lb8.grid(column=0,row=8,padx=5,pady=5,sticky="w")
    x_slider=tk.Scale(second_root,from_= 0,to = 255,orient=tk.HORIZONTAL,command=update_values_x,troughcolor="white")
    x_slider.grid(column=1,row=8,padx=5,pady=5,sticky="w")
    
    #slider Track Window Size y
    lb9=tk.Label(second_root,text = "Track Window Size    Y",font=('calibri',11))
    lb9.grid(column=0,row=9,padx=5,pady=5,sticky="w")
    y_slider=tk.Scale(second_root,from_=0,to=255,orient=tk.HORIZONTAL,command=update_values_y,troughcolor="white")
    y_slider.grid(column=1,row=9,padx=5,pady=5,sticky="w")
    
    #slider Track Window Size x status
    x_textbox_var=tk.StringVar(value="NA")
    x_textbox=tk.Entry(second_root,textvariable=x_textbox_var,state='readonly',width=10)
    x_textbox.grid(column=1,row=8,padx=5,pady=5,sticky="e")
    
    #slider Track Window Size y status
    y_textbox_var=tk.StringVar(value="NA")
    y_textbox=tk.Entry(second_root,textvariable=y_textbox_var,state='readonly',width=10)
    y_textbox.grid(column=1,row=9,padx=5,pady=5,sticky="e")
    x_slider.set(0)
    y_slider.set(0)
    
    #buttons for track modes status
    lbl2 = tk.Label(second_root,text = "Track Modes Status",font=('calibri',11))
    lbl2.grid(column=0,row=14,padx=5,pady=5,sticky="w")
    entry_var=tk.StringVar(value="NA")
    entry = tk.Entry(second_root,width=17,textvariable=entry_var,state=tk.DISABLED)
    entry.grid(row=14,column=1,sticky="w")
    lbl1 = tk.Label(second_root,text = "")
    lbl1.grid()
    lbl1 = tk.Label(second_root,text = "Track Modes",font=('calibri',11))
    lbl1.grid(column=0,row=13,padx=5,pady=5,sticky="w")
        
    #buttons for track modes
    button_name=["offset","adjust","retrack","search"]
    buttons=[]
    for i,name in enumerate(button_name,start=1):
        button=tk.Button(second_root,text=name,command=lambda name=name:update_text(name))
        button.grid(row=13,column=i-1,columnspan=2,padx=5,pady=5)
        buttons.append(button)
        button['state'] = "disabled" 
        if name =='retrack':
            retrack_button = button
            retrack_button['state'] = "disabled" 
        elif name == 'search':
            search_button = button
           
            
    def main():
        app=Minijoystickapp(second_root)
        
             
    if __name__=="__main__":
            main()
            
    #slider output
    lb13 = tk.Label(second_root,text = "Error Output",font=('calibri',11))
    lb13.grid(column = 0,row = 16,padx = 5,pady = 5,sticky = "w")
    #label for target
    lb20= tk.Label(second_root,text = "Target",font=('calibri',11))
    lb20.grid(column = 2,row = 16,padx = 5,pady = 5,sticky = "w")
    #slider Target position  x
    lb14 = tk.Label(second_root,text = "Position X",font=('calibri',11))
    lb14.grid(column = 1,row = 17,padx = 5,pady = 5,sticky = "w")
    #slider Target position  y
    lb15 = tk.Label(second_root,text = "Position Y",font=('calibri',11))
    lb15.grid(column = 1,row = 18,padx = 5,pady = 5,sticky = "w")
    #slider Target crosshair  x
    lb14 = tk.Label(second_root,text = "Crosshair X",font=('calibri',11))
    lb14.grid(column = 3,row = 17,padx = 5,pady = 5,sticky = "w")
    #slider Target crosshair y
    lb15 = tk.Label(second_root,text = "Crosshair Y",font=('calibri',11))
    lb15.grid(column = 3,row = 18,padx = 5,pady = 5,sticky = "w")
    #Track Rate
    lb17 = tk.Label(second_root,text = "Track Rate",font=('calibri',11))
    lb17.grid(column = 1,row = 19,padx = 5,pady = 5,sticky = "w")
    #slider Target position x status
    x_textbox1_var = tk.StringVar()
    x_textbox1 = tk.Entry(second_root,textvariable = x_textbox1_var,state = 'readonly',width = 10)
    x_textbox1.grid(column=1,columnspan=3,row = 17,padx = 5,pady = 5)
    #slider Target position  y status
    y_textbox1_var = tk.StringVar()
    y_textbox1 = tk.Entry(second_root,textvariable = y_textbox1_var,state = 'readonly',width = 10)
    y_textbox1.grid(column=1,columnspan=3,row = 18,padx = 5,pady = 5)
    #slider Target crosshair x status
    x_textbox2_var = tk.StringVar()
    x_textbox2 = tk.Entry(second_root,textvariable = x_textbox1_var,state = 'readonly',width = 10)
    x_textbox2.grid(column = 4,row = 17,padx = 5,pady = 5)
    #slider Target crosshair y status
    y_textbox2_var = tk.StringVar()
    y_textbox2 = tk.Entry(second_root,textvariable = y_textbox1_var,state = 'readonly',width = 10)
    y_textbox2.grid(column = 4,row = 18,padx = 5,pady = 5)
    #Track Rate status
    z_textbox1_var = tk.StringVar()
    z_textbox1 = tk.Entry(second_root,textvariable = z_textbox1_var,state = 'readonly',width = 10)
    z_textbox1.grid(column=1,columnspan=3,row = 19,padx = 5,pady = 5)
    #track command status
    lb16=Label(second_root,text="")
    lb16.grid()
    lb16=Label(second_root,text='Tracker Status',font='calibri')
    lb16.grid(column=0,row=4,padx=5,pady=5,sticky="w")
    textbox1_var = tk.StringVar()
    textbox1=tk.Entry(second_root,width=20,textvariable = textbox1_var,state=tk.DISABLED)
    textbox1.grid(column=1,row=4,padx=5,pady=5,sticky="w")
    #COM status
    lb16=Label(second_root,text="")
    lb16.grid()
    lb16=Label(second_root,text='Communication: ',font='calibri')
    lb16.grid(column=0,row=2,padx=5,pady=5,sticky="w")
    textbox2_var = tk.StringVar()
    textbox2=tk.Entry(second_root,width=20,textvariable = textbox2_var,state=tk.DISABLED)
    textbox2.grid(column=1,row=2,padx=5,pady=5,sticky="w")
    disp_value = Label(second_root,text = data,font=('calibri',11),width=22)
    '''#disp_value.grid()
    disp_value.grid(column = 1,row = 5,padx = 5,pady = 5)
    lb6 = Label(second_root,text = "")
    lb6.grid()
    lb6 = Label(second_root,text = 'Received Data',font = 'calibri')
    lb6.grid(column = 0,row = 5,padx = 5,pady = 5,sticky = "w")'''

    


    
    #receive serial data
    #Previous_read_serial_data = data
    serial_thread_1 = threading.Thread(target = read_serial_data, daemon=True)
    serial_thread_1.start()
    serial_thread_2 = threading.Thread(target = update_rec_data, daemon=True)
    serial_thread_2.start()
    #second_root.update()
    second_root.mainloop()
    
    # main3 loop ends here

# Start of the code(main)       
first_root=tk.Tk()
first_root.title('COM Port Selection')
first_root.geometry('400x180')
first_root.resizable(False, False)

#com port selection command
com_port = "COM1"
option1=["COM1","COM2","COM3","COM4"]
#global data
global ser
data = ' X:NA  Y:NA  NA'
ser_Flag=0
selected_option1=tk.StringVar(first_root)
selected_option1.set(option1[0])
lb2= Label(first_root,text = "")
lb2.grid()
lb2=tk.Label(first_root,text = "Select COM port",font='calibri')
lb2.grid(column=0,row=3,padx=5,pady=5)
option_menu1=tk.OptionMenu(first_root,selected_option1,*option1,command=lambda option:update_button_text1(option,textbox,option_menu1))
option_menu1.config(width=5)
option_menu1.grid(column=1,row=3,padx=5,pady=5)

lb3 = Label(first_root,text = "")
lb3.grid()
lb3=tk.Label(first_root,text = "Selected COM port",font='calibri')
lb3.grid(column=0,row=5,padx=5,pady=5)
textbox=tk.Entry(first_root,text=selected_option1,state="readonly",width=7)
textbox.grid(column=1,row=5,padx=5,pady=5)

submit_button2=tk.Button( first_root,text='SUBMIT',command = on_option_selected)
submit_button2.grid()

first_root.mainloop()
serial_close()
