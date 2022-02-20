from tkinter import *
from tkmacosx import Button
from tkinter.filedialog import askopenfiles
from PIL import Image, ImageDraw, ImageFont
from tkinter import messagebox


class Watermark(Tk):
    def __init__(self):
        super().__init__()
        self.position_opt_hor = ["From Left", "From Right", "Center"]
        self.position_opt_vert = ["From Top", "From Bottom", "Center"]
        self.position_var_vert = None
        self.rotate_angle = None
        self.opacity_var = None
        self.rotate_var = None
        self.font_size_entry = None
        self.text_to_add = None
        self.height_var = None
        self.width_var = None
        self.position_var_hor = None
        self.sub_text_frame = None
        self.file_path = None
        self.variable = StringVar(self.sub_text_frame)
        self.title("Watermark Adder")
        self.config(padx=20, pady=20, background="#084594")
        self.geometry("800x800")

        # Welcome label
        wel_label = Label(self, text="Welcome to watermarker adder app", font=("Helvetica", 24),
                          fg="#FFD32D", bg="#084594")
        wel_label.grid(row=0, column=0, columnspan=2)
        #    upload label
        up_label = Label(self, text="Select images to add Watermark", font=("Helvetica", 20), foreground="#FFD32D",
                         background="#084594")
        up_label.grid(row=1, column=0, padx=30, pady=30)
        #     button creation
        file_up_btn = Button(self, text='Choose File', command=self.open_file, background="#FFD32D", foreground="white",
                             borderless=1)
        file_up_btn.grid(row=1, column=1, padx=30, pady=30)

        # Text watermark Radio Button
        self.main_radio_selector = IntVar()
        radio_text = Radiobutton(self, text="Add watermark by Text", background="#FFD32D", foreground="white",
                                 variable=self.main_radio_selector, value=1, command=self.add_using_text)
        radio_text.grid(row=2, column=0, padx=10, pady=30)

        # Image watermark Radio Button
        radio_image = Radiobutton(self, text="Add Watermark by another Image/Logo", background="#FFD32D",
                                  foreground="white", variable=self.main_radio_selector, value=2,
                                  command=self.add_using_image)
        radio_image.grid(row=2, column=1, padx=10, pady=30)

    def open_file(self):
        self.file_path = askopenfiles(mode='r', title="Please choose the images",
                                      filetypes=[('Image Files', ('.jpg', '.png', '.jpeg'))])

    def position(self):
        self.position_var_hor = StringVar(self.sub_text_frame)
        self.position_var_hor.set(self.position_opt_hor[0])
        self.position_var_vert = StringVar(self.sub_text_frame)
        self.position_var_vert.set(self.position_opt_vert[0])
        position_hor_select_label = Label(self.sub_text_frame, text="Modify orientation for Horizontal Distance")
        position_hor_select_label.grid(row=7, column=0, padx=10, pady=10)
        position_vert_select_label = Label(self.sub_text_frame, text="Modify orientation for Vertical Distance")
        position_vert_select_label.grid(row=8, column=0, padx=10, pady=10)
        position_hor_select = OptionMenu(self.sub_text_frame, self.position_var_hor, *self.position_opt_hor)
        position_hor_select.grid(row=7, column=1, padx=10, pady=10)
        position_vert_select = OptionMenu(self.sub_text_frame, self.position_var_vert, *self.position_opt_vert)
        position_vert_select.grid(row=8, column=1, padx=10, pady=10)
        #     position X and Y
        default = 0
        self.width_var = IntVar()
        self.width_var.set(default)
        self.height_var = IntVar()
        self.height_var.set(default)
        width_value = Entry(self.sub_text_frame, width=10, textvariable=self.width_var)
        width_value.grid(row=7, column=2, padx=10, pady=10)
        height_value = Entry(self.sub_text_frame, width=10, textvariable=self.height_var)
        height_value.grid(row=8, column=2, padx=10, pady=10)

    def calculate_position(self, size):
        text_width, text_height = size
        if self.position_var_hor.get() == self.position_opt_hor[0]:
            width = int(self.width_var.get())
        elif self.position_var_hor.get() == self.position_opt_hor[1]:
            width = self.image.size[0] - (text_width + int(self.width_var.get()))
        else:
            width = (self.image.size[0] / 2) - (text_width / 2)

        if self.position_var_vert.get() == self.position_opt_vert[0]:
            height = int(self.height_var.get())
        elif self.position_var_vert.get() == self.position_opt_vert[1]:
            height = self.image.size[1] - (text_height + int(self.height_var.get()))
        else:
            height = (self.image.size[1] / 2) - (text_height / 2)

        return int(width), int(height)

    def add_text_labels(self):
        text_label = Label(self.sub_text_frame, text="Enter your Watermark text")
        text_label.grid(row=3, column=0, padx=10, pady=10)
        # Text to add
        self.text_to_add = Entry(self.sub_text_frame, width=19)
        self.text_to_add.grid(row=3, column=1, padx=10, pady=10)
        # Selector
        options = ["Regular", "Bold", "Bold-Italics"]
        self.variable.set(options[0])  # setting default value
        font_type_label = Label(self.sub_text_frame, text="Select Font Type")
        font_type_label.grid(row=4, column=0, padx=10, pady=10)
        font_type_drop = OptionMenu(self.sub_text_frame, self.variable, *options)
        font_type_drop.grid(row=4, column=1, padx=10, pady=10)
        # font_size
        font_size_label = Label(self.sub_text_frame, text="Font Size")
        font_size_label.grid(row=5, column=0, padx=10, pady=10)
        self.font_size_entry = Entry(self.sub_text_frame, width=10)
        self.font_size_entry.grid(row=5, column=1, padx=10, pady=10)
        #     opacity
        opacity_label = Label(self.sub_text_frame, text="Opacity percentage")
        opacity_label.grid(row=5, column=2, padx=10, pady=10)
        self.opacity_var = IntVar()
        opacity_value = Entry(self.sub_text_frame, width=10, textvariable=self.opacity_var)
        self.opacity_var.set(100)
        opacity_value.grid(row=5, column=3, padx=10, pady=10)

    def rotate_txt_img(self):
        def state_change():
            if self.rotate_var.get() == 1:
                self.rotate_angle.config(state="normal")
            elif self.rotate_var.get() == 0:
                self.rotate_angle.config(state="disabled")

        self.rotate_var = IntVar(self.sub_text_frame)
        rotate_check = Checkbutton(self.sub_text_frame, text="Rotate text", variable=self.rotate_var, onvalue=1,
                                   offvalue=0,
                                   command=state_change)
        rotate_check.grid(row=6, column=0, padx=10, pady=10)
        rotate_angle_label = Label(self.sub_text_frame, text="Specify Rotate Angle")
        rotate_angle_label.grid(row=6, column=1, padx=10, pady=10)
        self.rotate_angle = Entry(self.sub_text_frame, width=10, state="disabled")
        self.rotate_angle.grid(row=6, column=2, padx=10, pady=10)

    def check_image_upload(self):
        if not self.file_path:
            self.main_radio_selector.set(0)
            messagebox.showerror("Image not found", "Please upload image to add watermark")
            return True

    def add_using_text(self):
        if self.check_image_upload():
            return None
        if self.sub_text_frame:
            self.sub_text_frame.destroy()
        self.sub_text_frame = Frame(self)
        self.sub_text_frame.grid(row=3, column=0, columnspan=2)

        self.add_text_labels()
        self.rotate_txt_img()
        self.position()
        submit_btn = Button(self.sub_text_frame, text="Submit", command=self.add_watermark)
        submit_btn.grid(row=9, column=1, padx=10, pady=10)

    def add_watermark(self):
        with Image.open(self.file_path[0].name) as self.image:
            draw = ImageDraw.Draw(self.image)
            font_ = ImageFont.truetype(f"fonts/{self.variable.get()}.ttf", size=int(self.font_size_entry.get()))
            # draw.text((10, 25), text_to_add.get(), font=font_, fill="white")
            if self.rotate_var.get() == 1:
                text = self.text_to_add.get()
                text_width, text_height = draw.textsize(text, font=font_)
                txt_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
                draw_txt = ImageDraw.Draw(txt_img)
                draw_txt.text((0, 0), text=text, font=font_,
                              fill=(255, 255, 255, int((self.opacity_var.get() / 100) * 255)))
                txt_img = txt_img.rotate(int(self.rotate_angle.get()), expand=True)
                self.image.paste(txt_img, self.calculate_position(txt_img.size), txt_img)
            self.image.show()

    def add_using_image(self):
        if self.check_image_upload():
            return None
        if self.sub_text_frame:
            self.sub_text_frame.destroy()
