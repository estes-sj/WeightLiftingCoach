from importlib import reload
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import json
from venv import create
import create_xml
import os
#import subprocess

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
fontStyle = "Consolas"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Get final result information 0 = score, 1 = feedback
try:
    final_results = create_xml.getFinalResults()
except:
    final_results = ["0", "No Squat Detected. Please try again.\nMake sure that you are positioned far enough away\nso that you are fully in frame of the camera.\nHowever, being too far away may impair results.\nThe camera is adjustable.\nHalf squats will result in a score of 0.\nMake sure to let the live video load."]
    print("No final results found")

def goHome():
    cleanup(1)
    #subprocess.run("python3 StartPage.py", shell=True)
    window.destroy()
    import StartPage
    reload(StartPage)

def NextSet():
    cleanup(2)
    #subprocess.run("python3 PositionSystem.py", shell=True)
    window.destroy()
    #quit()
    import PositionSystem
    reload(PositionSystem)

def cleanup(choice):
    try:
        os.system("pkill -f demo.py")
        os.system("pkill -f ConductLift.py")
        os.system("pkill -f PositionSystem.py")
        os.system("pkill -f SelectWorkout.py")
        os.system("pkill -f StartPage.py")
    except:
        print("No process demo/conduct/pos/selwkt/stpg to kill")

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
canvas.create_text(
    102.0,
    210.0,
    anchor="nw",
    text="Final Score: ",
    fill="#FFFFFF",
    font=(fontStyle, 69 * -1)
)

canvas.create_text(
    102.0,
    393.0,
    anchor="nw",
    text="Comments:",
    fill="#FFFFFF",
    font=(fontStyle, 69 * -1)
)

canvas.create_text(
    554.0,
    210.0,
    anchor="nw",
    # Final Score will go here
    text="   " + str("{:.2f}".format(float(final_results[0]))) + "%",
    fill="#FFFFFF",
    font=(fontStyle, 69 * -1)
)

canvas.create_text(
    554.0,
    393.0,
    anchor="nw",
    # Comments will go here!
    text=final_results[1],
    fill="#FFFFFF",
    font=(fontStyle, 30 * -1)
)

canvas.create_text(
    295.0,
    0.0,
    anchor="nw",
    text="Barbell Back Squat",
    fill="#FFFFFF",
    font=(fontStyle, 144 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("NextSet.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: NextSet(),
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
    command=lambda: goHome(),
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
