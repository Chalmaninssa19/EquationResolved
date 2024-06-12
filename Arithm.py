import sys

class Pile :
    def __init__(self) :
        self.item = []
        
#Ajouter un valeur dans la pile
    def add(self, item) :
        self.item.append(item)

#Suprrimer le denier element inserer du pile
    def delete(self) :
        self.item.pop(-1)
        
#Lecture du pile par le dernier element insere
    def read(self) :
        return self.item[-1]
    
#Est ce que la pile est vide
    def isEmpty(self) :
        if len(self.item) <= 0 :
            return True
        return False
    
#Initialisation de la pile
    def init(self) :
        self.item = []
    
#Algorithme de shunting yard: Convertir une expression algebrique en expression polonaise en eliminant les parentheses
def algoShuntingYard(expAlgebrique) :
    #Verifier la syntaxe de l'expression
    if(verifySyntaxe(expAlgebrique)) == False :
        return "Erreur syntaxe"
    
    expr = expAlgebrique.split(" ")
    pileOperateur = Pile()
    pileOperande = Pile()
    for item in expr :
        if item.isdigit() == True : #Si l'element est un nombre, on l'ajoute dans l'operande
            pileOperande.add(item)
        #Sinon si c'est un operateur, on procede a quelques etapes
        elif item == "+" or item == "-" or item == "*" or item == "/" or item == "//" or item == "(" or item == ")":
            #Assurer la priorite de la multiplication et division devant l'addition et soustraction dans l'expression sans parentheses
            if (len(pileOperateur.item) > 0) and (item == "+" or item == "-") and (pileOperateur.read() == "*" or pileOperateur.read() == "/" or pileOperateur.read() == "//"): 
                pileOperande.add(pileOperateur.read())
                pileOperateur.delete()
                pileOperateur.add(item)
                
            elif (item == ")") :#Si nous rencontrons une parenthese ferme
                while (pileOperateur.read() != "(") : #Tant que la parenthese ouvert n'est pas trouve
                    pileOperande.add(pileOperateur.read()) #On ajoute le dernier element dans la pile des operandes
                    pileOperateur.delete() #Et on le supprime de la pile des operateurs
                pileOperateur.delete() #On supprime la parenthese ouvert de la pile des operateurs
            
            else :
                pileOperateur.add(item)
 
    addOperateurInOperande(pileOperateur, pileOperande) #Transeferer les operateurs dans la pile de operandes
    
    return writerNpi(pileOperande)

#Calcul sur les expressions polonaises
def calculPolonaise(expPolonaise) :
    tab = expPolonaise.split(" ")
    pile = Pile()
    for item in tab :
        if item == "+" or item == "-" or item == "/" or item == "*" or item == "//":
            #Recuperer les deux derniers valeurs de notre pile
            firstMembre = pile.read()
            pile.delete()
            secondMembre = pile.read()
            pile.delete()
            value = str(secondMembre) + str(item) + str(firstMembre)
            pile.add(eval(value))
        else :
            pile.add(item)
    return pile.read()

#Verifier la syntaxe de l'expression algebrique
def verifySyntaxe(exprAlgr) :
    expr = exprAlgr.split(" ")
    countParenthese = 0
    for item in expr :
        if item == "(" or item == ")" : #Compter les nombres de parentheses dans l'expression
            countParenthese = countParenthese + 1
            
    if countParenthese%2 != 0 :
        return False
    return True

#Transferer les operateurs dans operandes
def addOperateurInOperande(pileOperateur, pileOperande) :
    while(len(pileOperateur.item) > 0) :
        pileOperande.add(pileOperateur.read())
        pileOperateur.delete()
        
#Ecriture en npi
def writerNpi(pileOperande) :
    npi = ""
    for item in pileOperande.item :
        npi = npi + " " + item
    return npi

eq = sys.argv[1]  
expr = eq
npi = algoShuntingYard(expr)

print("Resultat du calcul = " + str(calculPolonaise(npi)))