# A cause que Python y passe les variab' par adresse:
from copy import deepcopy as clone
from json import dumps

def printf(obj):
    """ Print JSON object sweetly """
    print(
        dumps(obj, indent = 4, separators=(",",": ") )
    )

# Globales
digits = 3


# Données classes
dureesRaw = {
    "6.6+4/3*1.1":
        ["TS.1+AP", "TS.2+AP"],
    "5.5":
        ["1S.+AP", "1S.SES+AP"],
    "4.4+2/3*1.1":
        ["TES.2+AP"],
    "5":
        ["2nde.1+AP", "2nde.2+AP", "2nde.3+AP",
         "2nde.4+AP", "2nde.5+AP", "2nde.6+AP",
         "SIO.1.1", "SIO.1.2", "SIO.2.1.UF2" ],
    "4.4+1/3*1.1":
        ["TES.1+AP"],
    "3.3":
        ["1ES.LES", "1ES", "1ES.SES", "1ST2S",
         "1STMG.1", "1STMG.2", "TST2S"],
    "3":
        ["Prépa"],
    "2.5":
        ["SIO.2.2.UF2"],
    "2.2":
        ["TS.SpéM", "TSTMG.1", "TSTMG.2"],
    "1.65":
        ["TES.SpéM"],
    "1.5":
        ["MPS"],
    "1.25":
        ["SIO.1.Algo1", "SIO.1.Algo2", "SIO.1.Algo3"],
    "1.1":
        ["TS.ISN"],
    "0.75":
        ["ICN"],
    "0.55":
        ["1S.TPE", "1S.SES.TPE"]
}

def getTag(classStr):
    """ Identify type of class from class code """
    # Currently unused (php inheritance)
    idx = classStr.find(".")
    if idx==-1:
        return classStr
    return classStr[:idx]

def revertObj(obj):
    """ revert object {duration=>list_of_classes} to {classes=>duration} """
    revert = {}
    for key, list_of_values in obj.items():
        for value in list_of_values:
            revert[value] = eval(key)
    return revert
classes = revertObj(dureesRaw)

totalHeuresDues = 0
for key, list_of_values in dureesRaw.items():
    totalHeuresDues += eval(key)*len(list_of_values)
print("Heures Dues:", round(totalHeuresDues,digits), "h")


# Données profs
profsRaw = {
    "CB":  {
        "min": 15, "max": 16,
        "service": ["TS.1+AP"]
    },
    "MC":  {
        "min": 15, "max": 17,
        "service": ["TS.2+AP"]
    },
    "CG":  {
        "min": 15, "max": 17,
        "service": []
    },
    "NR":  {
        "min": 15, "max": 17,
        "service": ["SIO.1.1"]
    },
    "SR":  {
        "min": 18, "max": 19,
        "service": []
    },
    "JPR": {
        "min": 15, "max": 16,
        "service": ["2nde.2+AP", "2nde.3+AP"]
    },
    "PV":  {
        "min": 15, "max": 17,
        "service": ["SIO.1.2"]
    },
    "BMP": {
        "min": 18, "max": 19,
        "service": []
    }
}

minServices = 0
maxServices = 0
for prof in profsRaw:
    minServices += profsRaw[prof]["min"]
    maxServices += profsRaw[prof]["max"]
print(
    "Totaux services: entre",
    round(minServices, digits),"h",
    "et",
    round(maxServices, digits),"h"
)


# TODO
def popOut(durees, classe):
    # Pour être plus pythonique: remplacer le breakout par une fonction
    pass
# /TODO

def majDonnes(profsRaw, dureesRaw):
    profs = clone(profsRaw)
    durees = clone(dureesRaw)
    for prof in profsRaw:
        if profsRaw[prof]["service"]:
            for classe in profsRaw[prof]["service"]:
                breakOut = False
                for duree in durees:
                    if durees[duree].count(classe):
                        profs[prof]["min"] -= round(eval(duree),digits)
                        profs[prof]["max"] -= round(eval(duree),digits)
                        durees[duree].pop(durees[duree].index(classe))
                        if len(durees[duree])==0:
                            del durees[duree]
                        breakOut = True
                        break
                if breakOut:
                    break
    return [durees, profs]
data = majDonnes(profsRaw, dureesRaw)
durees = data[0]
profs = data[1]



absolMax = 0
absolMin = 100
for prof in profs:
    absolMax = max( absolMax, profs[prof]["max"] )
    absolMin = min( absolMin, profs[prof]["min"] )
print("Attribution Min:", absolMin, "h")
print("Attribution Max:", absolMax, "h")


# Calcul des combinaisons de durées
def qteDurees(durees):
    qtes = {}
    for duree in durees:
        qtes[duree] = len(durees[duree])
    return qtes

## TODO
class basicCombination:
    def __init__(self, combi, qte):
        self.combi = combi  # list of durations
        self.qte = qte

class Combination:
    def __init__(self, nbCombis, listeCombis, usedObj):
        self.nbCombis = nbCombis
        self.listeCombis = listeCombis  # list of basicCombination-s
        self.used = usedObj
## /TODO

def initCombis(durees):
    combis = {}
    for key in durees:
        str_key = str(round(eval(key),digits))
        combis[str_key] = {
            "listeCombis": [{
                "combi": [key],
                "qte": len(durees[key]),
            }],
            "nbCombis": len(durees[key]),
            "used": { str_key: 1 }
        }
    return combis

def combine(combis, durees, dureeMax):
    newCombis = {}
    for dureeCombi in combis:
        combi = combis[dureeCombi]  # Combination type
        for duree in durees:
            if hasattr(combi["used"], duree):
                if combi["used"][duree] >= len(durees[duree]):
                    print(combi["used"][duree],">=len(durees[",duree,"], skipping...")
                    continue
            dureeNewCombi = round(eval(dureeCombi)+eval(duree),digits)
            if dureeNewCombi > dureeMax:
                continue
            key = str(dureeNewCombi)
            if not hasattr(newCombis, key):
                newCombis[key] = {
                    "listeCombis": [],
                    "nbCombis": 0,
                    "used": {}
                }
            if not hasattr(newCombis[key]["used"], duree):
                newCombis[key]["used"][duree] = 0
            used = 0
            if hasattr(combi["used"], duree):
                used = combi["used"][duree]
            newCombis[key]["nbCombis"] += combi["nbCombis"]*(len(durees[duree])-used)
            for i in range(len(combi["listeCombis"])):
                newCombis[key]["listeCombis"] += [{
                    "combi": clone(combi["listeCombis"][i]["combi"]) + [duree],
                    "qte": combi["listeCombis"][i]["qte"]*(len(durees[duree])-used)
                }]
            newCombis[key]["used"][duree] += used+1
    return newCombis

def calculeCombinaisons(durees, dureeMax, n):
    combinaisons = [{} for i in range(n+1)]
    combinaisons[0] = initCombis(durees)
    print("Initializing with",len(combinaisons[0]),"durations")
    for i in range(n):
        combinaisons[i+1] = combine(combinaisons[i], durees, dureeMax)
        print(len(combinaisons[i+1]),"partitions of length",i+1,"found")
        if not combinaisons[i+1]:
            break
    return combinaisons

def unGrading(combinations):
    pass
        

combinaisons = calculeCombinaisons(durees, absolMax, 50)

