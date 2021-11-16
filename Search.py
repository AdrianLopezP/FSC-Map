from tkinter import *

root = Tk()
root.title('Maps')
root.geometry("800x500")

# Update the listbox
def update(data):
    # Clear listbox
    myList.delete(0, END)
    # Add list
    for i in data:
        myList.insert(END, i)

# Update entry box with click
def fillout(e):
    # Clear entry
    myEntry.delete(0, END)
    # Add click
    myEntry.insert(0, myList.get(ACTIVE))



# Create a label
myLabel = Label(root, text="Start Typing...",
            font=("Helvetica", 14), fg="grey")
myLabel.pack(pady=20)

# Create an entry box
myEntry = Entry(root, font=("Helvetica", 20))
myEntry.pack()

# Create a list box
myList = Listbox(root, width=50)
myList.pack(pady=40)

# Create building list
buildings = ["Becker Business", "Spivey Hall", "Polk Science",
                "Weinstein Computer Science", "Jenkins Green"]

# Add buildings to list
update(buildings)

# Create Binding
myList.bind("<<ListboxSelect>>", fillout)

myEntry.bind("<>",)

root.mainloop()