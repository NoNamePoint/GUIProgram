import datetime 
import sqlite3 as db



class ExpancesDB():
    def __init__(self):
        self.__connection = db.connect('homeexpances.db')       
        self.cursor = self.__connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS homeexpances (id integer primary key autoincrement not null, 
                                                                        description text, 
                                                                        form text, 
                                                                        total real)""")
                                                                        
        self.__connection.commit()


    def insert_data(self, *fields):
        description, form, total = fields
        self.cursor.execute("""INSERT INTO homeexpances(description, form, total) VALUES (?, ?, ?) """,
                           (description, form, total))
        self.__connection.commit()

    def update(self, index, *fields):
        description, form, total = fields
        self.cursor.execute("""UPDATE homeexpances SET description=?, form=?, total=? WHERE ID=?""",
                                 (description, form, total, index))
        self.__connection.commit()

    def delete(self, index):
        self.cursor.execute("""DELETE FROM homeexpances WHERE ID=?""", (index))
        self.__connection.commit()

    def search(self, description):
        self.cursor.execute(
            '''SELECT * FROM homeexpances WHERE description LIKE ?''', (description,))
        self.__connection.commit()


    







        
