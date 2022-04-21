""" 

important notes and tips for making graph
    x-axis = date
    y-axis = score

makeing graph help aids
https://www.w3schools.com/python/matplotlib_plotting.asp

make sure you install matplotlib
    pip install matplotlib

do everything within line 72 (data = {) to line 98 (axes.set_ylabel)

finds the most recent squat data file
    = create_xml.newest_file()

returns the list of the most recent 7 files
    = create_xml.previous_lift_files()
returns as a list of strings with index 0 being the newest file and index 6 being the oldest file

to access the final_score value from the xml file
    #get the xml file and parse it
    file = minidom.parse(path_of_file)
    #get the final_score value
    final_score = file.getElementsByTagName( "final_score" )[ 0 ].childNodes[ 0 ].nodeValue

to access the date value from the xml file
    #get the xml file and parse it if you havn't already
    file = minidom.parse(path_of_file)
    #get the date value
    date = file.getElementsByTagName( "date" )[ 0 ].childNodes[ 0 ].nodeValue

"""




import tkinter as tk
import matplotlib
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from importlib import reload
import create_xml

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
fontStyle = "Consolas"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def PrevWkts():
    App.destroy()
    import PreviousLiftVideos
    reload(PreviousLiftVideos)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry("1920x1080")
        self.configure(bg="#FFFFFF")
        self.title('Previous Squat Scores')

        # prepare data
        data = {
            'Python': 11.27,
            'C': 11.16,
            'Java': 10.46,
            'C++': 7.5,
            'C#': 5.26
        }
        languages = data.keys()
        popularity = data.values()

        # create a figure
        figure = Figure(figsize=(6, 4), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, self)

        # create axes
        axes = figure.add_subplot()

        # create the barchart
        axes.bar(languages, popularity)
        axes.set_title('Top 5 Programming Languages')
        axes.set_xlabel('Date and Time')
        axes.set_ylabel('Score (%)')

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        button_image_7 = PhotoImage(
            file=relative_to_assets("Back.png"))
        button_7 = Button(
            image=button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: PrevWkts(),
            relief="flat"
        )
        button_7.place(
            x=41.0,
            y=43.0,
            width=214.0,
            height=99.0
        )

if __name__ == '__main__':
    app = App()
    app.mainloop()