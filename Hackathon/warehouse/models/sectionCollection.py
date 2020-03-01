import sys

class sectionsCollection:
    def __init__(self, db):
        self.collection = db.db.Sections
        self.curMaxID = self.collection.find_one(sort=[("ID", -1)])
        if self.curMaxID == None:
            self.curMaxID = 1000000-1
        else:
            self.curMaxID = self.curMaxID["ID"]

    def create(self, name, managers):
        self.curMaxID += 1
        self.collection.insert({
            "ID": self.curMaxID,
            "Name": name,
            "Managers": managers,
            "Items": []
        })
        return self.curMaxID

    def get(self, ID):
        return self.collection.find_one({"ID":ID})

    def getManagers(self, ID):
        return list(self.get(int(ID))["Managers"])

    def getName(self, ID):
        return self.get(int(ID))["Name"]

    def addManager(self, ID, managerID):
        self.collection.update({"ID":int(ID)},{"$push":{"Managers": managerID}})

    def getItems(self, ID):
        return list(self.get(int(ID))["Items"])

    def addItem(self, ID, itemID):
        self.collection.update({"ID":int(ID)}, {
            "$push":{
                "Items": {
                    "ID": itemID,
                    "Quantity": 0
                }
            }
        })
        return 0

    def getAll(self):
        return self.collection.find()

    def changeSectItem(self, sectID, itemID, change):
        self.collection.update({"ID":int(sectID), "Items.ID": int(itemID)},
                               {"$inc": {"Items.$.Quantity": int(change)}})
        return 0
