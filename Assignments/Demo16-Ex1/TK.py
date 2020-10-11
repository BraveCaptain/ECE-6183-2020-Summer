import tkinter as tk

def fun():
    print('Stay healthy')

root = tk.Tk()

L = tk.Label(root, text = 'Stay healthy')
L.pack()

b = tk.Button(root, text = 'Press', command = fun)
b.pack()

e = tk.Entry(root)
e.pack()

s = tk.Scale(root)
s.pack()

c = tk.Checkbutton(root, text="Expand", variable="Health")
c.pack()

root.mainloop()
