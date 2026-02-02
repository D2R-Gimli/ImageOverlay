__version__ = "1.0.0"
__author__ = "Gimli"
__description__ = "A simple python script to overlay jpg/png image over the desktop, change transparency, size and can use a click-through option."

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import ctypes
import sys


class TransparentOverlay:
    def __init__(self, root):
        self.root = root
        self.root.title("ImageOverlay")
        self.root.attributes("-topmost", True)

        # Track whether click-through mode is active
        self.pass_through = False

        # Store original and resized images
        self.original_image = None
        self.tk_image = None

        # Initial window size
        self.root.geometry("800x600+100+100")

        # Canvas fills the entire window
        self.canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Prompt shown before loading an image
        self.prompt = tk.Label(
            self.canvas,
            text="Right-click to open (PNG or JPEG)",
            font=("Segoe UI", 15),
            fg="black",
            bg="white",
            justify="center"
        )
        self.prompt.place(relx=0.5, rely=0.5, anchor="center")

        # Window transparency (1.0 = opaque)
        self.transparency = 1.0
        self.root.attributes("-alpha", self.transparency)

        # Key bindings
        root.bind("<Escape>", lambda e: root.destroy())
        root.bind("<Control-t>", self.toggle_pass_through)
        root.bind("<Up>", self.increase_transparency)
        root.bind("<Down>", self.decrease_transparency)

        # Right-click loads an image
        self.canvas.bind("<Button-3>", self.open_image)

        # Bind resize to the CANVAS, not the window
        self.canvas.bind("<Configure>", self.on_resize)

        # Used for throttling resize events
        self._resize_after = None

    # -----------------------------
    # Resize Handling
    # -----------------------------
    def on_resize(self, event):
        """Throttle resize events so the image isn't resized too often."""
        if not self.original_image:
            return

        # Cancel any pending resize
        if self._resize_after:
            self.root.after_cancel(self._resize_after)

        # Schedule a new resize 50ms later
        self._resize_after = self.root.after(50, self.update_image)

    # -----------------------------
    # Image Loading
    # -----------------------------
    def open_image(self, event=None):
        """Open file dialog and load an image."""
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
        )

        if path:
            self.load_image(path)

    def load_image(self, path):
        """Load the selected image and convert to RGBA."""
        try:
            self.original_image = Image.open(path).convert("RGBA")
            self.prompt.place_forget()  # Hide the prompt
            self.update_image()
        except Exception as e:
            print("Failed to load image:", e)

    # -----------------------------
    # Image Resizing + Drawing
    # -----------------------------
    def update_image(self):
        """Resize the image to match the canvas size and redraw it."""
        if not self.original_image:
            return

        # Get canvas size (correct during resizing)
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w < 2 or h < 2:
            return

        # Resize using high-quality filter
        resized = self.original_image.resize((w, h), Image.LANCZOS)

        # Convert to Tk image
        self.tk_image = ImageTk.PhotoImage(resized)

        # Clear canvas and draw new image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        # Reapply transparency
        self.root.attributes("-alpha", self.transparency)

    # -----------------------------
    # Transparency Controls
    # -----------------------------
    def increase_transparency(self, event=None):
        self.transparency = min(1.0, self.transparency + 0.05)
        self.root.attributes("-alpha", self.transparency)

    def decrease_transparency(self, event=None):
        self.transparency = max(0.1, self.transparency - 0.05)
        self.root.attributes("-alpha", self.transparency)

    # -----------------------------
    # Click-Through Mode
    # -----------------------------
    def toggle_pass_through(self, event=None):
        """Enable or disable click-through mode."""
        self.pass_through = not self.pass_through
        self.set_click_through(self.pass_through)
        print(f"Pass-through {'enabled' if self.pass_through else 'disabled'}")

    def set_click_through(self, enable):
        """Use Windows API to toggle WS_EX_TRANSPARENT."""
        hwnd = ctypes.windll.user32.FindWindowW(None, "ImageOverlay")
        if hwnd:
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x80000
            WS_EX_TRANSPARENT = 0x20

            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)

            if enable:
                style |= WS_EX_LAYERED | WS_EX_TRANSPARENT
            else:
                style &= ~WS_EX_TRANSPARENT
                style |= WS_EX_LAYERED

            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)


# -----------------------------
# Program Entry Point
# -----------------------------
if __name__ == "__main__":
    # Only works on Windows
    if sys.platform != "win32":
        print("This program only works on Windows.")
        sys.exit()

    # Enable DPI awareness for sharp rendering
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

    root = tk.Tk()
    app = TransparentOverlay(root)
    root.mainloop()
