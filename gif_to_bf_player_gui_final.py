# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageSequence, ImageTk
import os

# =========================================================
# Image preprocessing
# =========================================================

def preprocess_preview(frame, w, h):
    frame = frame.convert("RGB")
    frame = frame.resize((w, h), Image.LANCZOS)
    return frame

def preprocess_bf(frame, w, h):
    frame = frame.convert("RGB")
    frame = frame.resize((w, h), Image.LANCZOS)
    frame = frame.quantize(colors=256, method=Image.MEDIANCUT)
    return list(frame.getdata())

# =========================================================
# Estimation logic
# =========================================================

def estimate(frames, w, h):
    if len(frames) < 2:
        return 0, 0, "N/A"

    total = w * h * len(frames)
    changed = 0

    prev = frames[0]
    for cur in frames[1:]:
        for a, b in zip(prev, cur):
            if a != b:
                changed += 1
        prev = cur

    ratio = changed / total
    est_bytes = int(changed * 14 * 1.2)

    pixels = w * h
    if pixels < 2000:
        speed = "Fast"
    elif pixels < 5000:
        speed = "Medium"
    elif pixels < 10000:
        speed = "Slow"
    else:
        speed = "Very Slow"

    return est_bytes, ratio, speed

# =========================================================
# Brainfuck generator
# =========================================================

def generate_bf(gif_path, w, h, max_frames):
    bf = []
    cell = 0

    def set_cell(v):
        nonlocal cell
        d = v - cell
        bf.append("+" * d if d > 0 else "-" * (-d))
        cell = v

    def emit(v):
        set_cell(v)
        bf.append(".")

    def esc(s):
        return [27] + [ord(c) for c in s]

    def clear():
        return esc("[H") + esc("[2J")

    def cursor(r, c):
        return esc(f"[{r};{c}H")

    def bg(c):
        return esc(f"[48;5;{c}m")

    def reset():
        return esc("[0m")

    im = Image.open(gif_path)

    frames = []
    for i, f in enumerate(ImageSequence.Iterator(im)):
        if i >= max_frames:
            break
        frames.append(preprocess_bf(f, w, h))

    prev = None

    for b in clear():
        emit(b)

    for frame in frames:
        if prev is None:
            for i, col in enumerate(frame):
                r = i // w + 1
                c = i % w + 1
                for b in cursor(r, c): emit(b)
                for b in bg(col): emit(b)
                emit(ord(" "))
        else:
            for i, (a, bcol) in enumerate(zip(prev, frame)):
                if a != bcol:
                    r = i // w + 1
                    c = i % w + 1
                    for b in cursor(r, c): emit(b)
                    for b in bg(bcol): emit(b)
                    emit(ord(" "))

        for b in reset():
            emit(b)

        prev = frame

    out = os.path.join(os.path.dirname(gif_path), "video_player.bf")
    with open(out, "w", encoding="ascii") as f:
        f.write("".join(bf))

    return out

# =========================================================
# GUI callbacks
# =========================================================

def browse():
    p = filedialog.askopenfilename(filetypes=[("GIF files", "*.gif")])
    if p:
        gif_path.set(p)
        load_preview()

def load_preview():
    try:
        w = int(width.get())
        h = int(height.get())
    except:
        return

    path = gif_path.get()
    if not os.path.isfile(path):
        return

    im = Image.open(path)
    preview_imgs.clear()
    raw_frames.clear()

    for i, f in enumerate(ImageSequence.Iterator(im)):
        if i >= 5:
            break
        pimg = preprocess_preview(f, w, h)
        preview_imgs.append(ImageTk.PhotoImage(pimg))
        raw_frames.append(preprocess_bf(f, w, h))

    if preview_imgs:
        preview_label.config(image=preview_imgs[0])

    update_estimate()

def update_estimate():
    try:
        w = int(width.get())
        h = int(height.get())
    except:
        return

    size, ratio, speed = estimate(raw_frames, w, h)
    est_text.set(
        f"Estimated BF size: {size/1024/1024:.2f} MB\n"
        f"Pixel change ratio: {ratio*100:.1f}%\n"
        f"Playback speed: {speed}"
    )

def run_generate():
    path = gif_path.get()
    if not os.path.isfile(path):
        messagebox.showerror("Error", "Select a GIF first")
        return

    try:
        w = int(width.get())
        h = int(height.get())
        m = int(maxframes.get())
    except:
        messagebox.showerror("Error", "Invalid numeric input")
        return

    out = generate_bf(path, w, h, m)
    messagebox.showinfo("Done", f"Brainfuck file created:\n{out}")

# =========================================================
# GUI layout
# =========================================================

root = tk.Tk()
root.title("GIF to Brainfuck ANSI Video Player")

gif_path = tk.StringVar()
width = tk.StringVar(value="80")
height = tk.StringVar(value="48")
maxframes = tk.StringVar(value="28")
est_text = tk.StringVar(value="Estimation unavailable")

preview_imgs = []
raw_frames = []

pad = {"padx": 6, "pady": 4}

tk.Label(root, text="GIF file").grid(row=0, column=0, sticky="e", **pad)
tk.Entry(root, textvariable=gif_path, width=40).grid(row=0, column=1, **pad)
tk.Button(root, text="Browse", command=browse).grid(row=0, column=2, **pad)

tk.Label(root, text="Width").grid(row=1, column=0, sticky="e", **pad)
tk.Entry(root, textvariable=width, width=8).grid(row=1, column=1, sticky="w", **pad)

tk.Label(root, text="Height").grid(row=2, column=0, sticky="e", **pad)
tk.Entry(root, textvariable=height, width=8).grid(row=2, column=1, sticky="w", **pad)

tk.Label(root, text="Max Frames").grid(row=3, column=0, sticky="e", **pad)
tk.Entry(root, textvariable=maxframes, width=8).grid(row=3, column=1, sticky="w", **pad)

tk.Label(root, text="Preview").grid(row=1, column=2, **pad)
preview_label = tk.Label(root, relief="sunken", width=160, height=120)
preview_label.grid(row=2, column=2, rowspan=3, **pad)

tk.Label(root, textvariable=est_text, justify="left").grid(
    row=5, column=0, columnspan=3, sticky="w", **pad
)

tk.Button(
    root,
    text="Generate Brainfuck Player",
    command=run_generate,
    bg="#4CAF50",
    fg="white"
).grid(row=6, column=0, columnspan=3, pady=10)

root.mainloop()
