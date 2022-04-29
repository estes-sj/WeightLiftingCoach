from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from importlib import reload
import subprocess
import sys

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
fontStyle = "Consolas"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.attributes('-fullscreen', True)
window.geometry("1920x1080")
window.configure(bg="#FFFFFF")


def Conductwkt():
    window.destroy()
    #import ConductLift
    #reload(ConductLift)
    #running = True
    try:
        #import demo WARNING: import statements cause segments to load prematurely
        #subprocess.run("python3 /home/samjet/WeightLiftingCoach/ConductLift.py & python3 /home/samjet/WeightLiftingCoach/demo.py", shell=True)
        #import ConductLift
        #reload(ConductLift)
        #subprocess.run("python3 demo.py", shell=True)
        subprocess.run("python3 ConductLift.py & python3 demo.py", shell=True)
        sys.exit(exit_code=0)
        # samProgram.main()
    except:
        print("Error, Cannot Run Conduct Lift and Demo") 
        #running = False
    '''
    if running == False:
        try:
            subprocess.run("python3 /home/samjet/WeightLiftingCoach/ConductLift.py & python3 /home/samjet/WeightLiftingCoach/demo.py", shell=True)
        except:
            print("Error")
    if running == False:
        try:
            import ConductLift
            reload(ConductLift)
        except:
            print("Error")
    '''
    #quit() 


def SelWkt():
    #subprocess.run("python3 SelecktWorkout.py", shell=True)
    window.destroy()
    #quit()
    import SelectWorkout
    reload(SelectWorkout)


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
    305.0,
    192.0,
    anchor="nw",
    text="Position the Smart \n"
         "Lifting system about\n"
         "twelve feet away with a\n"
         "clear view of your\n"
         "right side.\n"
         "Adjust the camera as\n"
         "needed to be in frame.\n",
    fill="#FFFFFF",
    font=(fontStyle, 69 * -1)
)

canvas.create_text(
    305.0,
    0.0,
    anchor="nw",
    text="Barbell Back Squat",
    fill="#FFFFFF",
    font=(fontStyle, 144 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("Continue.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Conductwkt(),
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
    command=lambda: SelWkt(),
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
