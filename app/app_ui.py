from tkinter import *
from tkinter.filedialog import askopenfilename

import numpy as np
from PIL import Image, ImageTk

import filter

root = Tk()
root.title('Convolution Linear Filtering Application')
window_width = 1200
window_height = 900

LOW_FILTER_OPTION = (('Average filter', 'average_filter'), ('Gaussian filter', 'gaussian_filter'))
HIGH_FILTER_OPTION = (('High pass filter', 'high_pass_filter'), ('Sharpening', 'sharpening'))
GRADIENT_FILTER_OPTION = (('Horizontal edge detect', 'horizontal_edge_detect'),
                          ('Vertical edge detect', 'vertical_edge_detect'))
# set the position of the window to the center
root.geometry()


class AppUI:
    def __init__(self, root: Tk):
        self.root = root

        self.button_frame = Frame(root, width=800)
        self.button_frame.pack()

        self.option_filter_frame = Frame(root, width=800)
        self.radio_button_var = StringVar()
        self.radio_button_list: list[Radiobutton] = []
        self.radio_options = LOW_FILTER_OPTION
        self.low_pass_filter_size = Entry(self.option_filter_frame, width=5)
        self.low_pass_filter_size_label = Label(self.option_filter_frame, text="Input size")
        self.low_pass_filter_size_label.pack(side=LEFT, padx=5, pady=5)
        self.low_pass_filter_size.pack(padx=5, pady=10, side=LEFT)
        for option in self.radio_options:
            r = Radiobutton(
                self.option_filter_frame,
                text=option[0],
                value=option[1],
                variable=self.radio_button_var,
                takefocus=0
            )
            self.radio_button_list.append(r)
            r.pack(padx=5, pady=5, side=LEFT)
        self.option_filter_frame.pack()
        self.original_frame = Frame(root, width=600, height=600, highlightthickness=2, highlightbackground="blue")
        self.original_frame.pack(side=LEFT, padx=30)
        self.filter_frame = Frame(root, width=600, height=600, highlightthickness=2, highlightbackground="green")
        self.filter_frame.pack(side=RIGHT, padx=30)

        self.original_image = None
        self.original_image_path_label: Label = None
        self.original_image_label: Label = None
        self.original_photo_image = None

        self.filter_image = None
        self.filter_image_label: Label = None

        self.choose_file = Button(self.button_frame, text="Choose file", command=self.on_choose_image_button)
        self.choose_file.pack(side=LEFT)
        self.filter_button = Button(self.button_frame, text="Filter", command=self.on_filter)
        self.filter_button.pack(side=RIGHT)
        self.dropdown_var = StringVar(self.button_frame)
        self.dropdown_var.set("Low Pass Filter")  # default value
        w = OptionMenu(self.button_frame, self.dropdown_var, "Low Pass Filter", "High Pass Filter", "Gradient Filter",
                       command=self.add_radio_button)
        w.pack(side=RIGHT)

    def add_radio_button(self, filter_type):
        if filter_type == "Low Pass Filter":
            self.radio_options = LOW_FILTER_OPTION
            if self.low_pass_filter_size is None and self.low_pass_filter_size_label is None:
                self.low_pass_filter_size = Entry(self.option_filter_frame, width=5)
                self.low_pass_filter_size_label = Label(self.option_filter_frame, text="Input size")
                self.low_pass_filter_size_label.pack(side=LEFT, padx=5, pady=5)
                self.low_pass_filter_size.pack(padx=5, pady=10, side=LEFT)
        if filter_type == "High Pass Filter":
            self.radio_options = HIGH_FILTER_OPTION
            if self.low_pass_filter_size_label is not None and self.low_pass_filter_size is not None:
                self.low_pass_filter_size_label.destroy()
                self.low_pass_filter_size.destroy()
            self.low_pass_filter_size_label = None
            self.low_pass_filter_size = None
        if filter_type == "Gradient Filter":
            self.radio_options = GRADIENT_FILTER_OPTION
            if self.low_pass_filter_size_label is not None and self.low_pass_filter_size is not None:
                self.low_pass_filter_size_label.destroy()
                self.low_pass_filter_size.destroy()
            self.low_pass_filter_size_label = None
            self.low_pass_filter_size = None

        if len(self.radio_button_list) > 0:
            for r_btn in self.radio_button_list:
                r_btn.destroy()
        for option in self.radio_options:
            r = Radiobutton(
                self.option_filter_frame,
                text=option[0],
                value=option[1],
                variable=self.radio_button_var,
                takefocus=0
            )
            self.radio_button_list.append(r)
            r.pack(padx=5, pady=5, side=LEFT)

    def on_filter(self):
        filter_type = self.dropdown_var.get()

        def show_filter_image(img):
            if self.filter_image_label is None:
                Label(self.filter_frame, text="Filter Image").pack()

            if self.filter_image_label is not None:
                self.filter_image_label.destroy()
            self.filter_image = ImageTk.PhotoImage(img)
            self.filter_image_label = Label(self.filter_frame, image=self.filter_image)
            self.filter_image_label.pack()

        img_temp = None
        if filter_type == "Low Pass Filter":
            if self.radio_button_var.get() == "average_filter":
                img_temp = filter.average_filter(np.asarray(self.original_image), int(self.low_pass_filter_size.get()))
            elif self.radio_button_var.get() == "gaussian_filter":
                img_temp = filter.gaussian_filter(np.asarray(self.original_image), int(self.low_pass_filter_size.get()))
        if filter_type == "High Pass Filter":
            if self.radio_button_var.get() == "sharpening":
                img_temp = filter.sharpening(np.asarray(self.original_image))
            elif self.radio_button_var.get() == "high_pass_filter":
                img_temp = filter.hight_pass_filter(np.asarray(self.original_image))
        if filter_type == "Gradient Filter":
            if self.radio_button_var.get() == "vertical_edge_detect":
                img_temp = filter.vertical_edge_detect(np.asarray(self.original_image))
            elif self.radio_button_var.get() == "horizontal_edge_detect":
                img_temp = filter.horizontal_edge_detect(np.asarray(self.original_image))
        show_filter_image(Image.fromarray(img_temp))

    def on_choose_image_button(self):
        try:
            image_path = askopenfilename(
                initialdir='C:/Users/toquq/Documents',
                title="Select a image file",
                filetypes=(('PNG files', '.png'), ('All files', '*.*'))
            )
            self.original_image = Image.open(image_path)
            self.original_photo_image = ImageTk.PhotoImage(self.original_image)
            if self.original_image_label is not None:
                self.original_image_label.destroy()
                self.original_image_path_label.destroy()
            self.original_image_path_label = Label(self.original_frame, text="Original Image")
            self.original_image_path_label.pack()
            self.original_image_label = Label(self.original_frame, image=self.original_photo_image)
            self.original_image_label.pack()
        except Exception as e:
            pass

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    AppUI(root).run()
