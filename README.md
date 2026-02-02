# 🖼️ ImageOverlay  
A lightweight Windows-only tool that displays any PNG or JPEG as a resizable, semi-transparent overlay on your desktop. Perfect for artists, designers, and anyone who needs a reference image floating above other windows.

---

## ✨ Features

- 🔝 Always on top — the overlay stays above all other windows  
- 🖼️ Right‑click to load an image (PNG/JPG/JPEG)  
- 🔍 Auto-resizing — image scales smoothly with the window  
- 🌫️ Adjustable transparency using arrow up/down keys  
- 🖱️ Click‑through mode (experimental) — interact with apps behind the overlay  
- ⚡ Resize throttling for smooth performance  
- 🖥️ High‑DPI aware for crisp rendering  

---

## 🧩 Requirements

- Windows OS only  
- Python 3.8+  
- Dependencies:  
  - tkinter (included with Python on Windows)  
  - Pillow (install via pip)

Install Pillow:

```
pip install pillow  
```

---

## 📦 Installation

Download the python file.

Install dependencies:

```
pip install pillow  
```

---

## ▶️ Usage

Run the program:

```
python ImageOverlay.py 
```

When launched, you’ll see a blank window with a message prompting you to load an image.

### 🖱️ Basic Controls

| Action | How |
|-------|-----|
| Load image | Right‑click anywhere |
| Exit program | Esc |
| Increase opacity | ↑ Up Arrow |
| Decrease opacity | ↓ Down Arrow |
| Toggle click‑through mode | Ctrl + T |

---

## 🎛️ How It Works

### 🪟 Window & Canvas
- The window is always on top.  
- Transparency is controlled via the `-alpha` attribute.  
- A full‑window Tkinter canvas displays the image.  
- A prompt appears until an image is loaded.

### 🖼️ Image Handling
- Images are loaded with Pillow and converted to RGBA.  
- The image is resized to match the canvas using high‑quality LANCZOS filtering.  
- Resize events are throttled to avoid lag.

### 🖱️ Click‑Through Mode
The program uses Windows API calls (via ctypes) to toggle:

- WS_EX_TRANSPARENT  
- WS_EX_LAYERED  

This allows mouse clicks to pass through the overlay to windows behind it.

⚠️ Note:  
The script currently searches for a window titled **"ImageOverlay"** when enabling click‑through mode.  
The Tkinter window title is **"ImageOverlay"**.  
These should match for click‑through to work reliably.

---

## ⚠️ Limitations

- Windows only — exits immediately on other platforms  
- Canvas background is opaque — transparency applies to the whole window  
- Click‑through applies to the entire window, not transparent regions only  

---

## 🛠️ Future Ideas

- Toolbar for loading images & adjusting opacity  
- Aspect‑ratio lock  
- Per‑pixel click‑through  
- Config file for default settings  
- Hotkeys for switching images  

---

## 🤝 Contributing

Pull requests and issues are welcome.  
If you have ideas or improvements, feel free to open an issue.

---