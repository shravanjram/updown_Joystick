import tkinter as tk
import serial

# Serial port configuration (modify these values for your setup)
port = 'COM3'  # Replace with your port name (e.g., '/dev/ttyUSB0' for Linux/Mac)
baudrate = 9600

# Data format to send (modify based on your receiving program)
axis_sep = ','  # Separator between axis values
data_end = '\n'  # Character to mark end of data

# Initialize serial connection
try:
    ser = serial.Serial(port, baudrate)
except serial.SerialException as e:
    print(f"Error connecting to serial port: {e}")
    exit()


class Joystick:
    def __canvas_click(self, event):
        self.x = event.x
        self.y = event.y
        self.canvas.delete("all")
        self.draw_joystick()

    def __canvas_drag(self, event):
        self.x = event.x
        self.y = event.y
        self.canvas.delete("all")
        self.draw_joystick()
        self.send_data()

    def __init__(self, master):
        self.master = master
        self.x = self.master.winfo_screenwidth() // 2
        self.y = self.master.winfo_screenheight() // 2
        self.radius = 50
        self.base_color = "gray"
        self.stick_color = "red"

        self.canvas = tk.Canvas(master, width=2*self.radius, height=2*self.radius)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.__canvas_click)
        self.canvas.bind("<B1-Motion>", self.__canvas_drag)

        self.draw_joystick()

    def draw_joystick(self):
        center_x = self.canvas.winfo_width() // 2
        center_y = self.canvas.winfo_height() // 2

        # Draw base circle
        self.canvas.create_oval(
            center_x - self.radius,
            center_y - self.radius,
            center_x + self.radius,
            center_y + self.radius,
            fill=self.base_color,
        )

        # Draw stick relative to click position
        stick_center_x = center_x + min(max(self.x - center_x, -self.radius), self.radius)
        stick_center_y = center_y + min(max(self.y - center_y, -self.radius), self.radius)

        self.canvas.create_oval(
            stick_center_x - self.radius // 3,
            stick_center_y - self.radius // 3,
            stick_center_x + self.radius // 3,
            stick_center_y + self.radius // 3,
            fill=self.stick_color,
        )

    def send_data(self):
        center_x = self.canvas.winfo_width() // 2
        center_y = self.canvas.winfo_height() // 2

        # Normalize values to -1 to 1 range
        x_axis = (self.x - center_x) / self.radius
        y_axis = (self.y - center_y) / self.radius

        # Send data string (modify based on your receiving program)
        data_string = f"{x_axis}{axis_sep}{y_axis}{data_end}"
        try:
            ser.write(data_string.encode())
        except serial.SerialException as e:
            print(f"Error sending data: {e}")


root = tk.Tk()
root.title("Joystick")
joystick = Joystick(root)
root.mainloop()

# Close serial connection on exit
ser.close()
