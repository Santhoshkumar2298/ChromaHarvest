from tkinter import *
import requests as r
import io
from PIL import ImageTk
from colourpycker.colourpycker import *


class UrlExtract:
    def __init__(self, canvas: Canvas, home):
        # INITIALIZING URL EXTRACT PAGE
        self.canvas = canvas
        self.go_home = home
        self.canvas.create_text((375, 30), text="Harvest Color from Image URL", fill='#49108B',
                                font=("Verdana", 15, "bold"))
        self.canvas.create_text((200, 70), text="Input Image Url\n(.jpg or .png)", font=("Verdana", 10, "bold"),
                                fill="#000000")

        # INPUT BOX FOR URL
        self.input_url = Entry(width=35, highlightthickness=0)
        self.input_url.place(x=280, y=60)

        # HARVEST BUTTON FOR COLOR EXTRACT FROM ENTERED URL
        self.extract_btn = Button(text="Harvest", font=("Verdana", 10, "bold"), bg="purple", fg="white",
                                  highlightthickness=0, command=self.load_img)
        self.extract_btn.place(x=520, y=60)

        # GO BACK TO HOME BUTTON
        self.home_button = Button(text="Home", font=("Verdana", 10, "bold"), bg="purple", fg="white",
                                  highlightthickness=0, command=self.go_home_callback)
        self.home_button.place(x=50, y=30)

        # INITIATING REQUIRED ELEMENTS
        self.image_canvas = None
        self.final_image = None
        self.left_canvas = None
        self.right_canvas = None

    def load_img(self):
        # GET THE ENTERED URL FROM INPUT URL
        url_entered = self.input_url.get()
        self.destroy_items()
        try:
            # SEND THE REQUEST TO THE ENTERED URL AND GET THE RESPONSE
            response = r.get(url_entered)
            if response.status_code == 200:
                # CONVERTING THE BYTE DATA FROM RESPONSE TO IMAGE
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))

                # RESIZING OF IMAGE
                resized_img = image.resize((150, 150))

                self.final_image = ImageTk.PhotoImage(resized_img)

                # CREATING IMAGE CANVAS AND POPULATING THE IMAGE
                self.image_canvas = Canvas(self.canvas, width=150, height=150, bg="white",
                                           highlightbackground="#000000", highlightthickness=1.5)
                self.image_canvas.place(x=100, y=100)

                # DELETE THE IMAGE IF ANY POPULATED PREVIOUSLY
                self.image_canvas.delete("all")
                self.image_canvas.create_image(75, 75, anchor="center", image=self.final_image)

                # CALLING GENERATE COLOR FUNCTION
                self.generate_color(url_entered)

            else:
                # SHOWING FAILED MESSAGE WHEN THE URL IS INVALID OR NO INTERNET CONNECTION FOR MAKING REQUEST
                failed_label = self.canvas.create_text((375, 100), text="URL IS INVALID or\nCHECK INTERNET CONNECTION",
                                                       font=("Verdana", 8, "bold"), fill="red")

                # DESTROYING FAILED MESSAGE AFTER 5 SECONDS
                self.canvas.after(5000, lambda: self.canvas.delete(failed_label))

        except Exception as e:
            print(f"An error occurred: {e}")
            # SHOWING FAILED MESSAGE WHEN THE RESPONSE IS FAILED OR ERROR RESPONSE
            failed_label = self.canvas.create_text((375, 100), text=f"Error Occurred : {e}",
                                                   font=("Verdana", 8, "bold"), fill="red")
            self.image_canvas.destroy()
            self.canvas.after(5000, lambda: self.canvas.delete(failed_label))

    def generate_color(self, url):
        # GENERATING THE COLOR PALETTE FROM THE IMAGE URL USING colourpycker LIBRARY
        palette = get_color_palette(url, 10, 15)

        # SEPARATING COLORS IN ARRAY OF 5 AND 10
        first_five = palette[:5]
        remaining_ten = palette[5:]

        # INITIATING MARGIN FOR DIFFERENT COLOR ROWS
        margin = 0

        if first_five.size > 0:
            # CREATING CANVAS FOR POPULATING FIRST 5 ELEMENTS (HEX AND RGB)
            self.left_canvas = Canvas(self.canvas, width=300, height=250, bg="white",
                                      highlightbackground="#000000", highlightthickness=1.5)
            self.left_canvas.place(x=20, y=290)

            self.left_canvas.create_text((50, 15), text="HEX CODE", font=("Verdana", 8, "bold"),
                                         fill="blue")
            self.left_canvas.create_text((150, 15), text="RGB CODE", font=("Verdana", 8, "bold"),
                                         fill="blue")
            self.left_canvas.create_text((250, 15), text="COLOR", font=("Verdana", 8, "bold"),
                                         fill="blue")

            # LOOPING THROUGH ELEMENTS AND POPULATING HEX CODES AND RESPECTIVE COLORS IN ROWS
            for hex_code in first_five["HEX"]:
                self.left_canvas.create_text((50, 50 + margin), text=hex_code, font=("Verdana", 8, "bold"),
                                             fill="black", state=NORMAL)
                self.left_canvas.create_rectangle(220, 40 + margin, 270, 70 + margin, fill=hex_code)

                margin += 40

            margin = 0
            # LOOPING THROUGH ELEMENTS AND POPULATING RGB IN ROWS
            for rgb_code in first_five["RGB"]:
                self.left_canvas.create_text((150, 50 + margin), text=rgb_code, font=("Verdana", 8, "bold"),
                                             fill="black")
                margin += 40

        # CREATING CANVAS FOR POPULATING REMAINING COLORS
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
            # POPULATING HEX CODES AND RESPECTIVE COLORS IN ROWS
            for hex_code in remaining_ten["HEX"]:
                self.right_canvas.create_text((50, 50 + margin), text=hex_code, font=("Verdana", 8, "bold"),
                                              fill="black", state=NORMAL)
                self.right_canvas.create_rectangle(220, 40 + margin, 270, 70 + margin, fill=hex_code)

                margin += 40

            margin = 0

            # LOOPING THROUGH ELEMENTS AND POPULATING RGB COLORS IN ROWS
            for rgb_code in remaining_ten["RGB"]:
                self.right_canvas.create_text((150, 50 + margin), text=rgb_code, font=("Verdana", 8, "bold"),
                                              fill="black")
                margin += 40

    def destroy_items(self):
        # DESTROY ITEMS IN CANVAS WHEN USER ENTERS DIFFERENT IMAGE URL
        if self.image_canvas is not None:
            self.image_canvas.destroy()
        if self.left_canvas is not None:
            self.left_canvas.destroy()
        if self.right_canvas is not None:
            self.right_canvas.destroy()

    def go_home_callback(self):
        # DESTROY ITEMS IN WINDOW WHEN USER TRY TO GET BACK TO HOMEPAGE
        self.input_url.destroy()
        self.extract_btn.destroy()
        self.home_button.destroy()
        self.destroy_items()
        self.go_home()
