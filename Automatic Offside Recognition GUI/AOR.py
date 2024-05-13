import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import os

def seleziona_immagine():
    file_path = filedialog.askopenfilename()
    if file_path:
        visualizza_immagine(file_path)

def visualizza_immagine(file_path):
    background = Image.open("src/images/result.jpg")
    background = background.resize((1280, 720), Image.ANTIALIAS)
    background = ImageTk.PhotoImage(background)
    canvas.background = background
    canvas.create_image(0, 0, anchor=tk.NW, image=background)  

    img = Image.open(file_path)
    img = img.resize((753, 424), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    canvas.img = img
    canvas.create_image(0, 159, anchor=tk.NW, image=img)
    
    img2 = Image.open("src/offside/field.png")
    img2 = img2.resize((512, 356), Image.ANTIALIAS)
    img2 = ImageTk.PhotoImage(img2)
    canvas.img2 = img2
    canvas.create_image(769, 159, anchor=tk.NW, image=img2)

    font_path = "src/fonts/Sequel100Black-85.ttf"
    custom_font = ("SequelBlack", 18, "bold")  
    canvas.create_text(1025, 540, text="Offside Players 2", fill="white", font=custom_font)

def luminosita_diminuita(event):
    canvas.itemconfig(start_button, image=button_img_hover)

def luminosita_normale(event):
    canvas.itemconfig(start_button, image=button_img)

def avvia_processo():
    seleziona_immagine()

root = tk.Tk()
root.title("Automatic Offside Recognition")
root.geometry("1280x720")

#icon_path = os.path.join("src", "icons", "logo.ico")

#root.iconbitmap(icon_path)

canvas = tk.Canvas(root, width=1280, height=720, highlightthickness=0)
canvas.pack()

sfondo_img = Image.open(os.path.join("src", "images", "start.jpg"))
sfondo_img = sfondo_img.resize((1280, 720), Image.ANTIALIAS)
sfondo_img = ImageTk.PhotoImage(sfondo_img)
canvas.create_image(0, 0, anchor=tk.NW, image=sfondo_img)

button_img = Image.open("src/elements/start_button.png")
button_img = button_img.resize((200, 50), Image.ANTIALIAS)
button_img = ImageTk.PhotoImage(button_img)

button_img_hover = Image.open("src/elements/start_button_hover.png")
button_img_hover = button_img_hover.resize((200, 50), Image.ANTIALIAS)
button_img_hover = ImageTk.PhotoImage(button_img_hover)

start_button = canvas.create_image(640, 360, image=button_img)

canvas.tag_bind(start_button, '<Enter>', luminosita_diminuita)
canvas.tag_bind(start_button, '<Leave>', luminosita_normale)

canvas.tag_bind(start_button, '<Button-1>', lambda event: avvia_processo())

root.mainloop()
