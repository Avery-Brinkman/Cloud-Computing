from User import User

class UserInfo:
    def __init__(self, user: User, firstName: str, lastName: str, email: str):
        self.user = user
        self.firstName = firstName
        self.lastName = lastName
        self.email = email