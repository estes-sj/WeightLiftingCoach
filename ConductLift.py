from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from importlib import reload
import os
#import subprocess

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
fontStyle = "Consolas"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def FinRes():
    #bad_exit = True
    try: 
        os.system("pkill -f demo.py")
    except:
        #bad_exit = False
        print("No process demo to kill")
    '''
    if bad_exit == False:
        try:
            os.system("pkill -f /home/samjet/WeightLiftingCoach/demo.py")
        except:
            print("Error")
    '''
    #subprocess.run("python3 FinalResultsPage.py", shell=True)
    window.destroy()
    #quit()
    import FinalResultsPage
    reload(FinalResultsPage)

# Possible bugs?
def PosSys():
    #subprocess.run("python3 PositionSystem.py", shell=True)
    window.destroy()
    #quit()
    import PositionSystem
    reload(PositionSystem)


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
    385.0,
    192.0,
    anchor="nw",
    text="Wait approximately 15 seconds\n"
         "for the camera live video to \n"
         "load.\nThen perform 3 squats.\n"
         "Do not click the button until\n"
         "you are done lifting.",
    fill="#FFFFFF",
    font=(fontStyle, 69 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("SetComplete.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: FinRes(),
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
    command=lambda: PosSys(),
    relief="flat"
)
button_2.place(
    x=41.0,
    y=43.0,
    width=214.0,
    height=99.0
)

window.resizable(False, False)
window.mainloop()
