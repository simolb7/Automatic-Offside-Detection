import cv2
import torch
import numpy as np
import os
import model.sportsfield_release.utils.image_utils as utils
import model.sportsfield_release.utils.warp as warp


def putPng(image, tag, position) -> None:
    if tag.shape[2] == 4:
    # Separa i canali RGBA
        b, g, r, a = cv2.split(tag)

        print('position', position)
        
        # Crea una maschera e la sua inversa utilizzando il canale alfa
        maschera = cv2.merge([a, a, a])
        maschera_inversa = cv2.bitwise_not(maschera)
        
        # Definisci le dimensioni dell'immagine da sovrapporre
        altezza_sovrapposta, larghezza_sovrapposta = tag.shape[:2]
        print('h e 2: ',altezza_sovrapposta, larghezza_sovrapposta)
        
        # Specifica la posizione (x, y) dove vuoi inserire l'immagine sovrapposta
        x,y = position[0], position[1]
        print('valori: ', x,y)
   
        # Crea la ROI sull'immagine di sfondo
        roi = image[y:y+altezza_sovrapposta, x:x+larghezza_sovrapposta]
        
        # Usa la maschera inversa per oscurare l'area della ROI nel sfondo
        sfondo_bg = cv2.bitwise_and(roi, roi, mask=maschera_inversa[:, :, 0])
        
        # Usa la maschera per estrarre la parte dell'immagine sovrapposta
        sovrapposta_fg = cv2.bitwise_and(tag[:, :, :3], tag[:, :, :3], mask=maschera[:, :, 0])
        
        # Combina lo sfondo e l'immagine sovrapposta
        combinata = cv2.add(sfondo_bg, sovrapposta_fg)
        
        # Inserisci la combinazione nella ROI del sfondo
        image[y:y+altezza_sovrapposta, x:x+larghezza_sovrapposta] = combinata


def drawOffside(pathImage: str, team: str, colors: dict[str, np.ndarray], homography:torch.Tensor, defender:list[list[int]], attacker: list[list[int]], goalkeeper: list[list[int]]=0) -> int:

    image = cv2.imread(pathImage)
    pitch2D = cv2.imread("model/sportsfield_release/data/world_cup_template.png")

    offside_tag = cv2.imread('GUI/src/images/resizedTag.png',  cv2.IMREAD_UNCHANGED)


    #provax, provay = round(attacker[i][0]+attacker[i][2]/2),  round(attacker[i][1]+attacker[i][3]/2)
    print(round(((1207-1159)/2)+1159))
    mediax = round(((1249-1170)/2)+1170)
    putPng(image, offside_tag, [mediax-65,445-30])
    mediax = round(((1086-1036)/2)+1036)
    putPng(image, offside_tag, [mediax-65,399-30])


    cv2.imshow('image', image)
    cv2.waitKey(0)

posizione1 = [1170, 444, 1207, 557]
posizione2 = [1036, 398, 980, 484]
drawOffside('samples/281.jpg', None, None, None, None, None, None)