import time
import tkinter as tk
from tkinter import PhotoImage, filedialog
from PIL import ImageTk, Image
from tkinter import Canvas, Label
import os
from PIL import Image, ImageTk, ImageEnhance
from tkinter import font
import tkinter as tk
import tkinter as tk
import _thread
import pyglet

class gifplay:

        def __init__(self,label,gif_file_path,delay):
            self.frame=[]
            i=0
            while 1:
                try:
                    image=PhotoImage(file = gif_file_path, format="gif -index "+str(i))
                    self.frame.append(image)
                    i=i+1
                except:
                    break
            print(i)
            self.totalFrames=i-1
            self.delay=delay
            self.labelspace=label
            self.labelspace.image=self.frame[0]

        def play(self):
            _thread.start_new_thread(self.infinite,())

        def infinite(self):
            i=0
            while 1:
                self.labelspace.configure(image=self.frame[i])
                i=(i+1)%self.totalFrames
                time.sleep(self.delay)

def reduce_brightness(image, factor=0.7):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def seleziona_immagine():
    file_path = filedialog.askopenfilename()
    if file_path:
        impostazioni_preprocessamento(file_path)

def visualizza_immagine(file_path, team, players):
    background = Image.open("Automatic Offside Recognition GUI/src/images/result.jpg")
    background = background.resize((1280, 720))
    background = ImageTk.PhotoImage(background)
    canvas.background = background
    canvas.create_image(0, 0, anchor=tk.NW, image=background)  

    img = Image.open(file_path)
    img = img.resize((753, 424))
    img = ImageTk.PhotoImage(img)
    canvas.img = img
    canvas.create_image(0, 159, anchor=tk.NW, image=img)
    
    img2 = Image.open("Automatic Offside Recognition GUI/src/offside/pitch2D.png")
    x = 1050
    y = 680
    res = 2.4
    img2 = img2.resize((int(x/res), int(y/res)))
    img2 = ImageTk.PhotoImage(img2)
    canvas.img2 = img2
    canvas.create_image(810, 168, anchor=tk.NW, image=img2)

    restart_button_img = Image.open("Automatic Offside Recognition GUI/src/elements/restart_button.png")
    restart_button_img_resized = restart_button_img.resize((200, 50))
    restart_button_photo = ImageTk.PhotoImage(restart_button_img_resized)
    canvas.restart_button = restart_button_photo
    canvas.restart_button_img = restart_button_img_resized
    
    restart_button = canvas.create_image(640, 650, image=restart_button_photo)

    canvas.tag_bind(restart_button, '<Button-1>', lambda event: start_view())
    
    def on_enter_restart(event):
        brightened_image = reduce_brightness(canvas.restart_button_img)
        brightened_photo = ImageTk.PhotoImage(brightened_image)
        canvas.itemconfig(restart_button, image=brightened_photo)
        canvas.current_button_image = brightened_photo

    def on_leave_restart(event):
        canvas.itemconfig(restart_button, image=canvas.restart_button)

    canvas.tag_bind(restart_button, '<Enter>', on_enter_restart)
    canvas.tag_bind(restart_button, '<Leave>', on_leave_restart)

    players_button_img = Image.open(f"Automatic Offside Recognition GUI/src/images/{players}.png")
    players_button_photo = ImageTk.PhotoImage(players_button_img)
    canvas.players_button = players_button_photo
    canvas.players_button_img = players_button_img
    
    canvas.create_image(1140, 530, image=players_button_photo)

    team_button_img = Image.open(f"Automatic Offside Recognition GUI/src/images/{team}.png")
    team_button_photo = ImageTk.PhotoImage(team_button_img)
    canvas.team_button = team_button_photo
    canvas.team_button_img = team_button_img
    
    canvas.create_image(900, 530, image=team_button_photo)

def schermata_di_caricamento(file_path, team):
    canvas.delete("all")
    background = Image.open('Automatic Offside Recognition GUI/src/images/waiting.jpg')
    background = background.resize((1280, 720))
    background = ImageTk.PhotoImage(background)
    canvas.background = background
    canvas.create_image(0, 0, anchor=tk.NW, image=background)

    def handle_keypress(event):
        global stop
        stop = True
        visualizza_immagine(file_path, team, 8)

    root.bind("<Key>", handle_keypress)



def schermata_di_caricamento_gif(file_path, team):

    gif_file_path = "Automatic Offside Recognition GUI\src\loading.gif"

    background_image = Image.open("Automatic Offside Recognition GUI\src\images\start.jpg")
    background_photo = ImageTk.PhotoImage(background_image)
    label = tk.Label(root, image=background_photo)
    label.pack()
    
    gif = gifplay(label, gif_file_path,0.1)
    gif.play()


def schermata_di_caricamento_loop(file_path, team):
    global stop
    stop = False

    images = [
        Image.open("Automatic Offside Recognition GUI\src\images\image1.jpg"),
        Image.open("Automatic Offside Recognition GUI\src\images\image2.jpg"),
        Image.open("Automatic Offside Recognition GUI\src\images\image3.jpg"),
        Image.open("Automatic Offside Recognition GUI\src\images\image4.jpg")
    ]
    
    # Funzione per mostrare le immagini a intervalli
    def show_image(idx=0):
        if not stop:  # Continua solo se lo stato di stop è False
            canvas.delete("all")
            image = images[idx].resize((1280, 720))
            background = ImageTk.PhotoImage(image)
            canvas.background = background
            canvas.create_image(0, 0, anchor=tk.NW, image=background) 

            idx = (idx + 1) % len(images)  # Passa all'immagine successiva
            root.after(250, show_image, idx)  # Mostra l'immagine successiva dopo un breve ritardo

    def handle_keypress(event):
        global stop
        stop = True
        visualizza_immagine(file_path, team)

    root.bind("<Key>", handle_keypress)
    
    show_image(0)

def start_view():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            if widget["text"].startswith("Team ") or widget["text"].startswith("Giocatori "):
                widget.destroy()


    background = Image.open('Automatic Offside Recognition GUI/src/images/start.jpg')
    background = background.resize((1280, 720))
    background = ImageTk.PhotoImage(background)
    canvas.background = background
    canvas.create_image(0, 0, anchor=tk.NW, image=background)

    start_button_image = Image.open('Automatic Offside Recognition GUI/src/elements/start_button.png')
    start_button_image_resized = start_button_image.resize((200, 50))
    start_button_photo = ImageTk.PhotoImage(start_button_image_resized)
    canvas.start_button = start_button_photo
    canvas.start_button_image = start_button_image_resized
    
    start_button = canvas.create_image(640, 360, image=start_button_photo)

    def on_enter(event):
        brightened_image = reduce_brightness(canvas.start_button_image)
        brightened_photo = ImageTk.PhotoImage(brightened_image)
        canvas.itemconfig(start_button, image=brightened_photo)
        canvas.current_button_image = brightened_photo

    def on_leave(event):
        canvas.itemconfig(start_button, image=canvas.start_button)

    canvas.tag_bind(start_button, '<Button-1>', lambda event: avvia_processo())
    canvas.tag_bind(start_button, '<Enter>', on_enter)
    canvas.tag_bind(start_button, '<Leave>', on_leave)

def impostazioni_preprocessamento(file_path):
    global team
    team = "A"  # Valore iniziale del team

    background = Image.open("Automatic Offside Recognition GUI/src/images/preprocess.jpg")
    background = background.resize((1280, 720))
    background = ImageTk.PhotoImage(background)
    canvas.background = background
    canvas.create_image(0, 0, anchor=tk.NW, image=background)  

    imgX = 727
    img = Image.open(file_path)
    img = img.resize((imgX, int((imgX/16) * 9)))
    img = ImageTk.PhotoImage(img)
    canvas.img = img
    canvas.create_image(640-(imgX//2), 62, anchor=tk.NW, image=img)
    
    teamA_button_img = Image.open("Automatic Offside Recognition GUI/src/elements/teamA_button.png")
    teamA_button_img_resized = teamA_button_img.resize((160, 40))
    teamA_button_img_dark = reduce_brightness(teamA_button_img_resized, 0.5)
    teamA_button_photo = ImageTk.PhotoImage(teamA_button_img_dark)
    canvas.teamA_button_photo = teamA_button_photo
    canvas.teamA_button_img_resized = teamA_button_img_resized
    
    teamB_button_img = Image.open("Automatic Offside Recognition GUI/src/elements/teamB_button.png")
    teamB_button_img_resized = teamB_button_img.resize((160, 40))
    teamB_button_img_dark = reduce_brightness(teamB_button_img_resized, 0.5)
    teamB_button_photo = ImageTk.PhotoImage(teamB_button_img_dark)
    canvas.teamB_button_photo = teamB_button_photo
    canvas.teamB_button_img_resized = teamB_button_img_resized
    
    process_button_img = Image.open("Automatic Offside Recognition GUI/src/elements/process_button.png")
    process_button_img_resized = process_button_img.resize((200, 50))
    process_button_photo = ImageTk.PhotoImage(process_button_img_resized)
    canvas.process_button_photo = process_button_photo
    canvas.process_button_img = process_button_img_resized
    
    button_space = 90
    button_height = 560
    
    teamA_button = canvas.create_image(640-button_space, button_height, image=teamA_button_photo)
    teamB_button = canvas.create_image(640+button_space, button_height, image=teamB_button_photo)
    process_button = canvas.create_image(640, 630, image=process_button_photo)

    def scegli_team(this_team):
        global team
        team = this_team
        if team == "A":
            brightened_teamA = ImageTk.PhotoImage(canvas.teamA_button_img_resized)
            darkened_teamB = ImageTk.PhotoImage(reduce_brightness(canvas.teamB_button_img_resized, 0.5))
            canvas.itemconfig(teamA_button, image=brightened_teamA)
            canvas.itemconfig(teamB_button, image=darkened_teamB)
            canvas.teamA_button_photo = brightened_teamA
            canvas.teamB_button_photo = darkened_teamB
        elif team == "B":
            brightened_teamB = ImageTk.PhotoImage(canvas.teamB_button_img_resized)
            darkened_teamA = ImageTk.PhotoImage(reduce_brightness(canvas.teamA_button_img_resized, 0.5))
            canvas.itemconfig(teamB_button, image=brightened_teamB)
            canvas.itemconfig(teamA_button, image=darkened_teamA)
            canvas.teamB_button_photo = brightened_teamB
            canvas.teamA_button_photo = darkened_teamA

    def on_enter_process(event):
        brightened_image = reduce_brightness(canvas.process_button_img, 0.8)
        brightened_photo = ImageTk.PhotoImage(brightened_image)
        canvas.itemconfig(process_button, image=brightened_photo)
        canvas.current_button_image = brightened_photo

    def on_leave_process(event):
        canvas.itemconfig(process_button, image=canvas.process_button_photo)

    canvas.tag_bind(teamA_button, '<Button-1>', lambda event: scegli_team("A"))
    canvas.tag_bind(teamB_button, '<Button-1>', lambda event: scegli_team("B"))
    canvas.tag_bind(process_button, '<Button-1>', lambda event: schermata_di_caricamento(file_path, team))
    canvas.tag_bind(process_button, '<Enter>', on_enter_process)
    canvas.tag_bind(process_button, '<Leave>', on_leave_process)

def avvia_processo():
    seleziona_immagine()

root = tk.Tk()
root.title("Automatic Offside Recognition")
root.geometry("1280x720")
root.resizable(False, False)

icon_path = 'Automatic Offside Recognition GUI/src/icons/logo.ico'
im = Image.open(icon_path)
photo = ImageTk.PhotoImage(im)
root.wm_iconphoto(True, photo)

root.iconbitmap(icon_path)

canvas = tk.Canvas(root, width=1280, height=720, highlightthickness=0)
canvas.pack()
start_view()

root.mainloop()
