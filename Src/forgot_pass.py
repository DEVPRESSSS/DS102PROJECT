
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"\DS102PROJECT\Assets\assets1\frame0")

def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)





window = Tk()

window.geometry("688x375")
window.configure(bg = "#F4F5F6")
window.minsize(688,375)

canvas = Canvas(
    window,
    bg = "#F4F5F6",
    height = 375,
    width = 688,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))

image_1 = canvas.create_image(
    198.0,
    190.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    518.0,
    184.0,
    image=image_image_2
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    518.0,
    124.5,
    image=entry_image_1
)
entry_1 = Entry(
    canvas,
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=409.0,
    y=112.0,
    width=218.0,
    height=23.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))

entry_bg_2 = canvas.create_image(
    518.0,
    206.5,
    image=entry_image_2
)
entry_2 = Entry(
    canvas,
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=409.0,
    y=194.0,
    width=218.0,
    height=23.0
)

canvas.create_text(
    405.0,
    92.0,
    anchor="nw",
    text="Enter email:",
    fill="#0F0D74",
    font=("IstokWeb Bold", 11 * -1)
)

canvas.create_text(
    405.0,
    172.0,
    anchor="nw",
    text="Enter 6 digits code:",
    fill="#0F0D74",
    font=("IstokWeb Bold", 11 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    canvas,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=556.0,
    y=145.0,
    width=75.0,
    height=22.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    canvas,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=405.0,
    y=236.0,
    width=226.0,
    height=27.0
)
canvas.pack(expand=True)
window.resizable(True, True)
window.mainloop()
