import os
import tkinter as tk
from tkinter import filedialog

import customtkinter
from PIL import Image, ImageEnhance, ImageTk


class ImageProcessor:
    def __init__(self, image_path):
        self.original_image = Image.open(image_path)
        self.image = self.original_image.copy()
        self.brightness_enhancer = ImageEnhance.Brightness(self.image)
        self.contrast_enchancer = ImageEnhance.Contrast(self.image)
        self.saturation_enchancer = ImageEnhance.Color(self.image)

    def get_image(self):
        return self.image

    def update_image(self):
        self.image = self.original_image.copy()

    def apply_brightness(self, value):
        self.image = self.brightness_enhancer.enhance(value)

    def apply_contrast(self, value):
        self.image = self.contrast_enchancer.enhance(value)

    def apply_saturation(self, value):
        self.image = self.saturation_enchancer.enhance(value)

    def save_image(self, file_path):
        self.image.save(file_path)


class SliderFactory:
    def create_slider(self, parent, label, command, row_number):
        self.slider_label = customtkinter.CTkLabel(parent, text=label)
        self.slider_label.grid(row=row_number, column=0, pady=10, sticky="nsew")

        self.slider = customtkinter.CTkSlider(parent, from_=0, to=2.0, command=command)
        self.slider.configure(number_of_steps=100)
        self.slider.grid(row=row_number + 1, column=0, padx=10, pady=10, sticky="nsew")
        return self.slider


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Photo Master")
        self.geometry("1280x720")
        self.minsize(800, 600)

        self.slider_factory = SliderFactory()
        self.image_processor = None

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="Photo Master",
            compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Edit photo",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.home_button_event,
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="About",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.frame_2_button_event,
        )
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.set("System")
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.home_frame.grid_rowconfigure(0, weight=1)
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.photo_frame = customtkinter.CTkFrame(self.home_frame)
        self.photo_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.photo_frame.grid_rowconfigure(0, weight=1)
        self.photo_frame.grid_columnconfigure(0, weight=1)
        self.image_label = customtkinter.CTkLabel(self.photo_frame, text="")
        self.image_label.grid(row=0, column=0, padx=0, pady=0)
        self.tool_frame = customtkinter.CTkFrame(self.home_frame, width=300)
        self.tool_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")

        self.upload_photo_button = customtkinter.CTkButton(
            self.tool_frame, text="Upload photo", command=self.load_image
        )
        self.upload_photo_button.grid(
            row=0, column=0, padx=20, pady=(20, 10), sticky="ew"
        )

        self.brightness_slider = self.slider_factory.create_slider(
            self.tool_frame, "Яркость", self.update_brightness, 1
        )
        self.contrast_slider = self.slider_factory.create_slider(
            self.tool_frame, "Контрастность", self.update_contrast, 3
        )
        self.saturation_slider = self.slider_factory.create_slider(
            self.tool_frame, "Насыщенность", self.update_saturation, 5
        )

        self.discard_button = customtkinter.CTkButton(
            self.tool_frame, text="Discard changes", command=self.discard_changes
        )
        self.tool_frame.grid_rowconfigure(7, weight=1)
        # self.tool_frame.grid_rowconfigure(8, weight=1)

        self.discard_button.grid(row=7, column=0, padx=20, pady=(10, 10), sticky="sew")

        self.save_button = customtkinter.CTkButton(
            self.tool_frame, text="Save image", command=self.save_image
        )
        self.save_button.grid(row=8, column=0, padx=20, pady=(0, 20), sticky="sew")

        # create second frame
        self.second_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )
        self.second_frame.grid_rowconfigure(0, weight=1)
        self.second_frame.grid_columnconfigure(0, weight=1)
        self.about_frame = customtkinter.CTkFrame(self.second_frame, width=600)
        self.about_frame.grid_rowconfigure(0, weight=1)
        self.about_frame.grid_columnconfigure(0, weight=1)
        self.about_frame.grid(
            row=0, column=0, columnspan=3, padx=20, pady=20, sticky="ns"
        )
        self.about_text = customtkinter.CTkTextbox(
            self.about_frame,
            width=900,
            font=(tuple, 18),
            fg_color="transparent",
            activate_scrollbars=False,
        )
        self.about_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.about_text.insert(
            "0.0",
            "Данное приложение было разработано на языке Python с помощью библиотеки Custom Tkinter.\nОсновная задача данного приложения быстрое и простое редактирование базовых параметров любого изображения.\nРуководство использования:\n1. Перейдите во вкладку 'Edit photo';\n2. Далее нажмите на кнопку в правом верхнем углу 'Upload photo';\n3. После этого вам будет доступно редактирование базовых параметров вашего изображения\n\nДанное приложение было разработано для учебы, в частности для предмета 'Объектно-ориентированнео программирование', студентом 421-4 группы, Лошмановым Даниилом",
        )
        self.about_text.configure(state="disabled")

        # select default frame
        self.select_frame_by_name("home")

    def load_image(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Изображения", "*.png;*.jpg;*.jpeg")]
        )
        if self.file_path:
            self.image_processor = ImageProcessor(self.file_path)
            self.image = self.image_processor.get_image()
            self.parent_frame_width = self.photo_frame.winfo_width()
            self.parent_frame_height = self.photo_frame.winfo_height()
            self.parent_frame_aspect_ratio = (
                self.parent_frame_width / self.parent_frame_height
            )

            # Определение желаемой ширины и высоты картинки с сохранением пропорций
            if self.image.width / self.image.height >= self.parent_frame_aspect_ratio:
                self.desired_width = self.parent_frame_width
                self.desired_height = int(
                    self.parent_frame_width / self.image.width * self.image.height
                )
            else:
                self.desired_height = self.parent_frame_height
                self.desired_width = int(
                    self.parent_frame_height / self.image.height * self.image.width
                )

            self.photo = customtkinter.CTkImage(
                light_image=self.image,
                dark_image=self.image,
                size=(self.desired_width, self.desired_height),
            )
            self.image_label.configure(image=self.photo)

    def update_image(self):
        # self.image_processor.update_image()
        new_image = self.image_processor.get_image()
        if self.photo is not None:
            self.photo.configure(light_image=new_image, dark_image=new_image)

    def update_brightness(self, value):
        self.image_processor.update_image()
        if self.image_processor is None:
            return
        self.image_processor.apply_brightness(float(value))
        self.update_image()

    def update_contrast(self, value):
        self.image_processor.update_image()
        if self.image_processor is None:
            return
        self.image_processor.apply_contrast(float(value))
        self.update_image()

    def update_saturation(self, value):
        self.image_processor.update_image()
        if self.image_processor is None:
            return
        self.image_processor.apply_saturation(float(value))
        self.update_image()

    def discard_changes(self):
        # self.image_processor.update_image()
        self.image_processor.apply_brightness(1.0)
        self.image_processor.apply_contrast(1.0)
        self.image_processor.apply_saturation(1.0)
        self.update_image()
        self.brightness_slider.set(1.0)
        self.contrast_slider.set(1.0)
        self.saturation_slider.set(1.0)

    def save_image(self):
        image_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Изображения", "*.png;*.jpg;*.jpeg")],
        )
        if image_path:
            self.image_processor.save_image(image_path)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent"
        )
        self.frame_2_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_2" else "transparent"
        )

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
