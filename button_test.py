import tkinter as tk

root = tk.Tk()

root.title("info title")

tk.Label(root, text="This is the pop up message").pack()

root.after(5000, root.destroy())

root.mainloop()

