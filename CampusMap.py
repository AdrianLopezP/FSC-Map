# campusmap.py
# Show FSC campus map using tkinter.

import tkinter as tk
from PIL import ImageTk, Image
import os
from scipy import spatial
from scipy.spatial.distance import cdist, squareform
import numpy as np
import sys
import tkinter.messagebox
import pdb

IMAGEROOT = os.getcwd()
IMAGEFILE = 'fsc_campus_map.png'
THOLD = 40

def main():
    # Create main window of application
    gui = tk.Tk()
    gui.title("FSC Campus Map")
    gui.configure(background='grey')

    # Create global lists with names and with coordinates
    global names, img, panel
    names = ['Barnett Athletic Complex', 'Badcock Memorial Garden','Mr. George\'s Green', 'Water Dome',
        'Dell Hall','Hollis Hall','Miller Hall','Allan Spivey Hall','Joseph Reynolds Hall',
        'Wesley Hall','Nicholas Hall','Buck Stop Grill (Pizza)','Happy Place','The Caf','Greenhouse',
        'President\'s Residence','George W. Jenkins Field House','Fannin Center','Ruel B. Gilbert Gymnasium',
        'Campus Safety and Security','Edge Hall','Jack M. Berry Citrus Building',
        'Volleyball Courts','Volleyball Courts','Intramurals Field','Office of Marketing and Communication',
        'Evett Simmons Multicultural Appreciation Center',
        'William F. Chatlos Journalism Building','Joe K. and Alberta Blanton Nursing Building',
        'Wynee Warden Dance Studio','Dr. Marcene H. & Robert E. Christoverson Humanities Building',
        'Sarah D. & L. Kirk McKay, Jr. Archives Center','Roux Library (Tutu\'s Cafe)',
        'Emile E. Watson Administration Building','Benjamin Fine Administration Building',
        'Thad Buckner Building','Annie Pfeiffer Chapel','William H. Danforth Chapel',
        'Robert A. Davis Performing Arts Center','Honeyman Pavilion',
        'Brandscomb Memorial Auditorium','Music Addition','Marjorie McKinley Music Building',
        'Melvin Gallery','Hester Plaza','Loca Lee Buckner Theatre','President\'s Residence',
        'Planetarium','Polk County Science Building','Polk County Science Building',
        'Polk County Science Building','Polk County Science Building',
        'Centennial Tower and Presidential Garden Plaza','Carlisle Rogers Building',
        'L.A. Raulerson Building','Sharp Family Tourism & Education Center Usonian House',
        'Rogers Field','Willis Garden of Meditation','Patriot\'s Plaza',
        'Lucius Pond Ordway Building','Military Science','L.N. Pipkin Bandshell',
        'Barnett Early Childhood Learning and Health','Roberts Academy',
        'Greek Village (Jenkins Hall)','Greek Village (Jenkins Hall)',
        'Wynee Warden Tennis Center','Wynee Warden Tennis Center',
        'Rinker Technology Center','Swimming Pool','Lynn\'s Garden',
        'Boathouse','Nina B. Hollis Wellness Center',
        'Charles T. Thrift Building (Student Health & Counseling Centers)',
        'Admissions Center','Facilities Maintenance Building',
        'Becker Business Building','Weinstein Computer Sciences Center']
    coordinates = [(512, 113),(407, 183),(540, 261),
        (221, 165),(722, 209),(717, 159),(700, 182),
        (466, 264),(398, 262),(443, 402),(527, 389),
        (382, 208),(832, 273),(639, 275),(386, 337),
        (317, 409),(504, 196),(452, 187),(560, 175),
        (626, 159),(459, 335),(510, 308),(698, 245),
        (728, 250),(868, 206),(99, 111),(103, 141),
        (96, 179),(97, 222),(111, 408),(103, 481),
        (187, 94),(225, 110),(167, 154),(188, 154),
        (187, 236),(245, 269),(235, 311),(224, 358),
        (223, 382),(222, 414),(226, 456),(152, 387),
        (186, 411),(167, 424),(168, 458),(319, 413),
        (349, 361),(336, 339),(324, 322),(315, 302),
        (303, 279),(350, 223),(281, 100),(269, 159),
        (319, 22),(337, 104),(410, 340),(439, 169),
        (395, 95),(587, 177),(579, 214),(762, 12),
        (900, 64),(646, 93),(713, 85),(859, 127),
        (795, 151),(628, 211),(623, 332),(579, 362),
        (618, 453),(656, 365),(662, 314),(794, 347),
        (793, 280),(927, 366),(866, 334)]
    buildings = dict(zip(names, coordinates))
    
    # Checks that the length of both lists are equal and stops program if not
    if (len(names) == len(coordinates)):
        print("All good!")
    else:
        print("Something\'s off...")
        print("Names: ", len(names))
        print("Coordinates: ", len(coordinates))
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
    gui.bind("<Button 1>", lambda event: getorigin(event, buildings))

    # Start the GUI
    gui.mainloop()

# (WORK) Displays the name of the location in a new window
def click(name):
    #w = tk.Label(panel, text=name, image=img, compound='center')
    #w.pack()
    tkinter.messagebox.showinfo("FSC Campus Map", name)

# (WORK) After click, Finds closest coordinates in the list and returns name of location
def getorigin(event, buildings):
    x = event.x
    y = event.y
    pt = np.array([event.x, event.y]).reshape(-1, 2)
    bldg = np.array(list(buildings.values()))
    d = cdist(pt, bldg)[0]

    smallest = min(d)
    if smallest < THOLD:
        whichbuilding = np.argmin(d)
        click(list(buildings.keys())[whichbuilding])

    # pdb.set_trace()
    # tree = spatial.KDTree(coordinates)
    # index = str((tree.query([(x,y)]))[1])
    # if (len(index) == 3):
    #     #print(names[int(index[1])])
    #     click(names[int(index[1])])
    # else:
    #     #print(names[int(index[1:3])])
    #     click(names[int(index[1:3])])

# # (RECORD) Track cursor coordinates in terminal
# def motion(event):
#     x, y = event.x, event.y
#     print('({}, {})'.format(x, y))

# # (RECORD(UNCOMMENT)) After you click, it asks for name as an input and prints it to an output file
# def getorigin(event):
#     x = event.x
#     y = event.y
#     f = open("output.txt", "a")
#     name = input('Enter name: ')
#     print('\'', name, '\' ', '({}, {})'.format(x, y), file=f, sep="")
#     f.close()

if __name__ == '__main__':
    main()