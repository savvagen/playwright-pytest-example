from faker import Faker
import json
fake = Faker(['en_US'])


class User(object):

    def __init__(self, email, password, username=None, bio=None, image=None, token=None, created_at=None,
                 updated_at=None):
        self.id = None
        self.username = username
        self.email = email
        self.password = password
        self.bio = bio
        self.image = image
        self.token = token
        self.createdAt = created_at
        self.updatedAt = updated_at

    def __str__(self):
        return json.dumps(self.__dict__)


def fake_user():
    username = f"{str(fake.first_name()).lower()}.{str(fake.last_name()).lower()}"
    password = f"{username}{fake.port_number()}"
    return User(username=username, email=f"{username}@gmail.com", password=password)
