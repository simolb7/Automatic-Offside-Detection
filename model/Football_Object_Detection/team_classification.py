import os
from ultralytics import YOLO
import cv2
import numpy as np
import math
from sklearn.cluster import KMeans




def predictTeamAttacking(players_classification, img):

    def getAreas(coordinates_team_1, coordinates_team_2):

        """
        Calcola l'area formata dai giocatori più esterni di tutte le due squadre
        
        Args:
            coordinate giocatori squadra 1, coordinate giocatori squadra 2
        
        Returns:
            area giocatori squadra 1, aerea giocatori squadra 2
        """
        height, width, channels = img.shape

        img_empty = np.zeros((height, width, channels), dtype=np.uint8)

        ## Disegno i punti in una immagine vuota
        for center in coordinates_team_1:
            cv2.circle(img_empty, center, 5, (0, 0, 255), -1)
        for center in coordinates_team_2:
            cv2.circle(img_empty, center, 5, (255, 0, 0), -1)
        for center in coordinates_goalkeeper:
            cv2.circle(img_empty, center, 5, (0,255,0), -1)


        
        ## calcolo il convex hull per i punti delle due squadre per trovare i giocatori più esterni
        hull_points_team_1 = cv2.convexHull(coordinates_team_1)
        hull_points_team_2 = cv2.convexHull(coordinates_team_2)

        # disegno le linee sull'immagine vuota per rappresentare l'area dei giocatori
        cv2.polylines(img_empty, [hull_points_team_1], isClosed=True, color=(0,0,255), thickness=1)
        cv2.polylines(img_empty, [hull_points_team_2], isClosed=True, color=(255,0,0), thickness=1)

        def calculate_area(points):
            """
            Calculate the area of a polygon given its vertices using the Shoelace formula.
            
            Args:
                points (np.ndarray): An array of shape (N, 2) representing the vertices of the polygon.
            
            Returns:
                float: The area of the polygon.
            """
            n = len(points)
            area = 0.0
            for i in range(n):
                j = (i + 1) % n
                area += points[i][0] * points[j][1]
                area -= points[j][0] * points[i][1]
            area = abs(area) / 2.0
            return area

   

        area_points_team_1 = calculate_area(hull_points_team_1.squeeze())
        area_points_team_2 = calculate_area(hull_points_team_2.squeeze())
        return area_points_team_1, area_points_team_2
    
    def getPlayerCloserToGoalkeeper(coordinates_team_1, coordinates_team_2, coordinates_goalkeeper):
        """
        Calcola il numero dei giocatori per ogni squadra che sono più vicini al portiere ( se il portiere esiste)

        Args:
            Coordinate dei giocatori delle due squadre, coordinate del portiere sempre come tuple (x1, y1)

        Returns:
            numero di giocatori vicini al portiere della squadra 1, numero di giocatori vicini al portiere della squadra 2
            se il portiere esiste altrimenti 0
            numero di giocatori totali preso per il calcolo
        """
        counter_team_1 = 0
        counter_team_2 = 0
        max_players_near_goalkeeper = 0
        if existGoalkeeper:
            distances = []

            for coordinate_1 in coordinates_team_1:
                distance_1 = cv2.norm(coordinate_1, coordinates_goalkeeper[0])
                distances.append((distance_1, 'team1'))
            for coordinate_2 in coordinates_team_2:
                distance_2 = cv2.norm(coordinate_2, coordinates_goalkeeper[0])
                distances.append((distance_2, 'team2'))

            distances_sorted = sorted(distances, key=lambda x: (x[0]))
            max_players_near_goalkeeper = len(distances) // 2 # max num giocatori presi in considerazione per il calcolo ( metà lista )
            for i in range(max_players_near_goalkeeper):
                if distances_sorted[i][1] == 'team1':
                    counter_team_1 += 1
                else:
                    counter_team_2 += 1

        return counter_team_1, counter_team_2, max_players_near_goalkeeper
    
    def getTeamCloserToBall(coordinates_team_1, coordinates_team_2, coordinates_ball):
        """
        Calcola la squadra che è più vicina alla palla

        Args:
            Coordinate dei giocatori e coordinate della palla

        Returns:
            'team1' se il team 1 è la squadra più vicina alla palla, 'team2' se è il team 2
            se la palla non esiste ritorna una stringa vuota
        """
        team_closer_to_ball = ""
        if existBall:
            distances_ball = []
            for coordinate_1 in coordinates_team_1:
                distance_1 = cv2.norm(coordinate_1, coordinates_ball[0])
                distances_ball.append((distance_1, 'team1'))
            for coordinate_2 in coordinates_team_2:
                distance_2 = cv2.norm(coordinate_2, coordinates_ball[0])
                distances_ball.append((distance_2, 'team2'))
            
            team_closer_to_ball = sorted(distances_ball, key=lambda x: (x[0]))[0][1]
        return team_closer_to_ball  
    
    def getPercentages(area_points_team_1, area_points_team_2, n_players_team_1, n_players_team_2, max_players_near_goalkeeper, counter_team_1, counter_team_2, team_closer_to_ball):
        """
        Calcola la probabilità che le due squadre stiano attaccando
        Args:
            Area giocatori delle due squadre, numero giocatori delle due squadre, il max numero di giocatori presi tra quelli più vicini al portiere,
            il numero di giocatori di ogni squadra più vicini al portiere, squadra più vicina alla palla
        
        Returns:
            percentuali di attacco delle due squadre
        """
        
        max_area = max(area_points_team_1, area_points_team_2) # area più grande tra le due squadre
        max_n_players = max(n_players_team_1, n_players_team_2) # maggior numero di giocatori
        norm_area_team_1 = area_points_team_1 / max_area # normalizzazione area team 1
        norm_area_team_2 = area_points_team_2 / max_area # normalizzazione area team 2
        norm_n_players_team_1 = 1- (n_players_team_1 / max_n_players ) # normalizzaziome numero giocatori team 1
        norm_n_players_team_2 = 1 - (n_players_team_2 / max_n_players ) # normalizzazione numero giocatori team 2
        w_ball = 0
        w_distance = 0
        w_area = 0
        w_n_players = 0
        _case = ""

        if max_players_near_goalkeeper > 0 and team_closer_to_ball != "": # se ci sono portiere e palla
            _case = "gb" #goalkeeper & ball
            w_ball = 0.4
            w_distance = 0.3
            w_area = 0.2
            w_n_players = 0.1
        elif max_players_near_goalkeeper == 0 and team_closer_to_ball != "": # se non c'è il portiere e c'è la palla
            _case = "b" # ball
            w_ball = 0.45
            w_area = 0.35
            w_n_players = 0.2
        elif max_players_near_goalkeeper > 0 and team_closer_to_ball == "": # se c'è il portiere ma non la palla
            _case = "g" # goalkeeper
            w_distance = 0.4
            w_area = 0.4
            w_n_players = 0.2
        else:
            _case = "None" # !goalkeeper & !ball
            w_area = 0.7
            w_n_players = 0.3

        match _case:
            case "gb":
                # normalizzazione distanza portiere giocatori delle due squadre
                norm_distance_team_1 = 1 - (counter_team_1 / max_players_near_goalkeeper)
                norm_distance_team_2 = 1 - (counter_team_2 / max_players_near_goalkeeper)
                # normalizzazione squadra più vicina alla palla
                # max giocatori vicini alla palla = 1
                players_closer_to_ball_team1 = 0
                players_closer_to_ball_team2 = 0
                if (team_closer_to_ball == 'team1'):
                    players_closer_to_ball_team1 = 1
                else:
                    players_closer_to_ball_team2 = 1
                norm_ball_team1 = players_closer_to_ball_team1 / 1 
                norm_ball_team2 = players_closer_to_ball_team2 / 1
                score_team_1 = (w_ball * norm_ball_team1) + (w_area * norm_area_team_1) + (w_distance * norm_distance_team_1) + (w_n_players * norm_n_players_team_1)
                score_team_2 = (w_ball * norm_ball_team2) + (w_area * norm_area_team_2) + (w_distance * norm_distance_team_2) + (w_n_players * norm_n_players_team_2)
                total_score = score_team_1 + score_team_2
                percent_1 = (score_team_1/total_score) * 100
                percent_2 = (score_team_2/total_score) * 100
            case "b":
                players_closer_to_ball_team1 = 0
                players_closer_to_ball_team2 = 0
                if (team_closer_to_ball == 'team1'):
                    players_closer_to_ball_team1 = 1
                else:
                    players_closer_to_ball_team2 = 1
                norm_ball_team1 = players_closer_to_ball_team1 / 1 
                norm_ball_team2 = players_closer_to_ball_team2 / 1
                score_team_1 = (w_ball * norm_ball_team1) + (w_area * norm_area_team_1)  + (w_n_players * norm_n_players_team_1)
                score_team_2 = (w_ball * norm_ball_team2) + (w_area * norm_area_team_2)  + (w_n_players * norm_n_players_team_2)
                total_score = score_team_1 + score_team_2
                percent_1 = (score_team_1/total_score) * 100
                percent_2 = (score_team_2/total_score) * 100
            case "g":
                # normalizzazione distanza portiere giocatori delle due squadre
                norm_distance_team_1 = 1 - (counter_team_1 / max_players_near_goalkeeper)
                norm_distance_team_2 = 1 - (counter_team_2 / max_players_near_goalkeeper)
                score_team_1 = (w_area * norm_area_team_1) + (w_distance * norm_distance_team_1) + (w_n_players * norm_n_players_team_1)
                score_team_2 = (w_area * norm_area_team_2) + (w_distance * norm_distance_team_2) + (w_n_players * norm_n_players_team_2)
                total_score = score_team_1 + score_team_2
                percent_1 = (score_team_1/total_score) * 100
                percent_2 = (score_team_2/total_score) * 100
            case "None":
                score_team_1 = (w_area * norm_area_team_1) + (w_n_players * norm_n_players_team_1)
                score_team_2 = (w_area * norm_area_team_2) + (w_n_players * norm_n_players_team_2)
                total_score = score_team_1 + score_team_2
                percent_1 = (score_team_1/total_score) * 100
                percent_2 = (score_team_2/total_score) * 100
            
        return percent_1, percent_2   
    """
    Calcolo coordinate di tutti i giocatori, portiere e palla (se esistono)
    come tuple (x1,y1)
    """
    existGoalkeeper = False
    existBall = False
    coordinates_team_1 = []
    coordinates_team_2 = []
    coordinates_goalkeeper = []
    coordinates_ball = []
    for key,value in players_classification.items():
        for box in value:
            x1,y1,x2,y2 = box
            center = (int((x1+x2)//2), int((y1+y2)//2))
            if key == 0:
                coordinates_team_1.append(center)
            elif key == 1:
                coordinates_team_2.append(center)
            elif key == 2:
                existGoalkeeper = True
                coordinates_goalkeeper.append(center)
            elif key == 3:
                existBall = True
                coordinates_ball.append(center)


    """
    Converto tutto in np array
    """
    coordinates_team_1 = np.array(coordinates_team_1)
    coordinates_team_2 = np.array(coordinates_team_2)
    coordinates_goalkeeper = np.array(coordinates_goalkeeper)
    coordinates_ball = np.array(coordinates_ball)

    # ottiene aree giocatori delle due squadre
    area_points_team_1, area_points_team_2 = getAreas(coordinates_team_1, coordinates_team_2)

    #ottieni numero giocatori più vicini al portiere delle due squadre
    counter_team_1, counter_team_2, max_players_near_goalkeeper = getPlayerCloserToGoalkeeper(coordinates_team_1, coordinates_team_2, coordinates_goalkeeper)

    """
    Calcolo numero giocatori
    """
    n_players_team_1 = len(players_classification[0])
    n_players_team_2 = len(players_classification[1])
    
    # ottieni la squadra più vicina alla palla
    team_closer_to_ball = getTeamCloserToBall(coordinates_team_1, coordinates_team_2, coordinates_ball)


    #calcola le percentuali di attacco delle due squadre
    percent_team_1, percent_team_2 = getPercentages(area_points_team_1, area_points_team_2, n_players_team_1, n_players_team_2, max_players_near_goalkeeper, counter_team_1, counter_team_2, team_closer_to_ball)

    return percent_team_1, percent_team_2





def team_classification(path):

    model_players = YOLO("model/Football_Object_Detection/weights/best.pt")

    results = model_players(path)
    image = cv2.imread(path)

    boxes, classes = results[0].boxes.xyxy.tolist(), results[0].boxes.cls.tolist()


    def computeDistance(color1, color2):
        distance = math.sqrt((color2[0]-color1[0])**2 + (color2[1]-color1[1])**2 + (color2[2]-color1[2])**2)
        return distance

    def extract_mean_color(bounding_box_player):
        # mask green
        bounding_box_hsv = cv2.cvtColor(bounding_box_player, cv2.COLOR_BGR2HSV)
        mask_green = cv2.inRange(bounding_box_hsv, (36,25,25), (70,255,255))
        

        mask_green_inv = cv2.bitwise_not(mask_green)
        result = cv2.bitwise_and(bounding_box_player, bounding_box_player, mask=mask_green_inv)
        # extract mean color
        mean_color = np.array(cv2.mean(bounding_box_player, mask=mask_green_inv))
        return mean_color[:3]
        
    def get_dominant_colors(team_colors):
        colors_kmeans = KMeans(n_clusters=2)
        colors_kmeans.fit(team_colors)
        return colors_kmeans
        

    players_boxes = []
    goalkeeper_box = []
    team_colors = []
    ball_box = []
    for box, cls in zip(boxes, classes):
        if round(cls) == 0:
            x1,y1,x2,y2 = map(int, box)
            players_boxes.append([x1,y1,x2,y2])
            player = image[y1:y2, x1:x2]
            color = extract_mean_color(player)
            team_colors.append(color)
        if round(cls) == 1:
            x1,y1,x2,y2 = map(int, box)
            goalkeeper_box.append([x1,y1,x2,y2])
        if round(cls) == 2:
            x1,y1,x2,y2 = map(int, box)
            ball_box.append([x1,y1,x2,y2])

    
    kmeans_colors = get_dominant_colors(team_colors)
    dominant_colors = kmeans_colors.cluster_centers_.astype(int)
    colors_shirts = []
    team_classification = dict()
    team_1 = 0
    team_2 = 1
    goalkeeper = 2
    ball = 3
    for color in dominant_colors:
        colors_shirts.append(color)
        if team_1 in team_classification:
            team_classification[team_2] = color
        else:
            team_classification[team_1] = color

    players_classification = dict()
    players_classification[team_1] = []
    players_classification[team_2] = []
    if len(goalkeeper_box) > 0: players_classification[goalkeeper] = goalkeeper_box
    if len(ball_box) > 0: players_classification[ball] = ball_box
    for i, color in enumerate(team_colors):
        distance_team_1 = computeDistance(color, team_classification[team_1])
        distance_team_2 = computeDistance(color, team_classification[team_2])
        if distance_team_1 < distance_team_2:
            players_classification[team_1].append(players_boxes[i])
        else:
            players_classification[team_2].append(players_boxes[i])
    
    """
    Calcolo squadra che sta attaccando
    """

    percent_team_1, percent_team_2 = predictTeamAttacking(players_classification, image)



    def annotate_image(players_classification, percent_team_1, percent_team_2):

        players_team_A = players_classification[team_1] if percent_team_1> percent_team_2 else players_classification[team_2]
        for player in players_team_A:
            x1,y1,x2,y2 = player
            cv2.rectangle(image, (x1,y1), (x2,y2), color=(0,0,255), thickness=2)
            cv2.putText(image, "Team A", (x1-30, y1-10),cv2.FONT_HERSHEY_COMPLEX,1, (0,0,255),2)
        players_team_B = players_classification[team_2] if percent_team_2 < percent_team_1 else players_classification[team_1]
        for player in players_team_B:
            x1,y1,x2,y2 = player
            cv2.rectangle(image, (x1,y1), (x2,y2), color=(255,0,0), thickness=2)
            cv2.putText(image, "Team B", (x1-30, y1-10),cv2.FONT_HERSHEY_COMPLEX,1, (255,0,0),2)
        if len(goalkeeper_box) > 0:
            x1,y1,x2,y2 = players_classification[goalkeeper][0]
            cv2.rectangle(image, (x1,y1), (x2,y2), color=(0,0,0), thickness=2) 
            cv2.putText(image, "GK", (x1-30, y1-10),cv2.FONT_HERSHEY_COMPLEX,1, (0,0,0),2)
        if len(ball_box) > 0:
            x1,y1,x2,y2 = players_classification[ball][0]
            cv2.rectangle(image, (x1,y1), (x2,y2), color=(0,0,0), thickness=2) 
            cv2.putText(image, "Ball", (x1-30, y1-10),cv2.FONT_HERSHEY_COMPLEX,1, (0,0,0),2)
        os.chdir("result")
        cv2.imwrite("teamClassification.png", image)
        os.chdir("..")

    annotate_image(players_classification, percent_team_1, percent_team_2)


    return players_classification, colors_shirts, image

