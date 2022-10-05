# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database

class Ninja:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.dojo_id = data['dojo_id']

    # Class methods for querying database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM ninjas;"
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query)
        # Create an empty list to append our instances of users
        ninjas = []
        # Iterate over the db results and create instances of dojos with cls.
        for ninja in results:
            ninjas.append( cls(ninja) )
        return ninjas

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM ninjas where id=%(id)s;"
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query, data)

        if len(results) < 1:
            return False

        # print('Get One Query', results[0])
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO ninjas ( first_name , last_name, age, created_at, updated_at, dojo_id ) VALUES ( %(fname)s , %(lname)s, %(age)s, NOW() , NOW(), %(dojo_id)s );"
        return connectToMySQL('dojos_and_ninjas_schema').query_db( query, data )   

    @classmethod
    def update(cls, data):
        query = "UPDATE ninja SET first_name=%(fname)s, last_name=%(lname)s, age=%(age)s, dojo_id=%(dojo_id)s WHERE id=%(id)s"

        return connectToMySQL('dojos_and_ninjas_schema').query_db( query, data )   

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM ninjas WHERE id=%(id)s"

        return connectToMySQL('dojos_and_ninjas_schema').query_db( query, data )   

