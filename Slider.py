from tkinter import *
def select():
    sel ="value ="+str(v.get())
    label.config(text = sel)
top = Tk()
top.geometry("300x300")
v = DoubleVar()
scale = Scale(top, variable = v, from_ = 1, to = 100,
              orient = HORIZONTAL)
scale.pack(anchor = CENTER)
btn = Button(top, text = "value", command  = select)
btn.pack(anchor = CENTER)
label = Label(top)
label.pack()

mainloop()


