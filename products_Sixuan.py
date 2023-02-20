import shelve
from datetime import time, date, timedelta

class Slots:
    def __init__(self, d: str):
        self.date = d
        self.price = {"Adult": 10, "Concession": 6, "Child": 0}
        self.availability = {(time(10), time(10, 45)): 10,
                             (time(11), time(11, 45)): 10,
                             (time(14), time(14, 45)): 10,
                             (time(15), time(15, 45)): 10,
                             (time(16), time(16, 45)): 10}

    def getDate(self):
        return str(self.date)

    def setAdultPrice(self, adultPrice):
        self.price["Adult"] = int(adultPrice)

    def getAdultPrice(self):
        return self.price["Adult"]

    def setConcessionPrice(self, concessionPrice):
        self.price["Concession"] = int(concessionPrice)

    def getConcessionPrice(self):
        return self.price["Concession"]

    def setChildPrice(self, childPrice):
        self.price["Child"] = int(childPrice)

    def getChildPrice(self):
        return self.price["Child"]

    def decreaseAvailability(self, time: time):
        self.availability[time] -= 1

    def makeAllUnavailable(self):
        for i in range(len(self.availability)):
            self.setAvailability(i, 0)

    def makeAllAvailable(self):
        for i in range(len(self.availability)):
            self.setAvailability(i, 10)

    def setAvailability(self, slot:int, i):
        availability_list = list(self.availability)
        self.availability[availability_list[slot]] = i

    def getAvailability(self, slot):
        availability_list = list(self.availability.values())
        return availability_list[slot]



