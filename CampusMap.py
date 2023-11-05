from tkinter import *
from PIL import ImageTk, Image
import numpy as np
from scipy.spatial.distance import cdist

# Constants
IMAGEFILE = {'map': 'fsc_campus_map.png', 'pin': 'map-pin.png', 'fsc': 'FSCIMG.jpg'}
WIDTH = 985
HEIGHT = 525
COLORS = {'txt': '#FF0000', 'bg': '#FFFFFF'}
THOLD = 40  # Threshold for distance to detect nearest location
FONT = ("Consolas", 10, "bold")

# Data for campus locations
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
    'L.A.\nRaulerson\nBuilding','Sharp Family Tourism\n& Education Center\nUsonian House',
    'Rogers\nField','Willis\nGarden\nof\nMeditation','Patriot\'s\nPlaza',
    'Lucius Pond\nOrdway Building','Military\nScience','L.N.\nPipkin\nBandshell',
    'Barnett\nEarly\nChildhood\nLearning\nand\nHealth','Roberts\nAcademy',
    'Greek Village','Greek Village','Wynee Warden\nTennis Center',
    'Rinker\nTechnology\nCenter','Swimming\nPool','Lynn\'s\nGarden',
    'Boathouse','Nina B. Hollis\nWellness Center',
    'Charles T. Thrift Building\n(Student Health & Counseling Centers)',
    'Admissions\nCenter','Facilities\nMaintenance\nBuilding',
    'Becker\nBusiness\nBuilding','Weinstein\nComputer\nSciences\nCenter',
    'Jenkins Hall']

COORDINATES = [(512, 113),(407, 183),(540, 261),(221, 165),(722, 209),(717, 159),(700, 182),
        (466, 264),(398, 262),(443, 402),(527, 389),(382, 208),(832, 273),(639, 275),(386, 337),
        (317, 409),(504, 196),(452, 187),(560, 175),(626, 159),(459, 335),(510, 308),(698, 245),
        (728, 250),(868, 206),(99, 111),(103, 141),(96, 179),(97, 222),(111, 408),(103, 481),
        (187, 94),(225, 110),(167, 154),(188, 154),(187, 236),(245, 269),(235, 311),(224, 358),
        (223, 382),(222, 414),(226, 456),(152, 387),(186, 411),(167, 424),(168, 458),(319, 413),
        (349, 361),(336, 339),(324, 322),(315, 302),(303, 279),(350, 223),(281, 100),(269, 159),
        (190, 22),(337, 104),(410, 340),(439, 169),(395, 95),(587, 177),(579, 214),(762, 12),
        (900, 64),(646, 93),(670, 94),(830, 140),(628, 211),(623, 332),(579, 362),
        (618, 453),(656, 365),(662, 314),(794, 347),(793, 280),(927, 366),(866, 334),(745, 88)]

BUSSTOPS = {'Hollis Rooms': (742, 168),'Becker': (893, 337), 'ROTC Circle': (590, 175),
            'Weinstein': (844, 318), 'Buckner': (184, 270)}

PARKING = [(891, 286),(801, 204),(698, 301),(625, 184),(551, 323),(380, 451),(106, 453),(162, 307),(144, 121),(253, 60),
            (54, 137),(49, 210),(50, 273),(320, 21),(478, 67),(338, 102),(700, 31),(741, 117),(770, 80),(108, 368)]

# Main application function
def main():
    root, canvas = guisetup()
    
    # Load and display the campus map
    map_image = ImageTk.PhotoImage(Image.open(IMAGEFILE['map']))
    canvas.create_image(0, 0, image=map_image, anchor=NW, tag='map')

    # Load and prepare the pin image
    pin_image = ImageTk.PhotoImage(Image.open(IMAGEFILE['pin']).resize((50,50)))
    canvas.setvar('pin', pin_image)

    # Create a dictionary mapping building names to their coordinates
    buildings = dict(zip(NAMES, COORDINATES))

    # Add GUI elements (buttons)
    add_buttons(root, canvas, BUSSTOPS, PARKING)

    # Bind events for mouse click and escape key
    root.bind("<Button 1>", lambda event: getorigin(event, buildings, canvas))
    root.bind("<Escape>", lambda event: event.widget.destroy())

    # Start the GUI event loop
    root.mainloop()

# GUI setup function
def guisetup():
    root = Tk()
    root.title("FSC Campus Map")
    root.iconbitmap("FSCLOGO.ico")

    # Center the window on the screen
    x = (root.winfo_screenwidth() - WIDTH) // 2
    y = (root.winfo_screenheight() - HEIGHT) // 2
    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")
    root.resizable(False, False)

    # Create a canvas for drawing the map and elements
    canvas = Canvas(root, width=WIDTH, height=HEIGHT, borderwidth=0)
    canvas.pack()

    return root, canvas

# Function to handle mouse click events
def getorigin(event, buildings, canvas):
    canvas.delete('text', 'back', 'pin')  # Clear previous labels and pins

    # Compute distances from the click to each building
    click_point = np.array([event.x, event.y]).reshape(-1, 2)
    building_points = np.array(list(buildings.values()))
    distances = cdist(click_point, building_points)[0]
    nearest_building_distance = min(distances)

    # Check if the click is close enough to a building
    if nearest_building_distance < THOLD:
        building_index = np.argmin(distances)
        building_name = list(buildings)[building_index]
        click(canvas, building_name, list(buildings.values())[building_index])

# Function to handle the display of a pin and label
def click(canvas, name, coordinates):
    # Place the pin
    canvas.create_image(coordinates[0], coordinates[1]+5, image=canvas.getvar('pin'), anchor=S, tag='pin')

    # Decide the location for the label based on the specific building
    if coordinates == ((103, 481)):
        text_anchor = (coordinates[0], coordinates[1] - 100)
    else:
        text_anchor = (coordinates[0], coordinates[1] + 20)

    # Create the label
    text = canvas.create_text(text_anchor, justify=CENTER, text=name, anchor=N, fill=COLORS['txt'], font=FONT, tag='text')

    # Create a background box for the label
    back = canvas.create_rectangle(canvas.bbox(text), fill=COLORS['bg'], tag='back')
    canvas.tag_lower(back, text)

# Functions to display bus stops and parking spots
def showbus(canvas, BUSSTOPS):
    
    # Creates Bus Stops title
    canvas.create_text(470, 18, justify=CENTER, text='Bus Stops', anchor=CENTER, fill=COLORS['txt'], font=("Consolas", 22, "bold"), tag='text')

    # Loops through BUSSTOPS dictionary
    for i in range(len(BUSSTOPS)):

        # Finds and stores the name and coordinates in variables
        name = list(BUSSTOPS.keys())[i]
        coordinates = list(BUSSTOPS.values())[i]

        # Creates pin image at correct coordinate and creates text and textbox near the pin
        canvas.create_image(coordinates[0], coordinates[1]+5, image=canvas.getvar('pin'), anchor=S, tag='pin')
        text = canvas.create_text(coordinates[0], coordinates[1] + 10, justify=CENTER, text=name, anchor=N, fill=COLORS['txt'], font=FONT, tag='text')
        back = canvas.create_rectangle(canvas.bbox(text),fill=COLORS['bg'], tag='back')
        canvas.tag_lower(back, text)

def showParking(canvas, PARKING):
    
    # Creates Parking title
    canvas.create_text(470, 18, justify=CENTER, text='Parking', anchor=CENTER, fill=COLORS['txt'], font=("Consolas", 22, "bold"), tag='text')
    
    # Loops through PARKING list
    for i in range(len(PARKING)):
        
        # Finds and stores the coordinates in variables
        coordinates = PARKING[i]

        # Displays pin image at the coordinates of a parking spot
        canvas.create_image(coordinates[0], coordinates[1]+5, image=canvas.getvar('pin'), anchor=S, tag='pin')

# Function to clear pins and labels from the canvas
def close(canvas):
    canvas.delete('text', 'back', 'pin')

# Function to add buttons to the GUI
def add_buttons(root, canvas, BUSSTOPS, PARKING):
    # Bus stop button
    busButton = Button(root, text='Bus Stops', width=7, height=1, bd='1')
    busButton['command'] = lambda: showbus(canvas, BUSSTOPS)
    busButton.place(x=5, y=5)

    # Parking button
    parkingButton = Button(root, text='Parking', width=7, height=1, bd='1')
    parkingButton['command'] = lambda: showParking(canvas, PARKING)
    parkingButton.place(x=5, y=35)

    # Clear button
    closeButton = Button(root, text='Clear', width=5, height=1, bd='1')
    closeButton['command'] = lambda: close(canvas)
    closeButton.place(x=70, y=5)

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
