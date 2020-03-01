'''
The User object is used by flask-login to ensure authentication
!Everytime a logged in user requests a page a new User object is created!
version: 11.5.2019
'''
from warehouse import db
from flask_login import UserMixin
from warehouse import Backend

class User(UserMixin):
    '''
    Creates a User object based on an identification that is either a string username or int ID
    Validation is to be done outside of this object and any initial data on login should aswell
    '''
    def __init__(self, identification):
        # Gets User from database
        if type(identification) is str:
            q = db.db.Logins.find({"userName": identification})
        elif type(identification) is int:
            q = db.db.Logins.find({"ID": identification})
        else:
            raise Exception()

        # Check if a User was found
        if q.count() == 0:
            # was not found
            self.id = -1
            self.password = ""
        else:
            # was found
            q = q.next()
            self.id = q["ID"]
            self.password = q["hashedPassword"]
            self.name = Backend.getName(self.id)
            self.attempts = q["attempts"]

    '''
    Getter for the ID of the User
    '''
    def getId(self):
        return self.id

    '''
    Checks if the user is an Admin
    ::return Boolean, Is a Admin
    '''
    def isAdmin(self):
        return self.id >= 1000000 and self.id < 2000000

    '''
    Checks if the user is a Manager
    ::return Boolean, Is a Manager
    '''
    def isManager(self):
        return self.id >= 2000000 and self.id < 9000000