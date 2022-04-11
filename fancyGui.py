from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from importlib import reload
import os

sudoPassword = 'scalp431!'
command = 'xrandr --output HDMI-0 --mode 1920x1080'
#command = 'xrandr --output HDMI-0 --mode 1280x720'
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def SelWkt():
    window.destroy()
    import SelectWorkout
    reload(SelectWorkout)

window = Tk()

window.geometry("1920x1080")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=1080,
    width=1920,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_text(
    960.0,
    220.0,
    anchor="center",
    justify="center",
    text="Enhance Your Lift",
    fill="#000000",
    font=("Audiowide Regular", 48 * -1)
)

canvas.create_text(
    960.0,
    100.0,
    anchor="center",
    text="Smart Lifting",
    fill="#000000",
    font=("Space Grotesk", 144 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: SelWkt(),
    relief="flat"
)
button_1.place(
    x=660.0,
    y=627.0,
    width=600.0,
    height=106.0
)
window.resizable(False, False)
window.mainloop()
