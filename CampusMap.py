# campusmap.py
# Show FSC campus map using tkinter.

import tkinter as tk
from PIL import ImageTk, Image
import os
from scipy import spatial
import sys
import tkinter.messagebox

IMAGEROOT = os.getcwd()
IMAGEFILE = 'fsc_campus_map.png'

def main():
    # Create main window of application
    gui = tk.Tk()
    gui.title("FSC Campus Map")
    gui.configure(background='grey')

    # Create global lists with names and with coordinates
    global names, coordinates, img, panel
    names = ['Barnett Athletic Complex', 'Badcock Memorial Garden',
        'Mr. George\'s Green', 'Water Dome',
        'Dell Hall','Hollis Hall','Miller Hall',
        'Allan Spivey Hall','Joseph Reynolds Hall',
        'Wesley Hall','Nicholas Hall',
        'Buck Stop Grill (Pizza)','Happy Place','The Caf','Greenhouse',
        'President\'s Residence','George W. Jenkins Field House',
        'Fannin Center','Ruel B. Gilbert Gymnasium',
        'Campus Safety and Security','Edge Hall','Jack M. Berry Citrus Building']
    coordinates = [(512, 113),(407, 183),(540, 261),
        (221, 165),(722, 209),(717, 159),(700, 182),
        (466, 264),(398, 262),(443, 402),(527, 389),
        (382, 208),(832, 273),(639, 275),(386, 337),
        (317, 409),(504, 196),(452, 187),(560, 175),
        (626, 159),(459, 335),(510, 308)]

    # Checks that the length of both lists are equal and stops program if not
    if (len(names) == len(coordinates)):
        print("All good!")
    else:
        print("Something\'s off...")
        sys. exit()
    
    # Create tkinter-compatible photo image
    imgfile = os.path.join(os.path.expanduser(IMAGEROOT), IMAGEFILE)
    img = ImageTk.PhotoImage(Image.open(imgfile))

    # Create and pack Label with image
    panel = tk.Label(gui, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")

    # # (RECORD) Add callback function for cursor motion (track cursor coordinates in terminal)
    # gui.bind('<Motion>', motion)

    # Add callback function for cursor motion
    gui.bind("<Button 1>",getorigin)

    # Start the GUI
    gui.mainloop()

# (WORK) Displays the name of the location in a new window
def click(name):
    w = tk.Label(panel, text=name, image=img, compound='center')
    w.pack()
    #tkinter.messagebox.showinfo("FSC Campus Map", name)

# (WORK) After click, Finds closest coordinates in the list and returns name of location
def getorigin(event):
    x = event.x
    y = event.y
    tree = spatial.KDTree(coordinates)
    index = str((tree.query([(x,y)]))[1])
    if (len(index) == 3):
        #print(names[int(index[1])])
        click(names[int(index[1])])
    else:
        #print(names[int(index[1:3])])
        click(names[int(index[1:3])])

# # (RECORD) Track cursor coordinates in terminal
# def motion(event):
#     x, y = event.x, event.y
#     print('({}, {})'.format(x, y))

# # (RECORD) After you click, it asks for name as an input and prints it to an output file
# def getorigin(event):
#     x = event.x
#     y = event.y
#     f = open("output.txt", "a")
#     name = input('Enter name: ')
#     print('\'', name, '\' ', '({}, {})'.format(x, y), file=f, sep="")
#     f.close()

if __name__ == '__main__':
    main()