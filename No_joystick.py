import tkinter as tk

class Joystick:
    def __init__(self, master):
        self.master = master
        self.x = self.master.winfo_screenwidth() // 2
        self.y = self.master.winfo_screenheight() // 2
        self.radius = 50
        self.base_color = "gray"
        self.stick_color = "red"

        self.canvas = tk.Canvas(master, width=2*self.radius, height=2*self.radius)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.__on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.__on_canvas_drag)

        self.draw_joystick()

    def __on_canvas_click(self, event):
        self.x = event.x
        print(self.x)
        self.y = event.y
        self.canvas.delete("all")  # Clear previous drawing
        self.draw_joystick()

    def __on_canvas_drag(self, event):
        self.x = event.x
        self.y = event.y
        print(self.x,self.y)
        self.canvas.delete("all")  # Clear previous drawing
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
        stick_center_x = center_x + self.x - center_x
        stick_center_y = center_y + self.y - center_y

        self.canvas.create_oval(
            stick_center_x - self.radius // 3,
            stick_center_y - self.radius // 3,
            stick_center_x + self.radius // 3,
            stick_center_y + self.radius // 3,
            fill=self.stick_color,
        )

root = tk.Tk()
root.title("Joystick")
root.title("Joystick")
root.geometry("340x440")
joystick = Joystick(root)
#joystick.pack()
root.mainloop()
