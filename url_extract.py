from tkinter import *
import requests as r
import io
from PIL import ImageTk
from colourpycker.colourpycker import *


class UrlExtract:
    def __init__(self, canvas: Canvas, home):
        self.canvas = canvas
        self.go_home = home
        self.canvas.create_text((375, 30), text="Harvest Color from Image URL", fill='#49108B',
                                font=("Verdana", 15, "bold"))
        self.canvas.create_text((200, 70), text="Input Image Url\n(.jpg or .png)", font=("Verdana", 10, "bold"),
                                fill="#000000")
        self.input_url = Entry(width=35, highlightthickness=0)
        self.input_url.place(x=280, y=60)
        self.extract_btn = Button(text="Extract", font=("Verdana", 10, "bold"), bg="purple", fg="white",
                                  highlightthickness=0, command=self.load_img)
        self.extract_btn.place(x=520, y=60)

        self.home_button = Button(text="Home", font=("Verdana", 10, "bold"), bg="purple", fg="white",
                                  highlightthickness=0, command=self.go_home_callback)
        self.home_button.place(x=50, y=30)

        self.image_canvas = None
        self.final_image = None
        self.left_canvas = None
        self.right_canvas = None

    def load_img(self):
        url_entered = self.input_url.get()
        self.destroy_items()
        try:
            response = r.get(url_entered)
            if response.status_code == 200:
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))
                resized_img = image.resize((150, 150))

                self.final_image = ImageTk.PhotoImage(resized_img)

                self.image_canvas = Canvas(self.canvas, width=150, height=150, bg="white",
                                           highlightbackground="#000000", highlightthickness=1.5)
                self.image_canvas.place(x=100, y=100)

                self.image_canvas.delete("all")
                self.image_canvas.create_image(75, 75, anchor="center", image=self.final_image)

                self.generate_color(url_entered)

            else:
                failed_label = self.canvas.create_text((375, 100), text="URL IS INVALID or\nCHECK INTERNET CONNECTION",
                                                       font=("Verdana", 8, "bold"), fill="red")
                self.canvas.after(5000, lambda: self.canvas.delete(failed_label))

        except Exception as e:
            print(f"An error occurred: {e}")
            failed_label = self.canvas.create_text((375, 100), text=f"Error Occurred : {e}",
                                                   font=("Verdana", 8, "bold"), fill="red")
            self.image_canvas.destroy()
            self.canvas.after(5000, lambda: self.canvas.delete(failed_label))

    def generate_color(self, url):
        palette = get_color_palette(url, 10, 15)
        first_five = palette[:5]
        remaining_ten = palette[5:]

        margin = 0

        if first_five.size > 0:
            self.left_canvas = Canvas(self.canvas, width=300, height=250, bg="white",
                                      highlightbackground="#000000", highlightthickness=1.5)
            self.left_canvas.place(x=20, y=290)

            self.left_canvas.create_text((50, 15), text="HEX CODE", font=("Verdana", 8, "bold"),
                                         fill="blue")
            self.left_canvas.create_text((150, 15), text="RGB CODE", font=("Verdana", 8, "bold"),
                                         fill="blue")
            self.left_canvas.create_text((250, 15), text="COLOR", font=("Verdana", 8, "bold"),
                                         fill="blue")

            for hex_code in first_five["HEX"]:
                self.left_canvas.create_text((50, 50 + margin), text=hex_code, font=("Verdana", 8, "bold"),
                                             fill="black", state=NORMAL)
                self.left_canvas.create_rectangle(220, 40 + margin, 270, 70 + margin, fill=hex_code)

                margin += 40

            margin = 0
            for rgb_code in first_five["RGB"]:
                self.left_canvas.create_text((150, 50 + margin), text=rgb_code, font=("Verdana", 8, "bold"),
                                             fill="black")
                margin += 40

        if remaining_ten.size > 0:
            self.right_canvas = Canvas(self.canvas, width=300, height=435, bg="white",
                                       highlightbackground="#000000", highlightthickness=1.5)
            self.right_canvas.place(x=350, y=100)

            self.right_canvas.create_text((50, 15), text="HEX CODE", font=("Verdana", 8, "bold"),
                                          fill="blue")
            self.right_canvas.create_text((150, 15), text="RGB CODE", font=("Verdana", 8, "bold"),
                                          fill="blue")
            self.right_canvas.create_text((250, 15), text="COLOR", font=("Verdana", 8, "bold"),
                                          fill="blue")

            margin = 0
            for hex_code in remaining_ten["HEX"]:
                self.right_canvas.create_text((50, 50 + margin), text=hex_code, font=("Verdana", 8, "bold"),
                                              fill="black", state=NORMAL)
                self.right_canvas.create_rectangle(220, 40 + margin, 270, 70 + margin, fill=hex_code)

                margin += 40

            margin = 0

            for rgb_code in remaining_ten["RGB"]:
                self.right_canvas.create_text((150, 50 + margin), text=rgb_code, font=("Verdana", 8, "bold"),
                                              fill="black")
                margin += 40

    def destroy_items(self):
        if self.image_canvas is not None:
            self.image_canvas.destroy()
        if self.left_canvas is not None:
            self.left_canvas.destroy()
        if self.right_canvas is not None:
            self.right_canvas.destroy()

    def go_home_callback(self):
        self.input_url.destroy()
        self.extract_btn.destroy()
        self.home_button.destroy()
        self.destroy_items()
        self.go_home()
