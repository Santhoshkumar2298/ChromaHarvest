from tkinter import *
from file_extract import FileExtract
from url_extract import UrlExtract
from datetime import datetime

# Creating Window
window = Tk()
window.title("Chroma_Harvest_v1.0 ©SANTHOSHKUMAR_V. All rights reserved")
window.resizable(False, False)
window.config(bg="#ffffff", padx=20, pady=20)

# SIZING AND POSITIONING OF WINDOW TO THE CENTER OF THE SCREEN
width = 800
height = 600
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws / 2) - (width / 2) - 20
y = (hs / 2) - (height / 2) - 40
window.geometry('%dx%d+%d+%d' % (width, height, x, y))

# GETTING CURRENT YEAR
current_year = datetime.now().year

# CREATING CANVAS FOR PLACING ELEMENTS
canvas = Canvas(window, width=750, height=550, bg="#ffffff", highlightbackground="#0B60B0", relief="ridge")
canvas.place(x=0, y=0)

# INITIATING NECESSARY ELEMENTS
img_extract_btn = Button()
url_extract_btn = Button()
background_img = PhotoImage(file="images/background.png")
extract_img = PhotoImage(file="images/extract_background.png")


# MAIN FUNCTION
def home():
    global img_extract_btn, url_extract_btn
    # CREATE HOME CONTENT
    canvas.create_image(400, 260, image=background_img)
    canvas.create_text((375, 200), text="ChromaHarvest", fill='#FF004D', font=("Verdana", 45, "bold"))
    canvas.create_text((375, 260), text="Select the type of Color harvest", fill="#33186B",
                       font=("Verdana", 18, "bold"))

    # URL EXTRACT BUTTON
    url_extract_btn = Button(width=18, text="Harvest from\nUrl", font=("Verdana", 15, "bold"), bg="#FF004D",
                             fg="white", relief="groove", command=open_url_extract)
    url_extract_btn.place(x=100, y=300)

    # IMAGE EXTRACT FROM FILE BUTTON
    img_extract_btn = Button(width=18, text="Harvest from\nFile", font=("Verdana", 15, "bold"), bg="#FF004D",
                             fg="white", relief="groove", command=open_file_extract)
    img_extract_btn.place(x=400, y=300)

    # COPYRIGHT TEXT
    canvas.create_text((375, 480), text=f"{current_year} © Santhoshkumar_V. All rights reserved", fill='#FF004D',
                       font=("arial", 8, "bold"))


def open_url_extract():
    # OPENING URL COLOR EXTRACT PAGE
    destroy_home()
    UrlExtract(canvas, go_home_callback)


def open_file_extract():
    # OPENING FILE COLOR EXTRACT PAGE
    destroy_home()
    FileExtract(canvas, go_home_callback)


def destroy_home():
    # DESTROYING HOME ELEMENTS WHEN NAVIGATE TO OTHER PAGE
    global img_extract_btn, url_extract_btn
    canvas.delete("all")
    img_extract_btn.destroy()
    url_extract_btn.destroy()

    # CREATING BACKGROUND IMAGE FOR NAVIGATING PAGE
    canvas.create_image(400, 260, image=extract_img)


def go_home_callback():
    # RECREATING HOME CONTENT WHEN NAVIGATING TO HOME AGAIN
    canvas.delete("all")
    home()


home()

window.mainloop()
