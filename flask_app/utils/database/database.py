import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    #Create and populate the tables
    def createTables(self, purge=False, data_path='flask_app/database/'):
        sql_path = os.path.join(data_path, 'create_tables/')

        # Establishes database connection
        cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            charset='utf8mb4'
        )
        cursor = cnx.cursor()

        try:
            if purge:
                # Drops existing tables if purge is True
                cursor.execute("DROP TABLE IF EXISTS skills")
                cursor.execute("DROP TABLE IF EXISTS experiences")
                cursor.execute("DROP TABLE IF EXISTS positions")
                cursor.execute("DROP TABLE IF EXISTS institutions")
                cursor.execute("DROP TABLE IF EXISTS feedback")
                cursor.execute("DROP TABLE IF EXISTS users")
                cnx.commit()  # Commit after dropping tables

            # Execute SQL scripts to create tables
            sql_files = ['institutions.sql', 'positions.sql', 'experiences.sql', 'skills.sql', 'feedback.sql', 'users.sql']
            for sql_file in sql_files:
                sql_file_path = os.path.join(sql_path, sql_file)
                if os.path.exists(sql_file_path):
                    with open(sql_file_path, 'r') as f:
                        sql_commands = f.read().split(';')
                        for command in sql_commands:
                            if command.strip():
                                cursor.execute(command)

            # Defines data for each table
            data = [
                ('institutions', ['inst_id', 'type', 'name', 'department', 'address', 'city', 'state', 'zip'],
                os.path.join(data_path, 'initial_data/institutions.csv')),
                ('positions', ['position_id', 'inst_id', 'title', 'responsibilities', 'start_date', 'end_date'],
                os.path.join(data_path, 'initial_data/positions.csv')),
                ('experiences', ['experience_id', 'position_id', 'name', 'description', 'hyperlink', 'start_date', 'end_date'],
                os.path.join(data_path, 'initial_data/experiences.csv')),
                ('skills', ['skill_id', 'experience_id', 'name', 'skill_level'],
                os.path.join(data_path, 'initial_data/skills.csv'))
            ]

            # Inserts data from each CSV into respective tables 
            for table, columns, data_file in data:
                rows = []
                with open(data_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        values = []
                        for col in columns:
                            value = row.get(col)
                            values.append(value if value != 'NULL' and value != '' else None)
                        rows.append(values)
                
                # Inserts rows into the table by using insertRows functions
                self.insertRows(table, columns, rows)
            cnx.commit()
        finally:
            cursor.close()
            cnx.close()
            
    # inserts data into the database
    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        # establish database connection
        cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            charset='utf8mb4'
        )
        cursor = cnx.cursor()

        placeholders = ', '.join(['%s'] * len(columns))
        column_names = ', '.join(columns)
        
        query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
        cursor.executemany(query, parameters)

        cnx.commit()
        cursor.close()
        cnx.close()
        
    #Print out data for resume from tables and populated csv files
    def getResumeData(self):
        resume_data = {}
        cnx = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            charset='utf8mb4'
        )
        cursor = cnx.cursor(dictionary=True)

        try:
            # Retrieves institutions data
            cursor.execute("SELECT * FROM institutions")
            institutions = cursor.fetchall()
            print("Institutions:", institutions)  # Debug print

            for institution in institutions:
                inst_id = institution['inst_id']
                resume_data[inst_id] = {
                    'address': institution.get('address', 'NULL'),
                    'city': institution.get('city', 'NULL'),
                    'state': institution.get('state', 'NULL'),
                    'zip': institution.get('zip', 'NULL'),
                    'department': institution.get('department', 'NULL'),
                    'type': institution.get('type', 'NULL'),
                    'name': institution.get('name', 'NULL'),
                    'positions': {}
                }
                

                # Retrieve positions associated with the institution
                cursor.execute("SELECT * FROM positions WHERE inst_id = (%s)", (inst_id,))
                positions = cursor.fetchall()
                print(f"Positions for institution {inst_id}:", positions)  # Debug print
                #Beginning of nested for loop for dictionary
                for position in positions:
                    pos_id = position['position_id']
                    resume_data[inst_id]['positions'][pos_id] = {
                        'title': position.get('title', 'NULL'),
                        'responsibilities': position.get('responsibilities', 'NULL'),
                        'start_date': position.get('start_date', None),
                        'end_date': position.get('end_date', None),
                        'experiences': {}
                    }

                    # Retrieve experiences associated with the position
                    cursor.execute("SELECT * FROM experiences WHERE position_id = %s", (pos_id,))
                    experiences = cursor.fetchall()
                    print(f"Experiences for position {pos_id}:", experiences)  # Debug print

                    for experience in experiences:
                        exp_id = experience['experience_id']
                        resume_data[inst_id]['positions'][pos_id]['experiences'][exp_id] = {
                            'name': experience.get('name', 'NULL'),
                            'description': experience.get('description', 'NULL'),
                            'hyperlink': experience.get('hyperlink', None),
                            'start_date': experience.get('start_date', None),
                            'end_date': experience.get('end_date', None),
                            'skills': {}
                        }

                        # Retrieve skills associated with the experience
                        cursor.execute("SELECT * FROM skills WHERE experience_id = %s", (exp_id,))
                        skills = cursor.fetchall()
                        print(f"Skills for experience {exp_id}:", skills)  # Debug print

                        for skill in skills:
                            skill_id = skill['skill_id']
                            resume_data[inst_id]['positions'][pos_id]['experiences'][exp_id]['skills'][skill_id] = {
                                'name': skill.get('name', 'NULL'),
                                'skill_level': skill.get('skill_level', None)
                            }
        finally:
            cursor.close()
            cnx.close()

        print("Final Resume Data:", resume_data)  # Debuging test print final structure
        return resume_data
     #Inserts new feedback entry into the feedback table.
    def insertFeedback(self, name, email, comment):
        query = "INSERT INTO feedback (name, email, comment) VALUES (%s, %s, %s)"
        parameters = (name, email, comment)
        self.query(query, parameters)

 
    #Retrieves all feedback entries from the Feedback SQL table. 
    def getAllFeedback(self):
       
        query = "SELECT * FROM feedback"
        return self.query(query)
        
#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    #Creates a new user in the database
    def createUser(self, email='me@email.com', password='password', role='user'):
        query = "INSERT INTO users (role, email, password) VALUES (%s, %s, %s)"
        self.query(query, (role, email, self.onewayEncrypt(password)))
        return {'success': 1}
        
    #Authenticates a user in the database
    def authenticate(self, email='me@email.com', password='password'):
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        result = self.query(query, (email, password))
        if result:
            return {'success': 1}
        else:
            return {'success': 0}

    #Encrypts a string using scrypt
    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string
    
    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message


