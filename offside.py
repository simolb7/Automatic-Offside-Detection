import cv2
import torch
import numpy as np
import os



def convertPoint3Dto2D(homography: torch.Tensor, p: list, w: int, h: int) -> list[float]:
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



def convertPoint2Dto3D(homography: torch.Tensor, p: list, w: int, h: int) -> list[float]:
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


def drawOffside(pathImage: str, homography:torch.Tensor, defender:list[list[int]] = 0, attacker: list[list[int]]=0, goalkeeper: list[int]=0 ) -> int:
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
    goalkeeper = [741, 549]
    ''''
    homography = torch.tensor([[[ 0.2940,  0.0238, -0.3597],
            [-0.2042,  1.1472,  0.1179],
            [ 0.0560,  0.9439,  1.0000]]])
    '''
    defender = [[1089, 745], [1195, 704], [1496, 579], [892, 881]]
    attacker = [[833, 785], [1216, 719]]

    '''Calcola altezza e larghezza della foto'''
    w = len(image[0])
    h = len(image)

    '''Calcola la posizione del portiere e da questa deriviamo il lato dell'attacco (Nelle immagini delle azioni è presente sempre un solo portiere)'''
    p_goalkeeper = convertPoint3Dto2D(homography, goalkeeper, w, h)
    if p_goalkeeper[0] > 1050/2:
        side = 'right'
    else:
        side = 'left'
  
    if side == 'right':
        d = []
        a = []
        offside = []
        inside = []
        '''Conversione dei punti dei difensori sull'immagine 2D per agevolare la ricerca dell'ultimo difensore, che viene fatta attraverso max()
        nel caso in cui si attacchi a destra.
        Una volta trovato viene usata la cordinata x della sua posizione per tracciare la linea sull'immagine 2D e usando la matrice di omografia inversa
        vengono trovati i corrispettivi punti sull'immagine 3D e disegnata la linea.'''
        for p in defender:
            d_converted = convertPoint3Dto2D(homography, p, w, h)
            d.append(d_converted)
            image = cv2.circle(image, p, 0, (0, 0, 255), 10)
            pitch2D = cv2.circle(pitch2D, (int(d_converted[0]), int(d_converted[1])), 0, (0, 0, 255), 10)
        offside2D = max(d)
        p1_2D = [offside2D[0], 0]
        p2_2D = [offside2D[0], 680]
        pitch2D = cv2.line(pitch2D, (int(p1_2D[0]), int(p1_2D[1])), (int(p2_2D[0]), int(p2_2D[1])), (0, 255, 255), 1)
        inver_homography = torch.inverse(homography)
        p1_3D = convertPoint2Dto3D(inver_homography, p1_2D, w, h)
        p2_3D = convertPoint2Dto3D(inver_homography, p2_2D, w, h)
        image = cv2.line(image, (int(p1_3D[0]), int(p1_3D[1])), (int(p2_3D[0]), int(p2_3D[1])), (0, 255, 255), 3)
        '''Conversione dei punti dei difensori sull'immagine 2D per agevolare la ricerca degli attaccanti in fuorigioco. Per l'attacco a destra sono tutti
        quelli la cui coordinata x è maggiore della coordinata x dell'ultimo difensore. Vengono quindi disegnati sull'immagine 2D gli attaccanti.'''
        for p in attacker:
            a_converted = convertPoint3Dto2D(homography, p, w, h)
            a.append(a_converted)
            image = cv2.circle(image, p, 0, (255, 0, 0), 10)
            pitch2D = cv2.circle(pitch2D, (int(a_converted[0]), int(a_converted[1])), 0, (255, 0, 0), 10)
        for p in a:
            if p[0] > offside2D[0]:
                offside.append(p)
                pitch2D = cv2.circle(pitch2D, (int(p[0]), int(p[1])), 0, (0,0,0), 5)
            else:
                inside.append(p)

    elif side == 'left':
        d = []
        a = []
        offside = []
        inside = []
        '''Conversione dei punti dei difensori sull 'immagine 2D per agevolare la ricerca dell'ultimo difensore, che viene fatta attraverso min()
        nel caso in cui si attacchi a sinistra.
        Una volta trovato viene usata la cordinata x della sua posizione per tracciare la linea sull'immagine 2D e usando la matrice di omografia inversa
        vengono trovati i corrispettivi punti sull'immagine 3D e disegnata la linea.'''
        for p in defender:
            d_converted = convertPoint3Dto2D(homography, p, w, h)
            d.append(d_converted)
            image = cv2.circle(image, p, 0, (0, 0, 255), 10)
            pitch2D = cv2.circle(pitch2D, (int(d_converted[0]), int(d_converted[1])), 0, (0, 0, 255), 10)
        offside2D = min(d)
        p1_2D = [offside2D[0], 0]
        p2_2D = [offside2D[0], 680]
        pitch2D = cv2.line(pitch2D, (int(p1_2D[0]), int(p1_2D[1])), (int(p2_2D[0]), int(p2_2D[1])), (0, 255, 255), 1)
        inver_homography = torch.inverse(homography)
        p1_3D = convertPoint2Dto3D(inver_homography, p1_2D, w, h)
        p2_3D = convertPoint2Dto3D(inver_homography, p2_2D, w, h)
        image = cv2.line(image, (int(p1_3D[0]), int(p1_3D[1])), (int(p2_3D[0]), int(p2_3D[1])), (0, 255, 255), 3)
        '''Conversione dei punti dei difensori sull'immagine 2D per agevolare la ricerca degli attaccanti in fuorigioco. Per l'attacco a sinistra sono tutti
        quelli la cui coordinata x è minore della coordinata x dell'ultimo difensore. Vengono quindi disegnati sull'immagine 2D gli attaccanti.'''
        for p in attacker:
            a_converted = convertPoint3Dto2D(homography, p, w, h)
            a.append(a_converted)
            image = cv2.circle(image, p, 0, (255, 0, 0), 10)
            pitch2D = cv2.circle(pitch2D, (int(a_converted[0]), int(a_converted[1])), 0, (255, 0, 0), 10)
        for p in a:
            if p[0] < offside2D[0]:
                offside.append(p)
                pitch2D = cv2.circle(pitch2D, (int(p[0]), int(p[1])), 0, (0,0,0), 5)
            else:
                inside.append(p)

    '''Viene calcolato il numero degli attaccanti in fuorigioco e salvate le immagini lavorate nella cartella result.'''
    playerOffside = len(offside)

    os.chdir('result')
    cv2.imwrite('result3D.jpg', image)
    cv2.imwrite('result2D.png', pitch2D)
    os.chdir('..')
    
    return playerOffside