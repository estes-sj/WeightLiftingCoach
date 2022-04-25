from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from importlib import reload
import glob
import os
from venv import create
import create_xml
import subprocess

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
fontStyle = "Consolas"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.attributes('-fullscreen', True)
window.geometry("1920x1080")
window.configure(bg="#FFFFFF")

# Get list of most recent files where 0 = newest file
latest_file_list = create_xml.previous_lift_files()

# Send file information
def find_previous_lift():
    return

def SelWkt():
    #subprocess.run("python3 SelectWorkout.py", shell=True)
    window.destroy()
    #quit()
    import SelectWorkout
    reload(SelectWorkout)


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
    430.0,
    30.0,
    anchor="nw",
    text="Previous Workouts",
    fill="#000000",
    font=(fontStyle, 114 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("PrevLift1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=175.0,
    y=222.0,
    width=273.0,
    height=321.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("PrevLift2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=823.0,
    y=222.0,
    width=273.0,
    height=321.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("PrevLift3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=1471.0,
    y=223.0,
    width=273.0,
    height=321.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("PrevLift4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=175.0,
    y=648.0,
    width=273.0,
    height=321.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("PrevLift5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=823.0,
    y=648.0,
    width=273.0,
    height=321.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("PrevLift6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=1471.0,
    y=648.0,
    width=273.0,
    height=321.0
)


button_image_7 = PhotoImage(
    file=relative_to_assets("Back.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: SelWkt(),
    relief="flat"
)
button_7.place(
    x=41.0,
    y=43.0,
    width=214.0,
    height=99.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("graph.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: SelWkt(),
    relief="flat"
)
button_8.place(
    x=1650.0,
    y=43.0,
    width=214.0,
    height=99.0
)
window.resizable(False, False)
window.mainloop()
