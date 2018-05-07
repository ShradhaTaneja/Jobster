from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_email, user_type):
        self.user_email = user_email
        self.user_type = user_type

    def get(self):
        return {'user_email': self.user_email, 'user_type': self.user_type}

    def is_authenticated(self):
    	return True

    def is_active(self):
    	return True

    def is_anonymous(self):
    	return False
