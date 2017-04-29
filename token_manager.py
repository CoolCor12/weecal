import sqlite3
import os


def create_db():
    # delete old db file if exists
    try:
        os.remove('tokens.sqlite')
    except:
        pass

    
    #create db
    db = sqlite3.connect("tokens.sqlite")
    cursor = db.cursor()

    # create table
    cursor.execute('''CREATE TABLE Tokens
                      (id VARCHAR(20) PRIMARY KEY, 
                      token VARCHAR(256))
                   ''')

    # commit changes
    db.commit()
    db.close()

def insert_token(token):
    db = sqlite3.connect("tokens.sqlite")
    cursor = db.cursor()
    
    # get last used id
    command = '''SELECT id
                 FROM Tokens
                 WHERE id = (SELECT MAX(id) FROM Tokens);'''
    cursor.execute(command)
    
    #set next id
    
    ID = cursor.fetchone()
    if ID == None:
        ID = 0
    else:
        ID = int(ID[0]) + 1
        
    # insert data
    command = "INSERT INTO Tokens VALUES (?, ?);"
    cursor.execute(command, [ID, token])

    # commit changes
    db.commit()
    db.close()
    
    return ID
    
def remove_token(ID):
    db = sqlite3.connect("tokens.sqlite")
    cursor = db.cursor()
    
    # remove from db
    command = "DELETE FROM Tokens WHERE id=?;"
    cursor.execute(command, [ID])

    # commit changes
    db.commit()
    db.close()
    

def display_db():
    db = sqlite3.connect("tokens.sqlite")
    cursor = db.cursor()
    
    # remove from db
    command = "SELECT * FROM Tokens;"
    cursor.execute(command)
    
    for row in cursor:
        print(row)
    
    # commit changes
    db.commit()
    db.close()

def test():
    create_db()
    insert_token(123412341234123)
    ID = insert_token(234234)
    remove_token(ID)
    insert_token(200)
    display_db()
    
test()