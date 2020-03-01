class adminCollection:
    def __init__(self, db):
        self.collection = db.db.Admin
        self.curMaxID = self.collection.find_one(sort=[("ID", -1)])["ID"]

    def create(self, name):
        self.curMaxID += 1
        self.collection.insert({
            "ID": self.curMaxID,
            "Name": name,
        })
        return self.curMaxID

    def getName(self, ID):
        res = self.collection.find({"ID": ID})
        if res.count() == 1:
            information = res.next()
            return information["Name"]
        else:
            return 0

    def delete(self, ID):
        if self.collection.find({"ID": ID}):
            self.collection.remove({"ID": ID})
            return 0
        return 1
