import sqlite3
from configparser import ConfigParser
from datetime import datetime

def initialize_db() -> None:
    """
    Initializes db and returns cursor object.
    """
    config = ConfigParser()
    config.read("config.ini")

    global connection
    global cursor
    connection = sqlite3.connect(str(config["DB"]["name"]))
    cursor = connection.cursor()

    notes_table = """
    CREATE TABLE IF NOT EXISTS
    notes(note_id INTEGER PRIMARY KEY AUTOINCREMENT, created timestamp NOT NULL, updated timestamp NOT NULL, note_name TEXT NOT NULL, note_text TEXT NOT NULL);
    """
    cursor.execute(notes_table)

    return cursor

def insert_new_note(note_name:str, note_text:str) -> None:
    """
    Insert new row to db.
    """
    command = """
    INSERT INTO notes('note_name', 'note_text', 'created', 'updated') VALUES(?, ?, ?, ?);
    """
    data_tuple = (note_name, note_text, datetime.now(), datetime.now())
    cursor.execute(command, data_tuple)
    connection.commit()

def all_notes() -> list:
    """
    Returns all notes in a list.
    """
    command = """
    SELECT * FROM notes
    """
    rows = cursor.execute(command).fetchall()
    return rows

def delete_note(note_id:int) -> None:
    """
    Deletes a note.
    """
    command = f"""
    DELETE from notes where note_id = {note_id}
    """
    cursor.execute(command)
    connection.commit()

def update_note(note_id:int, note_name:str, note_text:str) -> None:
    """
    Updates a note.
    """
    command = """
    UPDATE notes SET note_name = ?, note_text = ?, updated = ? WHERE note_id = ?
    """
    data_tuple = (note_name, note_text, datetime.now(), note_id)
    cursor.execute(command, data_tuple)
    connection.commit()

def close_db():
    """
    Exits db.
    """
    cursor.close()
    connection.close()

    if __name__ == "__main__":
        initialize_db()
