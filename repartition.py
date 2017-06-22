# OBJECTIVE:
# Assign to each section in lecturesData a teacher in profsData, such that
# the total teaching duration for each teach' is between its max and min.
#
# Considered constraints are all related to total durations,
# thus lecturesData is structured around durations, and not sections,
# which are interchangeable within a given duration.
#
# Technically speaking, we wish to expand a map {Sections}->{Teachers}
# which is already partially defined by the teachers' wishes.


# Globals ----------------------------------------------------------------------
from copy import deepcopy as clone
from json import dumps
from functools import reduce

digits = 3

def printf(obj):
    """ Print JSON object sweetly """
    print(
        dumps(obj, indent = 4, separators=(",",": ") )
    )

def reround(x):
    if type(x) in [int, float]:
        return round(x, digits)
    return round(eval(x), digits)


# Sections data ----------------------------------------------------------------
lecturesDataRaw = [
    {
        "duration": "6.6+4/3*1.1",
        "sections": ["TS.1+AP", "TS.2+AP"]
    }, {
        "duration": "5.5",
        "sections": ["1S.+AP", "1S.SES+AP"]
    }, {
        "duration": "4.4+2/3*1.1",
        "sections": ["TES.2+AP"]
    }, {
        "duration": "5",
        "sections": ["2GT.1+AP", "2GT.2+AP", "2GT.3+AP",
                    "2GT.4+AP", "2GT.5+AP", "2GT.6+AP",
                    "SIO.1.1", "SIO.1.2", "SIO.2.1.UF2"]
    }, {
        "duration": "4.4+1/3*1.1",
        "sections": ["TES.1+AP"]
    }, {
        "duration": "3.3",
        "sections": ["1ES", "1ES.LES", "1ES.SES",
                    "1ST2S", "1STMG.1", "1STMG.2", "TST2S"]
    }, {
        "duration": "3",
        "sections": ["Prépa"]
    }, {
        "duration": "2.5",
        "sections": ["SIO.2.2.UF2"]
    }, {
        "duration": "2.2",
        "sections": ["TS.SpéM", "TSTMG.1", "TSTMG.2"]
    }, {
        "duration": "1.65",
        "sections": ["TES.SpéM"]
    }, {
        "duration": "1.5",
        "sections": ["2GT.MPS"]
    }, {
        "duration": "1.25",
        "sections": ["SIO.1.Algo1", "SIO.1.Algo2", "SIO.1.Algo3"]
    }, {
        "duration": "1.1",
        "sections": ["TS.ISN"]
    }, {
        "duration": "0.75",
        "sections": ["2GT.ICN"]
    }, {
        "duration": "0.55",
        "sections": ["1S.SES.TPE", "1S.TPE"]
    }
]

def getTag(sectionStr):
    """ Identify type of section from section identifier """
    # Currently unused (php inheritance)
    idx = sectionStr.find(".")
    if idx==-1:
        return sectionStr
    return sectionStr[:idx]

def setOfSections(lecturesData):
    """ Generates the set of sections from lecturesData """
    sections = {}
    for idx, lecture in enumerate(lecturesData):
        for section in lecture["sections"]:
            sections[section] = ""
    return sections

totalDueHours = 0
for idx, lecture in enumerate(lecturesDataRaw):
    duration = reround(lecture["duration"])
    totalDueHours += duration*len(lecture["sections"])
print("Due hours:", reround(totalDueHours), "h")


# Teachers data ----------------------------------------------------------------
profsDataRaw = {
    "CB":  {
        "min": 15, "max": 16,
        "wish": ["TS.1+AP"]
    },
    "MC":  {
        "min": 15, "max": 17,
        "wish": ["TS.2+AP"]
    },
    "CG":  {
        "min": 15, "max": 17,
        "wish": []
    },
    "NR":  {
        "min": 15, "max": 17,
        "wish": ["SIO.1.1"]
    },
    "SR":  {
        "min": 18, "max": 19,
        "wish": []
    },
    "JPR": {
        "min": 15, "max": 16,
        "wish": ["2nde.2+AP", "2nde.3+AP"]
    },
    "PV":  {
        "min": 15, "max": 17,
        "wish": ["SIO.1.2"]
    },
    "BMP": {
        "min": 18, "max": 19,
        "wish": []
    }
}

availableMin = 0
availableMax = 0
for prof in profsDataRaw:
    availableMin += profsDataRaw[prof]["min"]
    availableMax += profsDataRaw[prof]["max"]
print(
    "Total available services: from",reround(availableMin),"h",
    "to",reround(availableMax),"h"
)


# Update data from teachers' wishes --------------------------------------------
def findAndPop(lecturesData, section):
    """ looks for section in lecturesData, pops it out,
        and returns its duration """
    for idx, lecture in enumerate(lecturesData):
        if lecture["sections"].count(section):
            lecture["sections"].pop(
                lecture["sections"].index(section)
            )
            duration = reround(lecture["duration"])
            if not lecture["sections"]:
                lecturesData.pop(idx)
            return duration
    return 0

def updateData(profsDataRaw, lecturesDataRaw):
    """ Update data from teachers' wishes """
    profsData = clone(profsDataRaw)
    lecturesData = clone(lecturesDataRaw)
    for prof in profsDataRaw:
        if profsDataRaw[prof]["wish"]:
            for section in profsDataRaw[prof]["wish"]:
                durationOfThis = findAndPop(lecturesData, section)
                profsData[prof]["min"] = reround(
                    profsData[prof]["min"]-durationOfThis
                )
                profsData[prof]["max"] = reround(
                    profsData[prof]["max"]-durationOfThis
                )
    return [profsData, lecturesData]

data = updateData(profsDataRaw, lecturesDataRaw)
profsData = data[0]
lecturesData = data[1]

absolMax = 0
absolMin = 100
for prof in profsData:
    absolMax = max( absolMax, profsData[prof]["max"] )
    absolMin = min( absolMin, profsData[prof]["min"] )
print("Attribution Min:", absolMin, "h")
print("Attribution Max:", absolMax, "h")


# Compute possible partitions --------------------------------------------------
# A teacher's service may be viewed as a map:
# {durations} -> N
#  duration  |-> number of sections w/ this duration affected to this teacher
# The set {durations} is indexed by the lecturesData index,
# thus a teacher's service may be viewed as a map in coordinates: {indices of durations}->N
# Here we compute all such possible maps
class Coordinates:
    def __init__(self, maxCoords, weights):
        self.len = min(len(maxCoords), len(weights))
        self.maxCoords = maxCoords
        self.weights = weights
        self.coords = [0 for i in range(self.len)]
    def __str__(self):
        return str(self.coords)
    def weight(self):
        weight = 0
        for i in range(self.len):
            weight += self.coords[i]*self.weights[i]
        return reround(weight)
    def maxWeight(self, m=0):
        weight = 0
        for i in range(m, self.len):
            weight += self.maxCoords[i]*self.weights[i]
        return reround(weight)
    def downMax(self):
        i=0
        while(self.maxCoords[i]==0):
            i += 1
            if i==self.len:
                return False
        self.coords = [0 for x in range(self.len)]
        self.maxCoords[i] = 0
        return i+1
    def up(self):
        i = 0
        while(self.coords[i]==self.maxCoords[i]):
            self.coords[i] = 0
            i += 1
            if i==self.len:
                return False
        self.coords[i] += 1
        return True

# DEBUG
matchingPartitions = [
    # {
    # "coords":
    # "profs":
    # }
]

profsPartitions = {}
for prof in profsData:
    profsPartitions[prof] = []

maxCoordinates = [
    min( len(lecturesData[x]["sections"]), int(absolMax//eval(lecturesData[x]["duration"])) )
    for x in range(len(lecturesData))
]

weights = [ reround(lecturesData[x]["duration"]) for x in range(len(lecturesData)) ]
# /DEBUG

def computePossiblePartitions(
    matchingPartitions, profsPartitions, maxCoordinates, weights,
    profsData, lecturesData, absolMin, absolMax
    ):
    
    c = Coordinates(maxCoordinates, weights)
    idx = 0
    totalMatches = 0
    while(c.maxWeight(idx)>=absolMin):
        while c.up():
            weight = c.weight()
            if absolMin <= weight <= absolMax:
                partition = {
                    "coords": clone(c.coords),
                    "profs": []
                }
                for prof in profsData:
                    if profsData[prof]["min"] <= weight <= profsData[prof]["max"]:
                        partition["profs"] += [prof]
                        profsPartitions[prof] += [clone(c.coords)]
                        matchingPartitions += [clone(partition)]
                        totalMatches += 1
        idx = c.downMax()
        print("Done with idx =",idx-1)
        if not idx:
            break
    print("Found",totalMatches,"matches in total")
    for prof in profsData:
        print("   *",len(profsPartitions[prof]),"for",prof)
    print("")

computePossiblePartitions(
    matchingPartitions, profsPartitions, maxCoordinates, weights,
    profsData, lecturesData, absolMin, absolMax
)
