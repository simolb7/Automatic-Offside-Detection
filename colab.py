import requests
from google.colab import drive

# Definisci l'URL del notebook su Google Colab
notebook_url = "https://colab.research.google.com/drive/16WLYpoVUB2z8qCLIFBNUKvzl6Ykv9EYc?usp=sharing"

# Carica l'immagine
files = {'file': open('82.jpg', 'rb')}

# Esegui il notebook su Google Colab
response = requests.post(notebook_url, files=files)

# Controlla se la richiesta è andata a buon fine
if response.status_code == 200:
    print("Il notebook è stato eseguito con successo su Google Colab.")
else:
    print("Si è verificato un errore durante l'esecuzione del notebook su Google Colab.")

drive.mount('/content/drive')

# Supponiamo che il tuo file si trovi in '/content/file_da_scaricare.txt'
# Puoi spostarlo su Google Drive con il seguente comando
!cp /content/file_da_scaricare.txt /content/drive/My\ Drive/