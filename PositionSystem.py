from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
fontStyle = "Consolas"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


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
    305.0,
    192.0,
    anchor="nw",
    text="Position the Smart \n"
         "Lifting system about\n"
         "six feet away with a\n"
         "clear view of your\n"
         "side.",
    fill="#000000",
    font=(fontStyle, 69 * -1)
)

canvas.create_text(
    305.0,
    0.0,
    anchor="nw",
    text="Barbell Back Squat",
    fill="#000000",
    font=(fontStyle, 144 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("Continue.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=660.0,
    y=920.0,
    width=600.0,
    height=106.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("Back.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=41.0,
    y=43.0,
    width=214.0,
    height=99.0
)
img = PhotoImage(
    file=relative_to_assets("SideView.png"))
canvas.create_image(1388.0, 539.5, image=img)
window.resizable(False, False)
window.mainloop()
