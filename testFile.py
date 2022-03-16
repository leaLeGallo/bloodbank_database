from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Bloodbank database")
frame = ttk.Frame(root, padding=10)
frame.grid()
ttk.Label(frame, text="Hello World!").grid(column=0, row=0)
ttk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)

root.mainloop()


# Add a Treeview widget
tree = ttk.Treeview(root, column=("donorID","date","quantity","expired"), show='headings', height=5)
tree.column("# 1", anchor=CENTER)
tree.heading("# 1", text="donorID")
tree.column("# 2", anchor=CENTER)
tree.heading("# 2", text="date")
tree.column("# 3", anchor=CENTER)
tree.heading("# 3", text="quantity")
tree.column("# 4", anchor=CENTER)
tree.heading("# 4", text="expired")

# Insert the data in Treeview widget
for row in fetch:
    tree.insert('', 'end', text="1", values=('%s', '%s', '%s', '%s'))

#create the GUI
root = Tk()
root.title("Bloodbank database")
root.geometry("400x250")

ttk.Button(root, text="Quit", command=root.destroy).grid(column=1, row=1)

root.mainloop()