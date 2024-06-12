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


class Equation :
    def __init__(self,expression1, expression2) :
        self.expression1 = expression1
        self.expression2 = expression2
        self.inconnu = None
    
#Chercher l'inconnue dans la premiere expression
    def findInconnue(self, exp1) :
        for i in range(len(exp1)) :
            if(exp1[i] == "x") :
                return i
        return None
    
#Avoir l'oppose d'un operateur
    def opposeOperateur(self, operateur) :
        if(operateur == "+") :
            return "-"
        elif(operateur == "-") :
            return "+"
        elif(operateur == "*") :
            return "/"
        elif(operateur == "/") :
            return "*"
        
        return None
    
#Transfert d'un nombre vers la 2e expression
    def extraitInconnueAndCoeff(self) :
        indexInconnue = self.findInconnue(self.expression1)
        self.expression1 = self.expression1[indexInconnue-1]+""+self.expression1[indexInconnue]
    
#Deplacer le constant dans l'autre expression
    def transfert(self, nombre) :
        self.expression2 = str(self.expression2)+""+str(nombre)
                
#calculer l'expression 2
    def calculExpression2(self) :
        npi = algoShuntingYard(self.expression2)
        return calculPolonaise(npi)
    
#Extraction du coefficient de l:inconnu
    def extrayeCoeff(self) :
        indexInconnu = self.findInconnue(self.expression1)
        coeff = self.expression1[indexInconnu-1]
        self.expression1 = self.expression1[indexInconnu]
        
        return coeff
    
#Resolution de l'equation et retourner la solution
    def resolution(self) :
        indexInconnu = self.findInconnue(self.expression1) #Trouver l'inconnue
        self.inconnu = self.expression1[indexInconnu] #L'inconnu
        signeOppose = self.opposeOperateur(self.expression1[indexInconnu+1]) #Trouver le signe oppose du nombre constant
        constantToDeplace = str(signeOppose)+""+self.expression1[indexInconnu+2] #Le constant a deplacer
        constantToDeplace = " "+constantToDeplace[0]+" "+constantToDeplace[1] #Preparation du constant a deplacer
        #deplacer le nombre constant dans l'expression2
        self.transfert(constantToDeplace)
        self.extraitInconnueAndCoeff()
        valueExpression2 = self.calculExpression2() #Calculer l'expression 2
        self.expression2 = valueExpression2
        coeff = self.extrayeCoeff() #Extrayer le coefficient de l'inconnu
        
        #Trouver la valeur de l'inconnue
        expr2 = str(self.expression2)+"/"+coeff
        self.expression2 = expr2
        valueInconnu = eval(self.expression2)

        return str(self.inconnu)+" = "+str(valueInconnu)


eq = sys.argv[1]  # Récupère le premier argument passé en ligne de commande

equation = eq
expressions = equation.split("=")
equation = Equation(expressions[0], expressions[1])
print(equation.resolution())