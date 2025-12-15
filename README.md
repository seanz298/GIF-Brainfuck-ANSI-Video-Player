# GIF → Brainfuck ANSI Video Player

A GUI tool that converts a GIF into a **self-contained Brainfuck program** which plays an **ANSI 256-color video directly in the terminal**.

No external player.
No runtime dependencies beyond a Brainfuck interpreter.
The Brainfuck program **contains both the video data and the player logic**.

---

## Features

- GUI-based workflow (Tkinter)
- Select any GIF file
- Adjustable output resolution (Width / Height)
- Adjustable maximum frame count
- High-quality downsampling (LANCZOS)
- ANSI 256-color output
- Cursor-based delta rendering (only redraw changed pixels)
- Built-in Brainfuck “player” (ANSI escape sequences)
- Live preview of downsampled frames
- Estimated Brainfuck file size and playback speed
- Output is a single `.bf` file

---

## What This Project Does (Precisely)

This tool converts a GIF into:

```
GIF
 → downsample + antialias
 → 256-color quantization
 → frame differencing (delta rendering)
 → ANSI escape sequences
 → Brainfuck source code
```

Running the generated Brainfuck program:

```
bf video_player.bf
```

will **play the video in a terminal** that supports ANSI 256 colors.

---

## Requirements

### Python side (generator)

- Python 3.8+
- Pillow

Install dependency:

```bash
pip install pillow
```

### Runtime (player)

- Any Brainfuck interpreter with:
  - 8-bit cells (0–255 wraparound)
- Terminal with ANSI 256-color support:
  - Linux terminal
  - macOS Terminal / iTerm2
  - Windows Terminal

---

## How to Run the GUI

```bash
python gif_to_bf_player_gui_final.py
```

---

## GUI Usage

1. Click **Browse** and select a GIF file
2. Set:
   - Width (recommended: 64–80)
   - Height (recommended: 40–50)
   - Max Frames (recommended: 10–30)
3. Observe:
   - Live preview of downsampled frames
   - Estimated Brainfuck file size
   - Estimated playback speed
4. Click **Generate Brainfuck Player**

---

## Output Location

The generated file is always saved **next to the selected GIF**:

```
video_player.bf
```

Example:

```
C:\Users\...\Desktop\example.gif
C:\Users\...\Desktop\video_player.bf
```

---

## How to Play the Generated Video

 using a Python Brainfuck interpreter:

```bash
python bf.py < video_player.bf
```

---

## Performance Notes (Important)

This is intentionally extreme.

Brainfuck is used as:
- A data container
- A control stream
- A terminal renderer driver

### Practical limits

| Resolution | Experience |
|----------|-----------|
| 40×30 | Smooth |
| 64×48 | Acceptable |
| 80×48 | Slow but watchable |
| 200×200 | Not practical |

The GUI estimation panel exists to help you **avoid unusable configurations**.

---

## Why Delta Rendering Matters

Instead of clearing and redrawing the whole screen each frame, the generator:

- Compares each frame to the previous frame
- Only emits cursor movement + color output for changed pixels

This reduces Brainfuck output size and runtime by **70–90%** for typical GIFs.

---

## Known Limitations

- No audio
- No true frame timing (Brainfuck uses busy loops)
- Playback speed depends on:
  - Interpreter performance
  - Terminal rendering speed
- Very large resolutions will be extremely slow

---

## Project Philosophy

This project is intentionally **not practical**.

It explores:
- The expressive limits of Brainfuck
- ANSI terminals as a rendering backend
- How far preprocessing and system design can push an esoteric language

Brainfuck is not a video format.
That’s the point.

---

## License

MIT License

---

## Credits

- Brainfuck language: Urban Müller
- ANSI escape sequences: terminal pioneers
- Pillow: Python Imaging Library fork
- Tkinter: built-in GUI toolkit
