from tkinter import *
from PIL import ImageTk, Image
import numpy as np
from scipy.spatial.distance import cdist, squareform

IMAGEFILE = 'fsc_campus_map.png'
WIDTH = 985
HEIGHT = 525
COLORS = {'txt': '#FF0000', 'bg': '#FFFFFF'}
THOLD = 40
FONT = ("Consolas", 10, "bold")

# List of all the names of the locations on campus
NAMES = ['Barnett\nAthletic\nComplex','Badcock\nMemorial\nGarden','Mr. George\'s\nGreen','Water\nDome',
    'Dell Hall','Hollis Hall','Miller Hall','Allan Spivey\nHall','Joseph\nReynolds\nHall',
    'Wesley\nHall','Nicholas\nHall','Buck Stop\nGrill (Pizza)','Happy\nPlace','The Caf','Greenhouse',
    'President\'s\nResidence','George W.\nJenkins\nField\nHouse','Fannin\nCenter','Ruel B.\nGilbert\nGymnasium',
    'Campus\nSafety\nand\nSecurity','Edge\nHall','Jack\nM.\nBerry\nCitrus\nBuilding',
    'Volleyball\nCourts','Volleyball\nCourts','Intramurals\nField','Office of\nMarketing\nand\nCommunication',
    'Evett\nSimmons\nMulticultural\nAppreciation\nCenter','William F. Chatlos\nJournalism Building',
    'Joe K. and\nAlberta\nBlanton\nNursing\nBuilding','Wynee Warden\nDance Studio',
    'Dr. Marcene H. &\nRobert E.\nChristoverson\nHumanities Building',
    'Sarah D. &\nL. Kirk McKay, Jr.\nArchives\nCenter','Roux Library\n(Tutu\'s Cafe)',
    'Emile\nE.\nWatson\nAdministration\nBuilding','Benjamin\nFine\nAdministration\nBuilding',
    'Thad\nBuckner\nBuilding','Annie\nPfeiffer\nChapel','William\nH.\nDanforth\nChapel',
    'Robert\nA.\nDavis\nPerforming\nArts\nCenter','Honeyman\nPavilion',
    'Brandscomb\nMemorial\nAuditorium','Music\nAddition','Marjorie\nMcKinley\nMusic\nBuilding',
    'Melvin\nGallery','Hester\nPlaza','Loca Lee\nBuckner Theatre','President\'s\nResidence',
    'Planetarium','Polk\nCounty\nScience\nBuilding','Polk\nCounty\nScience\nBuilding',
    'Polk\nCounty\nScience\nBuilding','Polk\nCounty\nScience\nBuilding',
    'Centennial Tower and\nPresidential Garden Plaza','Carlisle\nRogers\nBuilding',
    'L.A.\nRaulerson\nBuilding','Sharp\nFamily\nTourism\n&\nEducation\nCenter\nUsonian\nHouse',
    'Rogers\nField','Willis\nGarden\nof\nMeditation','Patriot\'s\nPlaza',
    'Lucius Pond\nOrdway Building','Military\nScience','L.N.\nPipkin\nBandshell',
    'Barnett\nEarly\nChildhood\nLearning\nand\nHealth','Roberts\nAcademy',
    'Greek\nVillage\n(Jenkins\nHall)','Greek\nVillage','Wynee Warden\nTennis Center',
    'Rinker\nTechnology\nCenter','Swimming\nPool','Lynn\'s\nGarden',
    'Boathouse','Nina B. Hollis\nWellness Center',
    'Charles T. Thrift Building\n(Student Health & Counseling Centers)',
    'Admissions\nCenter','Facilities\nMaintenance\nBuilding',
    'Becker\nBusiness\nBuilding','Weinstein\nComputer\nSciences\nCenter',
    'Jenkins Hall','Bus Stop\nHollis Rooms','Bus Stop\nBecker','Bus Stop\nROTC Circle','Bus Stop\nWeinstein']

# List of all the coordinates of the locations on campus
COORDINATES = [(512, 113),(407, 183),(540, 261),(221, 165),(722, 209),(717, 159),(700, 182),
        (466, 264),(398, 262),(443, 402),(527, 389),(382, 208),(832, 273),(639, 275),(386, 337),
        (317, 409),(504, 196),(452, 187),(560, 175),(626, 159),(459, 335),(510, 308),(698, 245),
        (728, 250),(868, 206),(99, 111),(103, 141),(96, 179),(97, 222),(111, 408),(103, 481),
        (187, 94),(225, 110),(167, 154),(188, 154),(187, 236),(245, 269),(235, 311),(224, 358),
        (223, 382),(222, 414),(226, 456),(152, 387),(186, 411),(167, 424),(168, 458),(319, 413),
        (349, 361),(336, 339),(324, 322),(315, 302),(303, 279),(350, 223),(281, 100),(269, 159),
        (319, 22),(337, 104),(410, 340),(439, 169),(395, 95),(587, 177),(579, 214),(762, 12),
        (900, 64),(646, 93),(670, 94),(830, 140),(628, 211),(623, 332),(579, 362),
        (618, 453),(656, 365),(662, 314),(794, 347),(793, 280),(927, 366),(866, 334),(745, 88),
        (742, 168),(893, 330),(595, 175),(840, 318)]

def main():
    
    # Calls guisetup and catches the return into the root and canvas variables
    root, canvas = guisetup()

    # Open map image and puts it on the the window
    map = ImageTk.PhotoImage(Image.open(IMAGEFILE))
    canvas.create_image(0, 0, image=map, anchor=NW, tag='map')

    # Open pin image and assigns it to the 'pin' variable
    pin = ImageTk.PhotoImage(Image.open('map-pin.png').resize((50,50)))
    canvas.setvar('pin', pin)

    # Creates a dictionary with names as keys and coordinates as values
    buildings = dict(zip(NAMES, COORDINATES))

    # Creates the buttons
    button = Button(root,text='Bus Stops',width=8,height=1,bd='1',command=showbus(canvas, buildings))
    button.place(x=5, y=5)

    # Calls getorigin whenever the mouse is clicked
    root.bind("<Button 1>", lambda event: getorigin(event, buildings, canvas))

    # Calls endgame when escape key is pressed
    root.bind("<Escape>", endgame)

    # Starts mainloop
    root.mainloop()

def guisetup():

    # Creates the root
    root = Tk()
    root.title("FSC Campus Map")
    root.iconbitmap("FSCLOGO.ico")
    x = (root.winfo_screenwidth() - WIDTH) // 2
    y = (root.winfo_screenheight() - HEIGHT) // 2
    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")  # adjust the size of the window
    root.resizable(False, False)  # make the window fixed

    # Creates the canvas
    canvas = Canvas(root, width=WIDTH, height=HEIGHT, borderwidth=0)
    canvas.pack()

    # Returns both root and canvas as defined up above
    return root, canvas

def getorigin(event, buildings, canvas):

    print(event.x, " ", event.y)
    # Deletes any pre-existing text, textbox, or pins on the window
    canvas.delete('text', 'back', 'pin')

    # Creates a numpy array consisting of the coordinate of the click
    pt = np.array([event.x, event.y]).reshape(-1, 2)

    # Creates a numpy array consisting of all of the coordinates of the locations on the map
    bldg = np.array(list(buildings.values()))

    # Finds the distances between the click and each one of the locations on the map
    d = cdist(pt, bldg)[0]

    # Find the smallest of these distances
    smallest = min(d)

    # Checks if the closet location to the click is within a predetermined threshold
    if smallest < THOLD:

        # Gets the index and name (key) of the location
        buildingIndex = np.argmin(d)
        buildingName = list(buildings)[buildingIndex]
        
        # Calls click
        click(canvas, list(buildings.keys())[buildingIndex], list(buildings.values())[buildingIndex])

def click(canvas, name, coordinates):
    
    # Creates the pin image exactly on top of the coordinates of the location
    canvas.create_image(coordinates[0], coordinates[1]+5, image=canvas.getvar('pin'), anchor=S, tag='pin')

    # Checks if the location is Christoverson in order to show the text and textbox in a different spot and ensure its on the screen
    if (coordinates == ((103, 481))):
        text = canvas.create_text(coordinates[0], coordinates[1] - 100, justify=CENTER, text=name, anchor=N, fill=COLORS['txt'], font=FONT, tag='text')
    else:
        text = canvas.create_text(coordinates[0], coordinates[1] + 20, justify=CENTER, text=name, anchor=N, fill=COLORS['txt'], font=FONT, tag='text')
    
    # Adds a textbox and background to the text
    back = canvas.create_rectangle(canvas.bbox(text),fill=COLORS['bg'], tag='back')
    canvas.tag_lower(back, text)

def showbus(canvas, buildings):
    print("It runs")
    for i in range(73,len(buildings)):
        name = list(buildings.keys())[i]
        coordinates = list(buildings.values())[i]
        canvas.create_image(coordinates[0], coordinates[1]+5, image=canvas.getvar('pin'), anchor=S, tag='pin')
        text = canvas.create_text(coordinates[0], coordinates[1] + 20, justify=CENTER, text=name, anchor=N, fill=COLORS['txt'], font=FONT, tag='text')
        back = canvas.create_rectangle(canvas.bbox(text),fill=COLORS['bg'], tag='back')
        canvas.tag_lower(back, text)

def endgame(event):

    # Ends the program
    event.widget.destroy()

main()