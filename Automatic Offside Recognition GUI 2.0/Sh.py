import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import Canvas, Label
import os
from PIL import Image, ImageTk, ImageEnhance

def reduce_brightness(image):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(0.7)

def seleziona_immagine():
    file_path = filedialog.askopenfilename()
    if file_path:
        impostazioni_preprocessamento(file_path)

def visualizza_immagine(file_path, team):
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
    
    img2 = Image.open("src/offside/pitch2D.png")
    img2 = img2.resize((512, 300))
    img2 = ImageTk.PhotoImage(img2)
    canvas.img2 = img2
    canvas.create_image(769, 159, anchor=tk.NW, image=img2)

    restart_button = Image.open("src/elements/restart_button.png")
    restart_button = restart_button.resize((200, 50))
    restart_button = ImageTk.PhotoImage(restart_button)
    canvas.restart_button = restart_button
    
    restart_button = canvas.create_image(150, 75, image=restart_button)

    team_label = Label(root, text=f"Team: {team}", font=('Helvetica', 12), bg='white')
    canvas.create_window(640, 50, window=team_label)    

    canvas.tag_bind(restart_button, '<Button-1>', lambda event: start_view())
    
    # Aggiunta della label per indicare il valore di team
    

def start_view():
    # Carica e ridimensiona l'immagine di sfondo
    background = Image.open("src/images/start.jpg")
    background = background.resize((1280, 720))
    background = ImageTk.PhotoImage(background)
    canvas.background = background
    canvas.create_image(0, 0, anchor=tk.NW, image=background)

    # Carica e ridimensiona l'immagine del pulsante start
    start_button_image = Image.open("src/elements/start_button.png")
    start_button_image = start_button_image.resize((200, 50))
    start_button_photo = ImageTk.PhotoImage(start_button_image)
    canvas.start_button = start_button_photo

    # Crea e posiziona 
    start_button = canvas.create_image(640, 360, image=start_button_photo)

    def on_enter(event):
        brightened_image = reduce_brightness(start_button_image)
        brightened_photo = ImageTk.PhotoImage(brightened_image)
        canvas.itemconfig(start_button, image=brightened_photo)
        canvas.current_button_image = brightened_photo

    # Funzione per gestire l'uscita del mouse
    def on_leave(event):
        canvas.itemconfig(start_button, image=canvas.start_button)

    # Associa gli eventi al pulsante start
    canvas.tag_bind(start_button, '<Button-1>', lambda event: avvia_processo())
    canvas.tag_bind(start_button, '<Enter>', on_enter)
    canvas.tag_bind(start_button, '<Leave>', on_leave)

def impostazioni_preprocessamento(file_path):
    global team
    team = "scroto"  # Valore iniziale del team

    background = Image.open("src/images/preprocess.jpg")
    background = background.resize((1280, 720))
    background = ImageTk.PhotoImage(background)
    canvas.background = background
    canvas.create_image(0, 0, anchor=tk.NW, image=background)  

    imgX = 578
    img = Image.open(file_path)
    img = img.resize((imgX, 350))
    img = ImageTk.PhotoImage(img)
    canvas.img = img
    canvas.create_image(640-(imgX//2), 35, anchor=tk.NW, image=img)
    
    teamA_button_img = Image.open("src/elements/teamA_button.png")
    teamA_button_img = teamA_button_img.resize((160, 40))
    teamA_button_img = ImageTk.PhotoImage(teamA_button_img)
    canvas.teamA_button_img = teamA_button_img
    
    teamB_button_img = Image.open("src/elements/teamB_button.png")
    teamB_button_img = teamB_button_img.resize((160, 40))
    teamB_button_img = ImageTk.PhotoImage(teamB_button_img)
    canvas.teamB_button_img = teamB_button_img
    
    process_button_img = Image.open("src/elements/process_button.png")
    process_button_img = process_button_img.resize((200, 50))
    process_button_img = ImageTk.PhotoImage(process_button_img)
    canvas.process_button_img = process_button_img
    
    button_space = 90
    button_height = 500
    
    teamA_button = canvas.create_image(640-button_space, button_height, image=teamA_button_img)
    teamB_button = canvas.create_image(640+button_space, button_height, image=teamB_button_img)
    process_button = canvas.create_image(640, 570, image=process_button_img)

    def scegli_team(this_team):
        global team
        team = this_team

    canvas.tag_bind(teamA_button, '<Button-1>', lambda event: scegli_team("A"))
    canvas.tag_bind(teamB_button, '<Button-1>', lambda event: scegli_team("B"))
    canvas.tag_bind(process_button, '<Button-1>', lambda event: visualizza_immagine(file_path, team))




def avvia_processo():
    seleziona_immagine()

root = tk.Tk()
root.title("Automatic Offside Recognition")
root.geometry("1280x720")

icon_path = os.path.join("src", "icons", "logo.ico")

root.iconbitmap(icon_path)

canvas = tk.Canvas(root, width=1280, height=720, highlightthickness=0)
canvas.pack()
start_view()

root.mainloop() 