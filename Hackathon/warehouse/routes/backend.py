from warehouse.models.loginCollection import loginCollection
from warehouse.models.managerCollection import managerCollection
from warehouse.models.adminCollection import adminCollection
from warehouse.models.itemsCollection import itemsCollection
from warehouse.models.sectionCollection import sectionsCollection
import sys

class Backend:
    def __init__(self, db):
        self.adminCollection = adminCollection(db)
        self.managerCollection = managerCollection(db)
        self.loginCollection = loginCollection(db)
        self.itemsCollection = itemsCollection(db)
        self.sectionsCollection = sectionsCollection(db)

    '''
    Create a user account

    :param name, the name of the user for display purposes ie Matthew Schofield
    :param username, for authentication purposes
    :param hashedPassword, for authentication purposes
    :param accountType, to understand permissions of an account
    '''

    def createAccount(self, name, username, hashedPassword, accountType, sections):
        if accountType == "admin":
            ID = self.adminCollection.create(name)
        elif accountType == "manager":
            ID = self.managerCollection.create(name, sections)
            for section in sections:
                self.sectionsCollection.addManager(int(section), ID)
        else:
            # Error
            ID = -1
        return self.loginCollection.create(username, hashedPassword, ID)

    def deleteAccount(self, ID):
        ID = int(ID)
        if ID == 10000000:
            return 1
        else:
            self.loginCollection.delete(ID)
            if ID > 1000000 and ID < 2000000:
                return self.adminCollection.delete(ID)
            elif ID >= 20000000 and ID < 100000000:
                return self.managerCollection.delete(ID)


    def getName(self,ID):
        ID = int(ID)
        if ID >= 1000000 and ID < 2000000:
            return self.adminCollection.getName(ID)
        elif ID >= 2000000 and ID < 10000000:
            return self.managerCollection.getName(ID)


    def createItem(self, name, description):
        return self.itemsCollection.create(name, description)

    def createSection(self, name, managers):
        sId = self.sectionsCollection.create(name, managers)
        for manager in managers:
            self.managerCollection.addSection(manager, sId)
        return sId

    def getManagers(self):
        return self.managerCollection.getAll()

    def getManagerName(self, ID):
        return self.managerCollection.getName(ID)

    def getSections(self):
        return self.sectionsCollection.getAll()

    def getItems(self):
        return self.itemsCollection.getItems()

    def getSectName(self, id):
        return self.sectionsCollection.getName(id)

    def getSectManagers(self, id):
        return self.sectionsCollection.getManagers(id)

    def getSectItems(self, id):
        return self.sectionsCollection.getItems(id)

    def addItemToSect(self, id, itemId):
        return self.sectionsCollection.addItem(id, itemId)

    def getItemName(self, id):
        return self.itemsCollection.getName(id)

    def changeSectItem(self, sectID, itemID, change):
        return self.sectionsCollection.changeSectItem(sectID, itemID, change)