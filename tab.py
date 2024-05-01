from tkinter import *
root = Tk()
root.minsize(height=500,width= 900)
def tab1():
    def tab2():
        lb1.destroy()
        btn1.destroy()
        lb2 = Label(root, text ="this is second Tab",font=('arial',16))
        lb2.pack()
        def back():
            lb2.destroy()
            btn2.destroy()
            tab1()
        btn2=Button(root,text='BACK',
                    font=('arial',16),command =back)
        btn2.pack(side = BOTTOM)
        btn3=Button(root,text='CLOSE',
                    font=('arial',16),command =root.destroy)
        btn3.pack(side = BOTTOM)

    lb1 = Label(root, text ="this is firtst Tab",font=('arial',16))
    lb1.pack()
    btn1=Button(root,text='NEXT',font=('arial',16),command=tab2)
    btn1.pack(side = BOTTOM)
tab1()
root.mainloop()
