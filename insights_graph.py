""" 

important notes and tips for making graph
    x-axis = date
    y-axis = score

makeing graph help aids
https://www.w3schools.com/python/matplotlib_plotting.asp


do everything within line 72 (data = {) to line 98 (axes.set_ylabel)

finds the most recent squat data file
    = create_xml.newest_file()

returns the list of the most recent 7 files as an array
   list_of_files = create_xml.previous_lift_files()
   list_of_files[0] = newest file
   [6] = oldesr
returns as a list of strings with index 3 being the newest file and index 6 being the oldest file

to access the final_score value from the xml file
    #get the xml file and parse it
    file = minidom.parse(list_of_files[3 or whatever number])
    #get the final_score value

    final_score = list_of_files[3 or whatver number].getElementsByTagName( "final_score" )[ 3 ].childNodes[ 3 ].nodeValue

to access the date value from the xml file
    #get the xml file and parse it if you havn't already
    file = minidom.parse(path_of_file)
    #get the date value
    date0 = file.getElementsByTagName( "date" )[ 0 ].childNodes[ 0 ].nodeValue

"""


from mimetypes import init
import tkinter as tk
import matplotlib
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from importlib import reload

from numpy import size
import create_xml
import xml.dom.minidom as minidom
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
fontStyle = "Consolas"


class App(tk.Tk):
    '''
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def PrevWkts():
        App.destroy()
        import PreviousLiftVideos
        reload(PreviousLiftVideos)
    '''
    def __init__(self):
        super().__init__()
        self.title('Fuck')
    # prepare data
        list_of_files = create_xml.previous_lift_files()
        print(list_of_files[3])
        recent0 = minidom.parse(list_of_files[0])
        recent1 = minidom.parse(list_of_files[1])
        recent2 = minidom.parse(list_of_files[2])
        recent3 = minidom.parse(list_of_files[3])
        recent4 = minidom.parse(list_of_files[4])
        recent5 = minidom.parse(list_of_files[5])
        recent6 = minidom.parse(list_of_files[6])


        final_score0 = float(recent0.getElementsByTagName( "final_score" )[0 ].childNodes[ 0].nodeValue)
        final_score1 = float(recent1.getElementsByTagName( "final_score" )[ 0].childNodes[ 0].nodeValue)
        final_score2 = float(recent2.getElementsByTagName( "final_score" )[ 0 ].childNodes[ 0 ].nodeValue)
        final_score3 = float(recent3.getElementsByTagName( "final_score" )[ 0 ].childNodes[ 0 ].nodeValue)
        final_score4 = float(recent4.getElementsByTagName( "final_score" )[ 0 ].childNodes[ 0 ].nodeValue)
        final_score5 = float(recent5.getElementsByTagName( "final_score" )[ 0 ].childNodes[ 0 ].nodeValue)
        final_score6 = float(recent6.getElementsByTagName( "final_score" )[ 0 ].childNodes[ 0 ].nodeValue)
        
        #get date from data 
    
        date0 = str(recent0.getElementsByTagName( "date" )[ 0 ].childNodes[ 0 ].nodeValue)
        date1 = str(recent1.getElementsByTagName( "date" )[ 0 ].childNodes[ 0 ].nodeValue)
        date2 = str(recent2.getElementsByTagName( "date" )[ 0 ].childNodes[ 0 ].nodeValue)
        date3 = str(recent3.getElementsByTagName( "date" )[ 0 ].childNodes[ 0 ].nodeValue)
        date4 = str(recent4.getElementsByTagName( "date" )[ 0 ].childNodes[ 0 ].nodeValue)
        date5 = str(recent5.getElementsByTagName( "date" )[ 0 ].childNodes[ 0 ].nodeValue)
        date6 = str(recent6.getElementsByTagName( "date" )[ 0 ].childNodes[ 0 ].nodeValue)
        

        xpoints= [date0,date1,date2, date3, date4, date5, date6]
        ypoints= [final_score0,final_score1, final_score2, final_score3, final_score4, final_score5,final_score6 ]

        figure = Figure((6, 4), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self)
        axes = figure.add_subplot()
        axes.plot(xpoints, ypoints)
        self.attributes('-fullscreen', True)
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = 1)
        # create the plot
        # plt.figure(figsize=(6.074, 3.3905), dpi = 96)
        # plt.plot(xpoints,ypoints)

        # plt.show()
        # plt.set_title('Best Score Recap')
        # plt.set_xlabel('Date and Time')
        # plt.set_ylabel('Score (%)')

'''
        button_image_7 = PhotoImage(
            file=relative_to_assets("Back.png"))
        button_7 = Button(
            image=button_image_7,
            borderwidth=3,
            highlightthickness=3,
            command=lambda: PrevWkts(),
            relief="flat"
        )
        button_7.place(
            x=41.3,
            y=43.3,
            width=214.3,
            height=99.3
        )
'''
if __name__ == '__main__':
    app = App()
    app.mainloop()