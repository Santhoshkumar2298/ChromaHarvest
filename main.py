from tkinter import *
from file_extract import FileExtract
from url_extract import UrlExtract
from datetime import datetime

window = Tk()
window.title("Chroma_Harvest_v1.0 ©SANTHOSHKUMAR_V. All rights reserved")
window.resizable(False, False)
window.config(bg="#ffffff", padx=20, pady=20)
width = 800
height = 600
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x = (ws / 2) - (width / 2) - 20
y = (hs / 2) - (height / 2) - 40
window.geometry('%dx%d+%d+%d' % (width, height, x, y))

current_year = datetime.now().year

canvas = Canvas(window, width=750, height=550, bg="#ffffff", highlightbackground="#0B60B0", relief="ridge")
canvas.place(x=0, y=0)
img_extract_btn = Button()
url_extract_btn = Button()

background_img = PhotoImage(file="images/background.png")
extract_img = PhotoImage(file="images/extract_background.png")


def home():
    global img_extract_btn, url_extract_btn
    canvas.create_image(400, 260, image=background_img)
    canvas.create_text((375, 200), text="ChromaHarvest", fill='#FF004D', font=("Verdana", 45, "bold"))
    canvas.create_text((375, 260), text="Select the type of Color harvest", fill="#33186B",
                       font=("Verdana", 18, "bold"))

    url_extract_btn = Button(width=18, text="Harvest from\nUrl", font=("Verdana", 15, "bold"), bg="#FF004D",
                             fg="white", relief="groove", command=open_url_extract)
    url_extract_btn.place(x=100, y=300)

    img_extract_btn = Button(width=18, text="Harvest from\nFile", font=("Verdana", 15, "bold"), bg="#FF004D",
                             fg="white", relief="groove", command=open_file_extract)
    img_extract_btn.place(x=400, y=300)

    canvas.create_text((375, 480), text=f"{current_year} © Santhoshkumar_V. All rights reserved", fill='#FF004D',
                       font=("arial", 8, "bold"))


def open_url_extract():
    destroy_home()
    UrlExtract(canvas, go_home_callback)


def open_file_extract():
    destroy_home()
    FileExtract(canvas, go_home_callback)


def destroy_home():
    global img_extract_btn, url_extract_btn
    canvas.delete("all")
    canvas.create_image(400, 260, image=extract_img)
    img_extract_btn.destroy()
    url_extract_btn.destroy()


def go_home_callback():
    canvas.delete("all")
    home()


home()

window.mainloop()
