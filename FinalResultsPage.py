from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import json
from typing import final

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
fontStyle = "Consolas"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Method to obtain final results as an array
def final_results_log():

    phrase = "###############################"
    line_number = "Log does not exist..."
    log_file = open("logs\log_squat6.log","r")

    # Find where final results are
    for number, line in enumerate(log_file):
        if phrase in line:
            line_number = number
            break

    contents = log_file.readlines()

    # Store final results in array
    final_results = contents[line_number+1:line_number+4]

    log_file.close()

    return final_results

final_results = final_results_log

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
    102.0,
    210.0,
    anchor="nw",
    text="Final Score:",
    fill="#000000",
    font=(fontStyle, 69 * -1)
)

canvas.create_text(
    102.0,
    393.0,
    anchor="nw",
    text="Comments:",
    fill="#000000",
    font=(fontStyle, 69 * -1)
)

canvas.create_text(
    554.0,
    210.0,
    anchor="nw",
    # Final Score will go here
    text=str(final_results[2]),
    fill="#000000",
    font=(fontStyle, 69 * -1)
)

canvas.create_text(
    554.0,
    393.0,
    anchor="nw",
    # Comments will go here!
    text=str(final_results[0:1]),
    fill="#000000",
    font=(fontStyle, 69 * -1)
)

canvas.create_text(
    305.0,
    0.0,
    anchor="nw",
    text="Barbell Back Squat",
    fill="#000000",
    font=("Space Grotesk", 144 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("NextSet.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=1083.0,
    y=881.0,
    width=600.0,
    height=106.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("GoHome.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=236.0,
    y=881.0,
    width=600.0,
    height=106.0
)
window.resizable(False, False)
window.mainloop()
