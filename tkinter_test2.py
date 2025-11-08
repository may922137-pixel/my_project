import tkinter as tk

window = tk.Tk()
window.title("text")
window.geometry("200x200")

entry = tk.Entry(window)

entry.pack()

text = tk.Text(window, height=2)

text.pack()


def insert_point():
    var = entry.get()
    text.insert("insert", var)


def insert_end():
    var = entry.get()
    text.insert("end", var)


button1 = tk.Button(window, text="insert point", command=insert_point)
button2 = tk.Button(window, text="insert end", command=insert_end)

button1.pack()
button2.pack()

window.mainloop()
