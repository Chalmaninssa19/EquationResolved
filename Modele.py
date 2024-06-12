import numpy as np
import pandas as pd
from joblib import load
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# Enlever les lignes blanches 
def dropRowsWhiteImage(image_array):
    # Efface ligne horizontal blanc
    sums = np.sum(image_array, axis=1) #Avoir la somme de chaque ligne du tableau
    indices = np.where(sums == 255 * image_array.shape[1]) #prendre les indices du tableau qui  verifie la condition
    image_array = np.delete(image_array, indices, axis=0)#effacer les lignes se trouvant a indices
    
    # Efface ligne vertical blanc
    sums = np.sum(image_array, axis=0)
    indices = np.where(sums == 255 * image_array.shape[0])
    image_array = np.delete(image_array, indices, axis=1)
    
    result_image = (Image.fromarray(image_array)).resize((28, 28))
    return result_image


# Recuperer les valeurs pixels d'une image et la classifier
def getImagePixel(path, etiquette):
    image = Image.open(path) #ouvrir l'image
    image = dropRowsWhiteImage(np.array(image)) #Effacer les parties blanches de l'image
    pixels = list(image.getdata()) #Convertir l'image en liste
    pixels.append(etiquette) #ajouter l'etiquette dans la liste
    return pixels

# Lire une image 
def getImage(path):
    image = Image.open(path)
    return image

def loadModel(fileJoblib) :
    return load(fileJoblib)

def predictImage(image, modele):
    pixels = list(image.getdata())
    ready_data = improveData(np.array([pixels]))
    indice = modele.predict(ready_data)[0]
    significative = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '+', '-', '%', '[', ']', 'J']
    return significative[indice]
    

def dropWhiteLine(image_array):
    # Efface ligne horizontal blanc
    sums = np.sum(image_array, axis=1)
    indices = np.where(sums == 255 * image_array.shape[1])
    image_array = np.delete(image_array, indices, axis=0)

    return image_array

# Trouve les indices a partir du quelle on doit prendre l'image
def getSeparationIndice(indices):
    indices = indices[0] # Les elements sont tous dans un tableau
    result = []
    for i in range(1, len(indices)):
        if (indices[i] - indices[i-1]) != 1:
            result.append([indices[i - 1], indices[i]])
    return result
    
# Preparer image de sortie pour la prédiction
def prepareResultImage(image):
    # Efface ligne horizontal blanc
    image_array = np.array(image)
    sums = np.sum(image_array, axis=1)
    maxVal = np.max(sums)
    indices = np.where(sums == maxVal)
    image_array = np.delete(image_array, indices, axis=0)
    
    image = (Image.fromarray(image_array)).resize((28, 28))
    
    image_array = np.array(image)
    
    image_array = np.where(image_array < 200, 0, image_array)
    image_array = np.where(image_array >= 200, 255, image_array)

    return (Image.fromarray(image_array))

# Meilleur format d'image : 500 largeur et 100 hauteur
# Fonction pour découper une image en plusieur image
def cutImageIntoArray(image):
    image = Image.open(image)
    resized_image = ((image.resize((500, 100))).convert('L'))
    image_array = np.array(resized_image)
    image_array = dropWhiteLine(image_array)   # Efface ligne blanc    
    
    # Encadrement nouvelle image
    sums = np.sum(image_array, axis = 0)
    maxi = sums.max()
    indices = np.where(sums == maxi)
    separation = getSeparationIndice(indices)  # Indices de separation des images
    list_image = []  # Tableau des images séparés
    for limit in separation:
        temp_image = Image.fromarray(image_array[:, limit[0]:limit[1]])
        list_image.append(prepareResultImage(temp_image))
    return list_image

# Dessiner une image
def dessinerImage(image):
    plt.imshow(image)
    
    # Tous les améliorations de données
def improveData(data):
    # Enlever les bruits et normalisation
    data = np.where(data < 200, 0, data)
    data = np.where(data >= 200, 1, data)
    
    return data

image_list = cutImageIntoArray("image/file.png")
indice = 0
modele = loadModel('model_saved1.joblib')
expre = ''
#prediction = modelLoad.predict([imagePredire])
#print("taille = "+str(len(image_list)))
for i in range(len(image_list)) :
    expre = expre+" "+str(predictImage(image_list[i], modele))


if '%' in expre:
    expre[len(expre-1)] = "="
    print("L'expression = "+expre)
    #Traitement d'une equation
    print("Je suis equation")
    
elif '- -' in expre or '+ +' in expre:
    #Traitement d'une inequation
    print("Je suis inequation")
    
else :
    #Traitement d'un calcul arithmetique
    print("Je suis calcul arithmetique")

print(expre)