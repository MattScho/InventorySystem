
class loginCollection(object):

    def __init__(self, db):
        self.collection = db.db.Logins

    '''
    0 - Successful insert
    1 - ID is not in range
    2 - User name already in collection
    '''
    def create(self, user_name, hashed_password, ID):
        if not (ID > 999999 and ID < 10000000):
            return 1
        if not self.collection.find_one({"userName": user_name}):
            self.collection.insert({
                "userName":user_name,
                "hashedPassword":hashed_password,
                "ID":ID,
                "attempts": 0
            })
            return 0
        return 2

    def delete(self, ID):
        if ID == 1000000:
            return 1
        if self.collection.find_one({"ID": ID}):
            self.collection.remove({"ID":ID})
            return 0
        return 2

    def updatePassword(self, ID, newPassword):
        self.collection.update({"ID" : ID}, {"$set" : {"hashedPassword" : newPassword}})

    def clearBlock(self, ID):
        if self.collection.find_one({"ID": int(ID)}):
            self.collection.update({"ID" : int(ID)}, {"$set" : {"attempts" : 0}})