# === Imports ===
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD  # Drag-and-drop support
from PIL import Image, ImageTk
import numpy as np
import os

# === Helper Functions ===

# Converts text to binary string (8 bits per character)
def message_to_binary(message):
    return ''.join([format(ord(char), '08b') for char in message])

# Converts binary string back to text
def binary_to_message(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])


# 

# Encodes a message into the image and saves the result
def encode_image(input_path, output_path, message):
    img = Image.open(input_path).convert('RGB')
    data = np.array(img)
    binary_message = message_to_binary(message) + '1111111111111110'  

    flat_data = data.flatten()
    if len(binary_message) > len(flat_data):
        raise ValueError("Message too long for this image.")

    for i in range(len(binary_message)):
        flat_data[i] = (flat_data[i] & 0b11111110) | int(binary_message[i])

    encoded_data = flat_data.reshape(data.shape)
    encoded_img = Image.fromarray(encoded_data.astype(np.uint8))
    encoded_img.save(output_path)

# Decodes a hidden message from the image
def decode_image(path):
    img = Image.open(path).convert('RGB')
    data = np.array(img).flatten()
    binary_data = ''.join([str(pixel & 1) for pixel in data])
    end = binary_data.find('1111111111111110')
    if end == -1:
        return "No hidden message found."
    return binary_to_message(binary_data[:end])

# === GUI Application ===
class StegoApp:
    def __init__(self, root):
        self.root = root
        root.title("Image Steganography")
        root.geometry("450x500")

        self.image_path = None
        self.max_capacity = 0

        # --- GUI Widgets ---

        tk.Label(root, text="Secret Message:").pack()
        self.message_entry = tk.Entry(root, width=60)
        self.message_entry.pack(pady=5)
        self.message_entry.bind("<KeyRelease>", self.check_encode_ready)

        self.capacity_label = tk.Label(root, text="")
        self.capacity_label.pack(pady=2)

        self.image_label = tk.Label(root, text="No image selected")
        self.image_label.pack(pady=5)

        self.preview_label = tk.Label(root)
        self.preview_label.pack()

        self.choose_button = tk.Button(root, text="Choose Image to Encode", command=self.choose_image_encode)
        self.choose_button.pack(pady=5)

        self.encode_button = tk.Button(root, text="Encode and Save", command=self.encode_and_save, state="disabled")
        self.encode_button.pack(pady=5)

        tk.Label(root, text="").pack()

        self.decode_button = tk.Button(root, text="Choose Image to Decode", command=self.choose_image_decode)
        self.decode_button.pack(pady=10)

        self.decoded_label = tk.Label(root, text="", wraplength=400, justify="left")
        self.decoded_label.pack()

        # --- Drag and Drop ---
        root.drop_target_register(DND_FILES)
        root.dnd_bind('<<Drop>>', self.handle_drop)

    # === Encoding Section ===

    def choose_image_encode(self):
        path = filedialog.askopenfilename(
            filetypes=[("Lossless Image Files", "*.png *.bmp *.tif *.tiff")]
        )
        if path:
            self.set_encode_image(path)

    def set_encode_image(self, path):
        self.image_path = path
        file_name = os.path.basename(path)
        self.image_label.config(text=f"Selected: {file_name}")

        img = Image.open(path).convert('RGB')
        data = np.array(img)
        self.max_capacity = len(data.flatten()) // 8  # 8 bits = 1 char
        self.capacity_label.config(text=f"Max capacity: {self.max_capacity} characters")

        img.thumbnail((100, 100))
        self.tk_img = ImageTk.PhotoImage(img)
        self.preview_label.config(image=self.tk_img)

        self.check_encode_ready()

    def check_encode_ready(self, event=None):
        msg = self.message_entry.get()
        if self.image_path and msg:
            if len(msg) > self.max_capacity:
                self.encode_button.config(state="disabled")
                self.capacity_label.config(text=f"Message too long! Max: {self.max_capacity} chars")
            else:
                self.encode_button.config(state="normal")
        else:
            self.encode_button.config(state="disabled")

    def encode_and_save(self):
        msg = self.message_entry.get()
        if not self.image_path or not msg:
            messagebox.showerror("Error", "Please select image and enter message.")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG Image", "*.png")]
        )
        if output_path:
            try:
                encode_image(self.image_path, output_path, msg)
                messagebox.showinfo("Success", "Image saved with hidden message.")
                self.reset_encode_fields()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    # === Decoding Section ===

    def choose_image_decode(self):
        path = filedialog.askopenfilename(
            filetypes=[("Lossless Image Files", "*.png *.bmp *.tif *.tiff")]
        )
        if path:
            self.decode_and_show(path)

    def decode_and_show(self, path):
        try:
            message = decode_image(path)
            self.decoded_label.config(text=f"Decoded Message:\n{message}")
            self.reset_encode_fields()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # === Reset UI ===

    def reset_encode_fields(self):
        self.message_entry.delete(0, tk.END)
        self.image_label.config(text="No image selected")
        self.capacity_label.config(text="")
        self.preview_label.config(image="")
        self.encode_button.config(state="disabled")
        self.image_path = None
        self.max_capacity = 0

    # === Drag-and-Drop Handler ===

    def handle_drop(self, event):
        path = event.data.strip().strip("{").strip("}")  # Clean file path
        valid_exts = (".png", ".bmp", ".tif", ".tiff")

        if path.lower().endswith(valid_exts):
            action = messagebox.askquestion("Drag-and-Drop", "Use this image for encoding?")
            if action == "yes":
                self.set_encode_image(path)
            else:
                self.decode_and_show(path)
        else:
            messagebox.showwarning("Unsupported File", "Only .png, .bmp, .tif, .tiff files are supported.")

# === Launch Application ===
if __name__ == "__main__":
    root = TkinterDnD.Tk()    
    app = StegoApp(root)
    root.mainloop()
