from abc import ABC, abstractmethod
class User(ABC):
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class ViewingUser(User):
    def __init__(self, username, password, role):
        super().__init__(username, password, role)

class Admin(User):
    def __init__(self, username, password, role):
        super().__init__(username, password, role)

class UserFactory(ABC):
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    @abstractmethod
    def create_user(self):
        pass

class ViewingUserFactory(UserFactory):
    def create_user(self):
        return ViewingUser(self.username, self.password, self.role)

class AdminFactory(UserFactory):
    def create_user(self):
        return Admin(self.username, self.password, self.role)

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users_from_file()

    def add_user(self, user):
        self.users.append(user)

    def username_exists(self, username):
        for user in self.users:

            if user.username == username: 
                return True
            
        return False

    def load_users_from_file(self):
        try:
            with open("user_info.txt", "r") as file:

                for line in file:

                    if line.strip():
                        parts = line.strip().split(", ")

                        if len(parts) == 3:
                            username_part, password_part, role_part = parts
                            if username_part.startswith("Username: ") and password_part.startswith(
                                    "Password: ") and role_part.startswith("Role: "):
                                username = username_part.split(": ")[1]
                                password = password_part.split(": ")[1]
                                role = role_part.split(": ")[1]
                                factory = AdminFactory if role.lower() == 'admin' else ViewingUserFactory
                                user = factory(username, password, role).create_user()
                                self.add_user(user)

        except FileNotFoundError:
            pass
