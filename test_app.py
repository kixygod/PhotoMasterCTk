import unittest

from app import App, ImageProcessor, SliderFactory


class TestApp(unittest.TestCase):
    def test_empty_image(self):
        app = App()
        self.assertEqual(app.image_label.cget("text"), "")

    def test_all_sliders(self):
        app = App()
        self.assertEqual(app.brightness_slider.get(), 1.0)
        self.assertEqual(app.contrast_slider.get(), 1.0)
        self.assertEqual(app.saturation_slider.get(), 1.0)
