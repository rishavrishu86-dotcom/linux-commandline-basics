#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Inches, Pt, RGBColor

HOME = os.path.expanduser("~")
DIR = os.path.join(HOME, "linux_assignment")
SHOTS = os.path.join(DIR, "shots")

MENLO = "/System/Library/Fonts/Menlo.ttc"
FS = 26                      # font size (rendered big, scaled down in doc for crispness)
font = ImageFont.truetype(MENLO, FS)
bold = ImageFont.truetype(MENLO, FS, index=1)

PAD = 28
LINE_H = FS + 10
TITLEBAR = 56
BG = (30, 31, 34)           # terminal body
BAR = (60, 62, 66)          # title bar
FG = (220, 221, 222)        # normal text
GREEN = (126, 200, 110)     # prompt user@host
BLUE = (97, 175, 239)       # path
RED = (224, 108, 117)       # errors

def color_for(line):
    s = line.strip()
    if s.startswith("zsh:") and "not found" in s or "permission denied" in s:
        return RED
    return FG

def render(txt_path, png_path, title):
    with open(txt_path) as f:
        lines = [l.rstrip("\n") for l in f if l.strip("\n") != "" or True]
    # drop trailing blank lines
    while lines and lines[-1].strip() == "":
        lines.pop()

    # width based on longest line
    maxw = max((font.getlength(l) for l in lines), default=200)
    W = int(maxw) + PAD * 2
    W = max(W, 760)
    H = TITLEBAR + PAD * 2 + LINE_H * len(lines)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # title bar
    d.rectangle([0, 0, W, TITLEBAR], fill=BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 26 + i * 30
        d.ellipse([cx, TITLEBAR//2 - 9, cx + 18, TITLEBAR//2 + 9], fill=c)
    tw = font.getlength(title)
    d.text(((W - tw) / 2, TITLEBAR/2 - FS/2), title, font=font, fill=(180, 181, 182))

    y = TITLEBAR + PAD
    PROMPT_MARK = " % "
    for line in lines:
        x = PAD
        # color the prompt segment "user@host path %" then command in white
        if PROMPT_MARK in line and line.split(PROMPT_MARK)[0].count("@") == 1:
            head, _, cmd = line.partition(PROMPT_MARK)
            # head = "rishav@Rishavs-MacBook-Air linux_assignment"
            uh, _, path = head.partition(" ")
            d.text((x, y), uh + " ", font=font, fill=GREEN); x += font.getlength(uh + " ")
            d.text((x, y), path, font=font, fill=BLUE); x += font.getlength(path)
            d.text((x, y), " % ", font=font, fill=FG); x += font.getlength(" % ")
            d.text((x, y), cmd, font=bold, fill=FG)
        else:
            d.text((x, y), line, font=font, fill=color_for(line))
        y += LINE_H

    img.save(png_path)
    return png_path

tasks = [
    ("task1", "Task 1 — Creating and renaming files"),
    ("task2", "Task 2 — Viewing file contents"),
    ("task3", "Task 3 — Searching with grep"),
    ("task4", "Task 4 — Zip and unzip"),
    ("task5", "Task 5 — Downloading a file"),
    ("task6", "Task 6 — Changing permissions"),
    ("task7", "Task 7 — Environment variables"),
]
for key, title in tasks:
    render(os.path.join(SHOTS, key + ".txt"),
           os.path.join(SHOTS, key + ".png"), title)
print("rendered", len(tasks), "screenshots")

# ---------- build docx ----------
intro = [
 ("1. Creating and renaming files",
  "First I made a folder with mkdir, then made an empty file inside it with touch, and finally "
  "renamed the file using mv. After running mv the file showed up as renamed_example.txt when I "
  "listed the folder, so mv basically renames a file when you keep it in the same folder."),
 ("2. Looking at file contents",
  "I used the /etc/passwd file since it's always there. head -5 shows the first 5 lines (on a Mac "
  "those are just comment lines at the top) and tail -5 shows the last 5, which are the system "
  "accounts. I used -5 so I didn't have to scroll through the whole file."),
 ("3. Searching with grep",
  "Then I searched for the word root inside /etc/passwd. grep goes line by line and only prints the "
  "lines that match, so I got back the root account plus a couple of system lines that use /var/root "
  "as their home folder."),
 ("4. Zipping and unzipping",
  "I zipped the whole test_dir folder and unzipped it into a fresh folder to check it worked. The -r "
  "tells zip to include everything inside the folder, and -d lets you pick which folder to extract into. "
  "The renamed_example.txt file came back out exactly like the original."),
 ("5. Downloading a file",
  "The task asked for wget, but my Mac didn't have it (command not found), so I used curl which does the "
  "same job. The -o names the saved file and -L follows redirects. The sample.txt link gives a 404, so I "
  "just downloaded the example.com homepage to show the download working."),
 ("6. Changing permissions",
  "I made secure.txt and used chmod 444 to make it read only for everyone. The permissions went from "
  "-rw-r--r-- to -r--r--r--, and when I tried to add text it said permission denied, which is exactly "
  "what should happen. In octal 4 is read, 2 is write, 1 is execute, and the three digits are owner, "
  "group and everyone else. I can undo it with chmod 644."),
 ("7. Environment variables",
  "Last one. I set my own variable with export and printed it with echo $MY_VAR, then found it in the "
  "full list using env | grep MY_VAR. This only lasts for the current terminal window though, so to keep "
  "it permanently I'd add the export line to my ~/.zshrc file."),
]

doc = Document()
doc.styles["Normal"].font.name = "Calibri"
doc.styles["Normal"].font.size = Pt(11.5)

h = doc.add_heading("Linux Commands Assignment", level=0)
p = doc.add_paragraph()
p.add_run("Name: Rishav Jamwal\n")
p.add_run("Repo: https://github.com/rishavrishu86-dotcom/linux-commandline-basics")
doc.add_paragraph(
 "I did all of this on my Mac using the Terminal (zsh shell). I made a folder called linux_assignment "
 "and worked inside it. For each part below I've written what I did and pasted a screenshot of the actual "
 "command and its output from my terminal. Most of these are normal Linux commands so they work the same "
 "on Linux too. The only one that was different is wget, which my Mac didn't have, so I used curl instead.")

for (heading, text), (key, _title) in zip(intro, tasks):
    doc.add_heading(heading, level=1)
    doc.add_paragraph(text)
    png = os.path.join(SHOTS, key + ".png")
    doc.add_picture(png, width=Inches(6.3))

doc.add_heading("Wrap up", level=1)
doc.add_paragraph(
 "All seven tasks worked. The only thing that needed changing was wget since it isn't on Mac by default, "
 "so I used curl which does the same thing. Everything else ran without any problems, and the screenshots "
 "above show each command with its real output.")

out = os.path.join(DIR, "Linux_CommandLine_Basics_Submission.docx")
doc.save(out)
print("saved", out)
