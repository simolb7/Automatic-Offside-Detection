import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import os

testo = "Scegli il team"

def seleziona_immagine():
    file_path = filedialog.askopenfilename()
    if file_path:
        impostazioni_preprocessamento(file_path)

def visualizza_immagine(file_path):
    background = Image.open("src/images/result.jpg")
    background = background.resize((1280, 720))
    background = ImageTk.PhotoImage(background)
    canvas.background = background
    canvas.create_image(0, 0, anchor=tk.NW, image=background)  

    img = Image.open(file_path)
    img = img.resize((753, 424))
    img = ImageTk.PhotoImage(img)
    canvas.img = img
    canvas.create_image(0, 159, anchor=tk.NW, image=img)
    
    img2 = Image.open("src/offside/field.png")
    img2 = img2.resize((512, 356))
    img2 = ImageTk.PhotoImage(img2)
    canvas.img2 = img2
    canvas.create_image(769, 159, anchor=tk.NW, image=img2)

    font_path = "src/fonts/Sequel100Black-85.ttf"
    custom_font = ("SequelBlack", 18, "bold")  
    canvas.create_text(1025, 540, text="Offside Players 2", fill="white", font=custom_font)

def impostazioni_preprocessamento(file_path):
    background = Image.open("src/images/result.jpg")
    background = background.resize((1280, 720))
    background = ImageTk.PhotoImage(background)
    canvas.background = background
    canvas.create_image(0, 0, anchor=tk.NW, image=background)  

    img = Image.open(file_path)
    img = img.resize((400, 250))
    img = ImageTk.PhotoImage(img)
    canvas.img = img
    canvas.create_image(450, 0, anchor=tk.NW, image=img)
    
    teamA_button = Image.open("src/elements/start_button.png")
    teamA_button = teamA_button.resize((200, 50))
    teamA_button = ImageTk.PhotoImage(teamA_button)
    canvas.teamA_button = teamA_button
    
    teamB_button = Image.open("src/elements/start_button.png")
    teamB_button = teamB_button.resize((200, 50))
    teamB_button = ImageTk.PhotoImage(teamB_button)
    canvas.teamB_button = teamB_button
    
    process_button = Image.open("src/elements/start_button.png")
    process_button = process_button.resize((200, 50))
    process_button = ImageTk.PhotoImage(process_button)
    canvas.process_button = process_button
    
    teamA_button = canvas.create_image(500, 500, image=teamA_button)
    teamB_button = canvas.create_image(600, 500, image=teamB_button)
    start_button = canvas.create_image(550, 600, image=process_button)

    canvas.tag_bind(teamA_button, '<Button-1>', lambda event: scegli_team(0))
    canvas.tag_bind(teamB_button, '<Button-1>', lambda event: scegli_team(1))
    canvas.tag_bind(start_button, '<Button-1>', lambda event: visualizza_immagine(file_path))

    canvas.create_text(500, 340, text=testo, fill="white", font="Arial")

    # Aggiungi un frame per contenere i pulsanti

def scegli_team(team):
    if team==0:
        testo = "Team A"
    else:
        testo = "Team B"

def luminosita_diminuita(event):
    canvas.itemconfig(start_button, image=button_img_hover)

def luminosita_normale(event):
    canvas.itemconfig(start_button, image=button_img)

def avvia_processo():
    seleziona_immagine()

root = tk.Tk()
root.title("Automatic Offside Recognition")
root.geometry("1280x720")

icon_path = os.path.join("src", "icons", "logo.ico")
root.iconbitmap(icon_path)

canvas = tk.Canvas(root, width=1280, height=720, highlightthickness=0)
canvas.pack()

sfondo_img = Image.open(os.path.join("src", "images", "start.jpg"))
sfondo_img = sfondo_img.resize((1280, 720))
sfondo_img = ImageTk.PhotoImage(sfondo_img)
canvas.create_image(0, 0, anchor=tk.NW, image=sfondo_img)

button_img = Image.open("src/elements/start_button.png")
button_img = button_img.resize((200, 50))
button_img = ImageTk.PhotoImage(button_img)

button_img_hover = Image.open("src/elements/start_button_hover.png")
button_img_hover = button_img_hover.resize((200, 50))
button_img_hover = ImageTk.PhotoImage(button_img_hover)

start_button = canvas.create_image(640, 360, image=button_img)

canvas.tag_bind(start_button, '<Enter>', luminosita_diminuita)
canvas.tag_bind(start_button, '<Leave>', luminosita_normale)

canvas.tag_bind(start_button, '<Button-1>', lambda event: avvia_processo())

root.mainloop()
