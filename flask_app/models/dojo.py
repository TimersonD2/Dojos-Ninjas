# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ninja
# model the class after the friend table from our database

class Dojo:
    def __init__( self , data ):
        self.id = data['id']
        self.dojo_name = data['dojo_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []

    # Class methods for querying database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query)
        # Create an empty list to append our instances of users
        dojos = []
        # Iterate over the db results and create instances of dojos with cls.
        for dojo in results:
            dojos.append( cls(dojo) )
        return dojos

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM dojos where dojos.id=%(id)s;"
        results = connectToMySQL('dojos_and_ninjas_schema').query_db(query, data)

        if len(results) < 1:
            return False

        print('Get One Query', results[0])
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO dojos ( dojo_name , created_at, updated_at ) VALUES ( %(dojoname)s , NOW() , NOW() );"
        return connectToMySQL('dojos_and_ninjas_schema').query_db( query, data )   

    @classmethod
    def update(cls, data):
        query = "UPDATE dojos SET dojo_name=%(dojoname)s WHERE id=%(id)s"

        return connectToMySQL('dojos_and_ninjas_schema').query_db( query, data )   

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM dojos WHERE id=%(id)s"

        return connectToMySQL('dojos_and_ninjas_schema').query_db( query, data )   


    @classmethod
    def get_dojo_with_ninjas( cls , data ):
        query = "SELECT * FROM dojos LEFT JOIN ninjas ON ninjas.dojo_id = dojos.id WHERE dojos.id = %(id)s;"
        results = connectToMySQL('dojos_and_ninjas_schema').query_db( query , data )
        # results will be a list of dojos and associated ninjas 
        dojo = cls( results[0] )
        # print (results[0])
        for row in results:
            # Now we parse the ninja data to make instances of ninjas and add them into our list.
            ninja_data = {
                "id" : row["ninjas.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "age" : row["age"],
                "created_at" : row["ninjas.created_at"],
                "updated_at" : row["ninjas.updated_at"],
                "dojo_id" : row["dojo_id"]
            }
            print(ninja_data)
            dojo.ninjas.append( ninja.Ninja( ninja_data ) )

        print(results)
        return dojo

