from tkinter import *
root = Tk()
e=Entry(root)
e.pack()

def myclick():
    myLabel = Label(root, text='Hello ' + e.get() )
    myLabel.pack()

myButton = Button(root, text ="Enter your name:", command=myclick)
myButton.pack()


root.mainloop()
