from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import colorgram


class FileExtract:
    def __init__(self, canvas: Canvas, home):
        self.canvas = canvas
        self.go_home = home
        self.canvas.create_text((375, 30), text="Harvest Color from File", fill='#49108B',
                                font=("Verdana", 15, "bold"))
        self.canvas.create_text((280, 70), text="Upload Image File (.jpg or .png)", font=("Verdana", 10, "bold"),
                                fill="#000000")
        self.choose_btn = Button(text="Choose File", font=("Verdana", 10, "bold"), bg="purple", fg="white",
                                 highlightthickness=0, command=self.select_image)
        self.choose_btn.place(x=430, y=60)

        self.home_button = Button(text="Home", font=("Verdana", 10, "bold"), bg="purple", fg="white",
                                  highlightthickness=0, command=self.go_home_callback)
        self.home_button.place(x=50, y=30)
        self.image = None
        self.file_path = None
        self.image_canvas = None
        self.rgb_colors = []
        self.hex_codes = []
        self.left_canvas = None
        self.right_canvas = None

    def select_image(self):
        self.destroy_items()
        filetypes = (("Image Files", "*.jpg, *.png"),)
        file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=filetypes)
        if file != "":
            try:
                file_name = os.path.basename(file)

                self.file_path = self.canvas.create_text((170, 270), width=150, text=file_name, fill="#FF004D",
                                                         font=("Verdana", 8, "bold"))
                self.image = Image.open(file)
                self.image = self.image.resize((150, 150))
                self.image = ImageTk.PhotoImage(self.image)

                self.image_canvas = Canvas(self.canvas, width=150, height=150, bg="white",
                                           highlightbackground="#000000", highlightthickness=1.5)
                self.image_canvas.place(x=100, y=100)

                self.image_canvas.delete("all")
                self.image_canvas.create_image(75, 75, anchor="center", image=self.image)

                self.generate_color(file)

            except Exception as e:
                print(f"An error occurred: {e}")
                failed_label = self.canvas.create_text((375, 150), text=f"Error Occurred : {e}",
                                                       font=("Verdana", 8, "bold"), fill="red")
                self.image_canvas.destroy()
                self.canvas.after(5000, lambda: self.canvas.delete(failed_label))
        else:
            failed_label = self.canvas.create_text((375, 150), text=f"Select the File to Harvest Color",
                                                   font=("Verdana", 8, "bold"), fill="red")
            self.image_canvas.destroy()
            self.canvas.after(5000, lambda: self.canvas.delete(failed_label))

    def generate_color(self, image):
        colors = colorgram.extract(image, 15)
        for color in colors:
            rgb_tuple = self.create_rgb_colors(color.rgb.r, color.rgb.g, color.rgb.b)
            self.rgb_to_hex(rgb_tuple)

        rgb_first_five = self.rgb_colors[:5]
        rgb_remaining = self.rgb_colors[5:]
        hex_first_five = self.hex_codes[:5]
        hex_remaining = self.hex_codes[5:]

        margin = 0

        if len(rgb_first_five) > 0 and len(hex_first_five) > 0:
            self.left_canvas = Canvas(self.canvas, width=300, height=250, bg="white",
                                      highlightbackground="#000000", highlightthickness=1.5)
            self.left_canvas.place(x=20, y=290)

            self.left_canvas.create_text((50, 15), text="HEX CODE", font=("Verdana", 8, "bold"),
                                         fill="blue")
            self.left_canvas.create_text((150, 15), text="RGB CODE", font=("Verdana", 8, "bold"),
                                         fill="blue")
            self.left_canvas.create_text((250, 15), text="COLOR", font=("Verdana", 8, "bold"),
                                         fill="blue")

            for hex_code in hex_first_five:
                self.left_canvas.create_text((50, 50 + margin), text=hex_code, font=("Verdana", 8, "bold"),
                                             fill="black", state=NORMAL)
                self.left_canvas.create_rectangle(220, 40 + margin, 270, 70 + margin, fill=hex_code)

                margin += 40

            margin = 0
            for rgb_code in rgb_first_five:
                self.left_canvas.create_text((150, 50 + margin), text=rgb_code, font=("Verdana", 8, "bold"),
                                             fill="black")
                margin += 40

        if len(hex_remaining) > 0 and len(rgb_remaining) > 0:
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
            for hex_code in hex_remaining:
                self.right_canvas.create_text((50, 50 + margin), text=hex_code, font=("Verdana", 8, "bold"),
                                              fill="black", state=NORMAL)
                self.right_canvas.create_rectangle(220, 40 + margin, 270, 70 + margin, fill=hex_code)

                margin += 40

            margin = 0

            for rgb_code in rgb_remaining:
                self.right_canvas.create_text((150, 50 + margin), text=rgb_code, font=("Verdana", 8, "bold"),
                                              fill="black")
                margin += 40

    def create_rgb_colors(self, r, g, b):
        self.rgb_colors.append((r, g, b))
        return r, g, b

    def rgb_to_hex(self, rgb):
        self.hex_codes.append("#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2]))

    def destroy_items(self):
        if self.image_canvas is not None:
            self.image_canvas.destroy()
        if self.left_canvas is not None:
            self.left_canvas.destroy()
        if self.right_canvas is not None:
            self.right_canvas.destroy()
        if self.file_path is not None:
            self.canvas.delete(self.file_path)

    def go_home_callback(self):
        self.choose_btn.destroy()
        self.home_button.destroy()
        self.destroy_items()
        self.go_home()
