import tkinter as tk

window = tk.Tk()
window.title("111")
window.geometry("1500x1000")

text_var = tk.StringVar()

label = tk.Label(window, bg="green", textvariable=text_var, width=20, height=1)
label.pack()

hit_on = False


def hit_button():
    global hit_on
    if hit_on:
        text_var.set("")
        hit_on = False
    else:
        text_var.set("you hit the button")
        hit_on = True


button = tk.Button(window, text="hit me", width=10, height=2, command=hit_button)
button.pack()

window.mainloop()
