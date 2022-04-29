from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from mimetypes import init
import tkinter as tk
import matplotlib
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from importlib import reload
import os

from numpy import size
import create_xml
import xml.dom.minidom as minidom
import matplotlib.pyplot as plt

from matplotlib.figure import Figure

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def goHome():
    cleanup(1)
    # subprocess.run("python3 StartPage.py", shell=True)
    window.destroy()
    import SelectWorkout
    reload(SelectWorkout)


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

window.geometry("1920x1080")
window.configure(bg="#FFFFFF")
list_of_files = create_xml.previous_lift_files()
print(list_of_files)
recent0 = minidom.parse(list_of_files[0])
recent1 = minidom.parse(list_of_files[1])
recent2 = minidom.parse(list_of_files[2])
recent3 = minidom.parse(list_of_files[3])
recent4 = minidom.parse(list_of_files[4])
recent5 = minidom.parse(list_of_files[5])
recent6 = minidom.parse(list_of_files[6])

final_score0 = float(recent0.getElementsByTagName("final_score")[0].childNodes[0].nodeValue)
final_score1 = float(recent1.getElementsByTagName("final_score")[0].childNodes[0].nodeValue)
final_score2 = float(recent2.getElementsByTagName("final_score")[0].childNodes[0].nodeValue)
final_score3 = float(recent3.getElementsByTagName("final_score")[0].childNodes[0].nodeValue)
final_score4 = float(recent4.getElementsByTagName("final_score")[0].childNodes[0].nodeValue)
final_score5 = float(recent5.getElementsByTagName("final_score")[0].childNodes[0].nodeValue)
final_score6 = float(recent6.getElementsByTagName("final_score")[0].childNodes[0].nodeValue)

# get date from data

date0 = str(recent0.getElementsByTagName("date")[0].childNodes[0].nodeValue)
date1 = str(recent1.getElementsByTagName("date")[0].childNodes[0].nodeValue)
date2 = str(recent2.getElementsByTagName("date")[0].childNodes[0].nodeValue)
date3 = str(recent3.getElementsByTagName("date")[0].childNodes[0].nodeValue)
date4 = str(recent4.getElementsByTagName("date")[0].childNodes[0].nodeValue)
date5 = str(recent5.getElementsByTagName("date")[0].childNodes[0].nodeValue)
date6 = str(recent6.getElementsByTagName("date")[0].childNodes[0].nodeValue)

xpoints = [date0, date1, date2, date3, date4, date5, date6]
ypoints = [final_score0, final_score1, final_score2, final_score3, final_score4, final_score5, final_score6]

figure = Figure((6, 4), dpi=100)
axes = figure.add_subplot()
axes.plot(xpoints, ypoints)
plt.figure(figsize=(14, 11))
plt.plot(xpoints, ypoints)
plt.savefig('graph.png')
the_graph = PhotoImage(file='graph.png')

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
    0.0,
    anchor="nw",
    text="Insights Graph",
    fill="#FFFFFF",
    font=("Space Grotesk", 144 * -1)
)

button_1 = Button(
    image=the_graph,
    relief="flat",
    command=lambda: goHome()
)
button_1.place(
    x=250.0,
    y=10.0,
    width=the_graph.width(),
    height=the_graph.height()
)

window.resizable(False, False)
window.mainloop()
