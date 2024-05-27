import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from pathlib import Path


def process_image(filepath, height):
    img = Image.open(filepath)
    # Calculate the new width maintaining the aspect ratio
    aspect_ratio = img.width / img.height
    new_width = int(aspect_ratio * height)
    img = img.resize((new_width, height), Image.LANCZOS)  # Use Image.LANCZOS for high quality resizing
    return img


def save_image(img, output_path, format):
    img.save(output_path, format=format, quality=10, optimize=True)


def compress_to_webp(filepath, height, suffix, output_dir):
    img = process_image(filepath, height)
    base_name, _ = os.path.splitext(os.path.basename(filepath))
    output_path = os.path.join(output_dir, base_name + suffix + ".webp")
    save_image(img, output_path, "WEBP")
    return output_path


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor webp")
        self.root.geometry("800x900")
        # Centrar la ventana en la pantalla
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x_offset = (self.root.winfo_screenwidth() - width) // 2
        y_offset = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"+{x_offset}+{y_offset}")
        self.label = tk.Label(root, text="Choose an option:")
        self.label.pack(pady=10)

        self.img_button = tk.Button(root, text="Process Images", command=self.process_images)
        self.img_button.pack(pady=5)

        self.option_var = tk.StringVar(value="icono")

        self.icono_radio = tk.Radiobutton(root, text="Icono", variable=self.option_var, value="icono", command=self.update_preview)
        self.icono_radio.pack(pady=5)

        self.fondo_radio = tk.Radiobutton(root, text="Fondo", variable=self.option_var, value="fondo", command=self.update_preview)
        self.fondo_radio.pack(pady=5)

        self.producto_radio = tk.Radiobutton(root, text="Producto", variable=self.option_var, value="producto", command=self.update_preview)
        self.producto_radio.pack(pady=5)

        self.tarjeta_radio = tk.Radiobutton(root, text="Tarjeta", variable=self.option_var, value="tarjeta", command=self.update_preview)
        self.tarjeta_radio.pack(pady=5)

        self.filepath = None
        self.img_preview = None
        self.img_label = None
        self.output_dir = tk.StringVar(value=str(Path.home() / "Downloads"))  # Set default output directory to Downloads

        self.setup_output_dir_entry()

    def setup_output_dir_entry(self):
        self.output_dir_label = tk.Label(self.root, text="Output Directory:")
        self.output_dir_label.pack(pady=5)

        self.output_dir_entry = tk.Entry(self.root, textvariable=self.output_dir, width=50)
        self.output_dir_entry.pack(pady=5)

        self.output_dir_button = tk.Button(self.root, text="Browse", command=self.browse_output_dir)
        self.output_dir_button.pack(pady=5)

    def browse_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)

    def process_images(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.gif;*.tif;*.webp")])
        if self.filepath:
            self.update_preview()

    def get_height_and_suffix_by_option(self, option):
        if option == "icono":
            return 400, "-icon"
        elif option == "fondo":
            return 1280, "-back"
        elif option == "producto":
            return 500, "-product"
        elif option == "tarjeta":
            return 1280, "-card"

    def update_preview(self):
        if self.filepath:
            option = self.option_var.get()
            height, _ = self.get_height_and_suffix_by_option(option)
            img = process_image(self.filepath, height)
            img.thumbnail((400, 400))  # Thumbnail for preview purposes
            self.img_preview = ImageTk.PhotoImage(img)

            if self.img_label:
                self.img_label.config(image=self.img_preview)
            else:
                self.img_label = tk.Label(self.root, image=self.img_preview)
                self.img_label.pack(pady=10)

            self.save_options(height)

    def save_options(self, height):
        if hasattr(self, 'options_frame'):
            self.options_frame.destroy()

        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack(pady=10)

        option = self.option_var.get()
        _, suffix = self.get_height_and_suffix_by_option(option)

        save_button = tk.Button(self.options_frame, text="Save as WEBP", command=lambda: self.save_image(height, suffix))
        save_button.grid(row=0, column=0, padx=10)

    def save_image(self, height, suffix):
        output_dir = self.output_dir.get()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  # Create directory if it doesn't exist

        output_path = compress_to_webp(self.filepath, height, suffix, output_dir)
        self.display_message(f"Image saved as: {output_path}")

    def display_message(self, message):
        if hasattr(self, 'message_label'):
            self.message_label.destroy()

        self.message_label = tk.Label(self.root, text=message)
        self.message_label.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
