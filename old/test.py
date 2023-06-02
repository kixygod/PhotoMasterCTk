import tkinter as tk

from PIL import Image, ImageEnhance, ImageTk


class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")

        # Создание ползунков
        self.brightness_scale = tk.Scale(
            self.root,
            label="Brightness",
            from_=0.1,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            command=self.update_image,
        )
        self.brightness_scale.pack()

        self.contrast_scale = tk.Scale(
            self.root,
            label="Contrast",
            from_=0.1,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            command=self.update_image,
        )
        self.contrast_scale.pack()

        self.saturation_scale = tk.Scale(
            self.root,
            label="Saturation",
            from_=0.1,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            command=self.update_image,
        )
        self.saturation_scale.pack()

        # Загрузка и отображение исходного изображения
        self.original_image = Image.open("photo.png")
        self.tk_image = ImageTk.PhotoImage(self.original_image)
        self.image_label = tk.Label(self.root, image=self.tk_image)
        self.image_label.pack()

    def update_image(self, event=None):
        # Получение значений ползунков
        brightness = self.brightness_scale.get()
        contrast = self.contrast_scale.get()
        saturation = self.saturation_scale.get()

        # Создание объекта ImageEnhance и изменение параметров изображения
        enhancer = ImageEnhance.Brightness(self.original_image)
        image_brightness = enhancer.enhance(brightness)

        enhancer = ImageEnhance.Contrast(image_brightness)
        image_contrast = enhancer.enhance(contrast)

        enhancer = ImageEnhance.Color(image_contrast)
        image_final = enhancer.enhance(saturation)

        # Обновление отображения изображения
        self.tk_image = ImageTk.PhotoImage(image_final)
        self.image_label.config(image=self.tk_image)


if __name__ == "__main__":
    root = tk.Tk()
    editor = ImageEditor(root)
    root.mainloop()
