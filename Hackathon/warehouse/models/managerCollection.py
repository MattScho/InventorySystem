
class managerCollection:
    def __init__(self, db):
        self.collection = db.db.Managers
        self.curMaxID = self.collection.find_one(sort=[("ID", -1)])

        if self.curMaxID == None:
            self.curMaxID = 2000000 - 1
        else:
            self.curMaxID = self.curMaxID["ID"]

    def create(self, name, sections):
        self.curMaxID += 1
        self.collection.insert({
            "ID": self.curMaxID,
            "Name": name,
            "Sections": sections
        })
        return self.curMaxID

    def getName(self, ID):
        res = self.collection.find({"ID": ID})
        if res.count() == 1:
            information = res.next()
            return information["Name"]
        else:
            return 0

    def getAll(self):
        res = self.collection.find()
        return res

    def delete(self, ID):
        if self.collection.find({"ID": ID}):
            self.collection.remove({"ID": ID})
            return 0
        return 1

    def addSection(self, ID, sId):
        self.collection.update({"ID":ID}, {"$push": {"Sections":sId}})
        return 0