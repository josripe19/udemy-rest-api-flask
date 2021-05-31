import sqlite3


class UserModel:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __str__(self):
        return f"<User id: {self.id}, username: {self.username}>"

    @classmethod
    def find_by_username(cls, username):
        return cls.find_by_field(username, 'username')

    @classmethod
    def find_by_id(cls, _id):
        return cls.find_by_field(_id, 'id')

    @classmethod
    def find_by_field(cls, field, field_name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"SELECT * FROM users WHERE {field_name} = ?"
        result = cursor.execute(query, (field,))
        row = result.fetchone()
        user = cls(*row) if row else None

        connection.close()
        return user
