import tkinter as tk
from PIL import ImageTk, Image
import os

IMAGEROOT = os.getcwd()
IMAGEFILE = 'fsc_campus_map.png'
WIDTH = 1050
HEIGHT = 550
NAMES = ['Barnett Athletic Complex', 'Badcock Memorial Garden','Mr. George\'s Green', 'Water Dome',
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
COORDINATES = [(512, 113),(407, 183),(540, 261),
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

def main():
    root, canvas = guisetup()

    map = ImageTk.PhotoImage(Image.open(IMAGEFILE))
    x0 = 175  # TOD: Force player to start in the middle of the screen
    y0 = HEIGHT - 1000
    canvas.create_image(0, 0, image=map, anchor=NW, tag='player')

    root.mainloop()



def guisetup():
    root = tk()
    root.title("FSC Campus Map")
    root.iconbitmap("FSCLOGO.ico")
    x = (root.winfo_screenwidth() - WIDTH) // 2
    y = (root.winfo_screenheight() - HEIGHT) // 2
    root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")  # adjust the size of the window
    root.resizable(False, False)  # make the window fixed

    canvas = Canvas(root, width=WIDTH, height=HEIGHT, background=COLORS['bg'], borderwidth=0)
    canvas.setvar('stillplaying', True)
    canvas.pack()

    return root, canvas