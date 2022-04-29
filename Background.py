from tkinter import Tk, Canvas


window = Tk()

window.attributes('-fullscreen', True)
window.geometry("1920x1080")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#264653",
    height=1080,
    width=1920,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
window.resizable(False, False)
window.mainloop()
