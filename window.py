import tkinter 

window = tkinter.Tk()
window.title("Login Form")
window.geometry('340x440')
window.configure(bg='#333333')

#Creating the widgets
Login_label= tkinter.Label(window, text = "Login",bg='#333333',fg='#FFFFFF')
username_label = tkinter.Label(window, text = "Username",bg='#333333',fg='#FFFFFF')
username_entry = tkinter.Entry(window)
passward_entry = tkinter.Entry(window,show="*")
passward_label = tkinter.Label(window, text = "Passward",bg='#333333',fg='#FFFFFF')
Login_button = tkinter.Button(window,text="Login")
Quit_button = tkinter.Button(window,text="Quit",command = window.quit)


#Placing widgets on the screen
Login_label.grid(row=0, column =0, columnspan=2)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1)
passward_entry.grid(row=2, column=1)
passward_label.grid(row=2, column=0)
Login_button.grid(row=3, column=0, columnspan=2)
Quit_button.grid(row=4, column=0, columnspan=2)
#Quit_button.place(relx= 0.5,rely= 0.5)
##Quit_button.pack(CENTER)
window.mainloop()
