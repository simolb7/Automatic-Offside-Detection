import cv2
import torch
import numpy as np
import os
import model.sportsfield_release.utils.image_utils as utils
import model.sportsfield_release.utils.warp as warp


def convertPoint3Dto2D(homography: torch.Tensor, p: list[int], w: int, h: int) -> list[float]:
    '''Funzione che converte un punto sull'immagine 3D al punto sul campo 2D.
    La funzione prende in input:
    - Il tensore di omografia;
    - Il punto da convertire;
    - La larghezza dell'immagine del punto da convertire;
    - L'altezza dell'immagine del punto da convertire.\n
    La funzione ritorna in output la x e la y della posizione warpata.
    '''
    x = torch.tensor(p[0] / w - 0.5).float()
    y = torch.tensor(p[1] / h - 0.5).float()
    xy = torch.stack([x, y, torch.ones_like(x)])
    xy_warped = torch.matmul(homography.cpu(), xy)  # H.bmm(xy)
    xy_warped, z_warped = xy_warped.split(2, dim=1)

    # we multiply by 2, since our homographies map to
    # coordinates in the range [-0.5, 0.5] (the ones in our GT datasets)
    xy_warped = 2.0 * xy_warped / (z_warped + 1e-8)
    x_warped, y_warped = torch.unbind(xy_warped, dim=1)
    # [-1, 1] -> [0, 1]
    x_warped = (x_warped.item() * 0.5 + 0.5) * 1050
    y_warped = (y_warped.item() * 0.5 + 0.5) * 680

    return [x_warped, y_warped]



def convertPoint2Dto3D(homography: torch.Tensor, p: list[int], w: int, h: int) -> list[float]:
    '''Funzione che converte un punto sul campo 2D ad un punto sull'immagine 3D.
    La funzione prende in input:
    - Il tensore di omografia invertita;
    - Il punto da convertire;
    - La larghezza dell'immagine su cui convertire il punto;
    - L'altezza dell'immagine su cui convertire il punto.\n
    La funzione ritorna in output la x e la y della posizione warpata.
    '''
    x = torch.tensor(p[0] / 1050 - 0.5).float()
    y = torch.tensor(p[1] / 680 - 0.5).float()
    xy = torch.stack([x, y, torch.ones_like(x)])
    xy_warped = torch.matmul(homography.cpu(), xy)  # H.bmm(xy)
    xy_warped, z_warped = xy_warped.split(2, dim=1)

    # we multiply by 2, since our homographies map to
    # coordinates in the range [-0.5, 0.5] (the ones in our GT datasets)
    xy_warped = 2.0 * xy_warped / (z_warped + 1e-8)
    x_warped, y_warped = torch.unbind(xy_warped, dim=1)
    # [-1, 1] -> [0, 1]
    x_warped = (x_warped.item() * 0.5 + 0.5) * w
    y_warped = (y_warped.item() * 0.5 + 0.5) * h

    return [x_warped, y_warped]


def putPng(image, tag, position) -> None:
    if tag.shape[2] == 4:
    # Separa i canali RGBA
        b, g, r, a = cv2.split(tag)

        # Crea una maschera e la sua inversa utilizzando il canale alfa
        maschera = cv2.merge([a, a, a])
        maschera_inversa = cv2.bitwise_not(maschera)
        
        # Definisci le dimensioni dell'immagine da sovrapporre
        altezza_sovrapposta, larghezza_sovrapposta = tag.shape[:2]

        # Specifica la posizione (x, y) dove vuoi inserire l'immagine sovrapposta
        x,y = position[0], position[1]

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
    '''Funzione che calcola e disegna sull'immagine 2D e 3D il fuorigioco e le posizioni dei giocatori.
    La funzione prende in input:
    - Il path dell'immagine 3D;
    - Il tensore di omografia;;
    - La lista delle posizioni dei difensori nell'immagine 3D;
    - La lista delle posizioni degli attaccanti nell'immagine 3D;
    - La posizione del portiere nell'immagine 3D.\n
    La funzione ritorna in output il numero di attaccanti in fuorigioco e salva nella cartella result le immagini lavorate.'''
    image = cv2.imread(pathImage)
    pitch2D = cv2.imread("model/sportsfield_release/data/world_cup_template.png")

    offside_tag = cv2.imread('GUI/src/images/resizedTag.png',  cv2.IMREAD_UNCHANGED)

    '''Calcola altezza e larghezza della foto'''
    w = len(image[0])
    h = len(image)
    side = ''
    offside = []
    attacker2D = []
    defender2D = []

    if team == 'A':
        c_def = colors['Team B'].tolist()
        c_att = colors['Team A'].tolist()
    else:
        c_def = colors['Team A'].tolist()
        c_att = colors['Team B'].tolist()
 

    '''Calcola le posizioni dei giocatori in 2D'''
    for p in attacker:
        p_att = convertPoint3Dto2D(homography, [round((abs(p[0]+p[2])/2)), (p[3])], w, h)
        attacker2D.append(p_att)
        
    for p in defender:
        p_def = convertPoint3Dto2D(homography, [round((abs(p[0]+p[2])/2)), (p[3])], w, h)
        defender2D.append(p_def)
        
    if goalkeeper != 0:
        p_gk = convertPoint3Dto2D(homography, [round((abs(goalkeeper[0][2]+goalkeeper[0][0])/2)), (goalkeeper[0][3])], w, h)
        if p_gk[0] < 1050//2:
            side = 'left'
        else:
            side = 'right'
        if team == 'B':
            cv2.circle(pitch2D, (int(p_gk[0]), int(p_gk[1])), 10, c_def, -1)
        if team == 'A':
            cv2.circle(pitch2D, (int(p_gk[0]), int(p_gk[1])), 10, c_def, -1)
    else:
        c_left, c_right = 0,0
        for p in defender2D:
            if p[0] < 1050//2:
                c_left += 1
            else:
                c_right += 1
        for p in attacker2D:
            if p[0] < 1050//2:
                c_left += 1
            else:
                c_right += 1
        if c_left > c_right:
            side = 'left'
        else:   
            side = 'right'

    '''Disegna la linea del fuorigioco e calcola i giocatori in fuorigioco'''
    if side == 'left':
        last_def = min(defender2D, key=lambda x: x[0])
        cv2.line(pitch2D, (int(last_def[0]), 0), (int(last_def[0]), 680), (0,255,255), 2)
        invexHomo = torch.inverse(homography)
        p1 = convertPoint2Dto3D(invexHomo, [last_def[0], 0], w, h)
        p2 = convertPoint2Dto3D(invexHomo, [last_def[0], 680], w, h)
        cv2.line(image, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (0,255,255), 3)

        for i, p in enumerate(attacker2D):
            if p[0] < last_def[0]:
                offside.append(p)
                #CAMBIARE FONT
                mediax = round(((attacker[i][2]-attacker[i][0])/2)+attacker[i][0])

                putPng(image, offside_tag, [mediax-65,attacker[i][1]-30])


    if side == 'right':
        last_def = max(defender2D, key=lambda x: x[0])
        cv2.line(pitch2D, (int(last_def[0]), 0), (int(last_def[0]), 680), (0,255,255), 2)
        invexHomo = torch.inverse(homography)
        p1 = convertPoint2Dto3D(invexHomo, [last_def[0], 0], w, h)
        p2 = convertPoint2Dto3D(invexHomo, [last_def[0], 680], w, h)
        cv2.line(image, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), (0,255,255), 3)

        for i, p in enumerate(attacker2D):
            if p[0] > last_def[0]:
                offside.append(p)
                mediax = round(((attacker[i][2]-attacker[i][0])/2)+attacker[i][0])

                putPng(image, offside_tag, [mediax-65,attacker[i][1]-30])


    for p in attacker2D:
        if p in offside:
            cv2.circle(pitch2D, (int(p[0]), int(p[1])), 12, (0,255,255), -1)
        cv2.circle(pitch2D, (int(p[0]), int(p[1])), 10, c_att, -1)
    for p in defender2D:
        cv2.circle(pitch2D, (int(p[0]), int(p[1])), 10, c_def, -1)


  
    '''Viene calcolato il numero degli attaccanti in fuorigioco e salvate le immagini lavorate nella cartella result.'''

    playerOffside = len(offside)

    os.chdir('result')
    cv2.imwrite('result3D.jpg', image)
    cv2.imwrite('result2D.png', pitch2D)
    os.chdir('..')
    
    return playerOffside
