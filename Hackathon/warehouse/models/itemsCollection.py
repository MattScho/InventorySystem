
class itemsCollection:

    def __init__(self, db):
        self.collection = db.db.Items
        self.curMaxID = self.collection.find_one(sort=[("ID", -1)])
        if self.curMaxID == None:
            self.curMaxID = 1000000-1
        else:
            self.curMaxID = self.curMaxID["ID"]

    def create(self, name, description):
        self.curMaxID += 1
        self.collection.insert({
            "ID": self.curMaxID,
            "Name": name,
            "Description": description,
        })
        return self.curMaxID

    def getItems(self):
        return self.collection.find()

    def getName(self, ID):
        return self.collection.find_one({"ID": int(ID)})["Name"]
