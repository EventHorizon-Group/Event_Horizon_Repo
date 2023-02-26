from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

DB = "event_schema"

class Event:
    def __init__(self,data):
        self.id = data['id']
        self.event_name = data['event_name']
        self.location = data['location']
        self.date = data['date']
        self.description = data['description']
        self.member_num = data['member_num']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.userself = None

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO 
                events 
                    (event_name, 
                    location, 
                    date, 
                    description, 
                    member_num, 
                    user_id) 
            VALUES 
                (%(event_name)s, 
                %(location)s,
                %(date)s,
                %(description)s, 
                %(member_num)s, 
                %(user_id)s);
            """
        results = connectToMySQL(DB).query_db(query,data)
        print (results)
        return results

    @classmethod
    def get_users_and_events(cls):
        query = "SELECT * FROM events JOIN users on users.id = events.user_id;"
        results = connectToMySQL(DB).query_db(query)
        print (results)
        all_events = []

        for pho in results:
            one_event = cls(pho)
            user_data ={
                'id':pho['users.id'], 
                'first_name':pho['first_name'],
                'last_name':pho['last_name'],
                'email':pho['email'],
                'password':None,
                'created_at': pho['users.created_at'],
                'updated_at':pho['users.updated_at']
            }
            user_obj = user.User(user_data)
            one_event.userself = user_obj
            all_events.append(one_event)
        return all_events

    @classmethod
    def destroy (cls, data):
        query = "DELETE FROM events WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
    

    @classmethod
    def get_event_with_users( cls, data ):
        query = """
            SELECT *
            FROM
                events
            LEFT JOIN
                events_users
            ON
                events_users.events_id = events.id
            LEFT JOIN
                users
            ON
                events_users.users_id = users.id
            WHERE
                events.id = %(id)s;
            """
        results = connectToMySQL(DB).query_db( query, data )
        event = cls (results [0])
        for result in results:
            one_user_data={
                'id':result[0]['users.id'],
                'first_name':result[0]['first_name'],
                'last_name':result[0]['last_name'],
                'email':result[0]['email'],
                'password': None,
                'created_at':result[0]['users.created_at'],
                'updated_at':result[0]['users.updated_at']
            }
            event.on_users.append( user.User( one_user_data ))
        return event
    
    @classmethod
    def get_description (cls, data):
        query = "SELECT * FROM events JOIN users on users.id = events.user_id WHERE events.id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)

        row = cls (result[0])

        one_user_data={
            'id':result[0]['users.id'],
            'first_name':result[0]['first_name'],
            'last_name':result[0]['last_name'],
            'email':result[0]['email'],
            'password': None,
            'created_at':result[0]['users.created_at'],
            'updated_at':result[0]['users.updated_at']
        }
        user_obj=user.User(one_user_data)
        row.userself = user_obj
        return row

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM events WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = """
            UPDATE 
                events 
            SET 
                event_name=%(event_name)s,
                location=%(location)s,
                date = %(date)s,
                description=%(description)s,
                member_num=%(member_num)s 
            WHERE 
                id = %(id)s;
            """
        return connectToMySQL(DB).query_db(query,data)


    @staticmethod
    def validate_register(tv):
        is_valid = True # we assume this is true

        if len(tv['event_name']) < 3:
            flash("Event Name must be at least 2 characters")
            is_valid= False

        if tv['location'] is None:
            flash("Event Location required")
            is_valid= False

        if tv['date'] is None:
            flash("Event Date required")
            is_valid= False    
                    
        if len(tv['description']) < 3:
            flash("Description must be at least 3 characters")
            is_valid= False

        if tv['member_num'] < 1:
            flash("Max Members need to be at least 1")
            is_valid= False

        return is_valid