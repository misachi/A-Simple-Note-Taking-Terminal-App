# Author: OMKAR PATHAK
from __future__ import print_function

import argparse
import time
import os
import os.path
from decouple import config

# Config
DB_TABLE = 'notes'
DATABASE = config('DATABASE')
DB_HOST = config('HOST')
DB_USER = config('USER')
# DB_PASSWORD = '8149omkar'
DB_PASSWORD = config('PASSWORD')
PORT = config('PORT')
DATABASE_TYPE = config('DATABASE_TYPE')  # valid values: 'mysql', 'sqlite'


def get_database_connection():
    # if DATABASE_TYPE in ['mysql', 'postgresql', 'sqlite']:
    #     try:
    #         if
    #     except ConnectionRefusedError:
    #         pass
    if DATABASE_TYPE == 'mysql':
        import pymysql
        return pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_TABLE)
    elif DATABASE_TYPE == 'postgresql':
        import psycopg2
        conn = psycopg2.connect(
            database=DATABASE,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=PORT
        )
        return conn

    elif DATABASE_TYPE == 'sqlite':
        import sqlite3
        sqlite_file = 'notes.db'
        file_exists = os.path.isfile(sqlite_file)
        conn = sqlite3.connect(sqlite_file)
        if not file_exists:
            create_sqlite_tables(conn)
        return conn
    else:
        raise Exception("Undefined database type!")


def create_sqlite_tables(conn):
    cursor = conn.cursor()
    with open('schema_sqlite.sql', 'r') as schema_file:
        cursor.executescript(schema_file.read())
    conn.commit()


def insert_into_db(note, tags):
    # Open database connection
    connection = get_database_connection()
    # prepare a cursor object using cursor() method
    cursor = connection.cursor()
    # Prepare SQL query to INSERT a record into the database.
    insertQuery = "INSERT INTO " + DB_TABLE + "(note, tags) VALUES ('" + note + "', '" + tags + "')"
    # insertQuery = 'INSERT INTO {0}(note, tags) VALUES ({1}, {2})'.format(DB_TABLE, note, tags)
    try:
        # Execute the SQL command
        cursor.execute(insertQuery)
        # Commit your changes in the database
        connection.commit()
        print('Successful inserted new note.')
    except:
        # Rollback in case there is any error
        connection.rollback()
    # disconnect from server
    connection.close()


def read_from_db():
    # Open database connection
    connect = get_database_connection()
    # prepare a cursor object using cursor() method
    cursor = connect.cursor()
    # Prepare SQL query to SELECT all records from the database.
    readQuery = 'SELECT * FROM ' + DB_TABLE
    try:
        # Execute the SQL command
        cursor.execute(readQuery)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()

        for row in results:
            ID = row[0]
            createdAt = row[1]
            modifiedAt = row[2]
            Note = row[3]
            Tag = row[4]

            print()
            print('ID:', ID)
            print('Created At:', createdAt)
            print('Last Modified At:', modifiedAt)
            print('Note:', Note)
            print('Tag:', Tag)
    except:
        print("Error: unable to fetch data")

    # disconnect from server
    connect.close()


def modify_data(idx, modifiedNote):
    # Open database connection
    connect = get_database_connection()
    # prepare a cursor object using cursor() method
    cursor = connect.cursor()
    # Prepare SQL query to UPDATE records from the database.
    updateQuery = 'UPDATE ' + DB_TABLE + ' SET note = "' + modifiedNote + '" WHERE id = ' + idx
    try:
        # Execute the SQL command
        cursor.execute(updateQuery)
        # Commit your changes in the database
        connect.commit()
        print('Successfully modified the note.')
    except:
        print("Error: unable to fetch data")
        # Rollback in case there is any error
        connect.rollback()

    # disconnect from server
    connect.close()


def delete_using_id(idx):
    # Open database connection
    connect = get_database_connection()
    # prepare a cursor object using cursor() method
    cursor = connect.cursor()
    # Prepare SQL query to UPDATE records from the database.
    deleteQuery = 'DELETE  FROM ' + DB_TABLE + ' WHERE id = ' + idx
    try:
        # Execute the SQL commands
        cursor.execute(deleteQuery)
        # Commit your changes in the database
        connect.commit()
        print('Successfully deleted the note.')
    except:
        print("Something went wrong try again")
        # Rollback in case there is any error
        connect.rollback()

    # disconnect from server
    connect.close()


def read_tags():
    # Open database connection
    connect = get_database_connection()
    # prepare a cursor object using cursor() method
    cursor = connect.cursor()
    # Prepare SQL query to SELECT all records from the database.
    readQuery = 'SELECT DISTINCT tags FROM ' + DB_TABLE
    try:
        # Execute the SQL command
        cursor.execute(readQuery)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        print('Tags:')
        for row in results:
            tags = row[0]
            print(tags)

    except:
        print("Error: unable to fetch data")

    # disconnect from server
    connect.close()


def update_tag(idx, modifiedTag):
    # Open database connection
    connect = get_database_connection()
    # prepare a cursor object using cursor() method
    cursor = connect.cursor()
    # Prepare SQL query to UPDATE records from the database.
    updateQuery = 'UPDATE ' + DB_TABLE + ' SET tags = "' + modifiedTag + '" WHERE id = ' + idx
    try:
        # Execute the SQL command
        cursor.execute(updateQuery)
        # Commit your changes in the database
        connect.commit()
        print('Successfully modified the note.')
    except:
        print("Error: unable to fetch data")
        # Rollback in case there is any error
        connect.rollback()

    # disconnect from server
    connect.close()


# function to set the reminder
def reminder(message, date):
    with open('/home/omkarpathak/Documents/GITs/A-Simple-Note-Taking-Terminal-App/Schedules.txt', 'a') as outFile:
        outFile.write(date + ' ' + message + '\n')
    print('Reminder set Successfully')


def read_clean():
    # Open database connection
    connect = get_database_connection()
    # prepare a cursor object using cursor() method
    cursor = connect.cursor()
    # Prepare SQL query to SELECT all records from the database.
    readQuery = 'SELECT * FROM ' + DB_TABLE
    try:
        # Execute the SQL command
        cursor.execute(readQuery)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in simple_generator(results):
            print(row)
    except:
        print("Error: unable to fetch data")

    # disconnect from server
    connect.close()


# function to generate a generator for seeing the notes
def simple_generator(numbers):
    i = 0
    while True:
        check = input('\nWanna see next note? (If yes, press y else n): ')
        if check in ('Y', 'y') and len(numbers) > i:
            os.system('clear')
            yield print_data(numbers[i])
            i += 1
        else:
            print('Done!')
            break


def print_data(row):
    print()
    print('ID:', row[0])
    print('Created At:', row[1])
    print('Last Modified At:', row[2])
    print('Note:', row[3])
    print('Tag:', row[4])
    return


def search_using_tags(pattern):
    # Open database connection
    connect = get_database_connection()
    # prepare a cursor object using cursor() method
    cursor = connect.cursor()
    # Prepare SQL query to SELECT all records from the database.
    searchNoteUsingTagQuery = 'SELECT * FROM ' + DB_TABLE + ' WHERE tags LIKE "%' + pattern + '%"'
    try:
        # Execute the SQL command
        cursor.execute(searchNoteUsingTagQuery)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        for row in results:
            ID = row[0]
            createdAt = row[1]
            modifiedAt = row[2]
            Note = row[3]
            Tag = row[4]

            print()
            print('ID:', ID)
            print('Created At:', createdAt)
            print('Last Modified At:', modifiedAt)
            print('Note:', Note)
            print('Tag:', Tag)
    except:
        print("Error: unable to fetch data")

    # disconnect from server
    connect.close()


def argumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add_note', nargs='*', help='Add notes to the database', action='store')
    parser.add_argument('-r', '--read_all', help='Fetch all Records from the database', action='store_true')
    parser.add_argument('-u', '--update', nargs='*', help='Update a record from the database', action='store')
    parser.add_argument('-d', '--delete', help='Delete a record from database', action='store')
    parser.add_argument('-rt', '--read_tags', help='Read all the available tags from database', action='store_true')
    parser.add_argument('-ut', '--update_tag', nargs='*', help='Update a tag of a record from the database',
                        action='store')
    parser.add_argument('--reminder', nargs='*', help='Set a reminder', action='store')
    parser.add_argument('-rc', '--read_clean', help='Fetch all Records one by one from the database',
                        action='store_true')
    parser.add_argument('-st', '--search_using_tags', help='Search notes based on tags', action='store')
    arg = parser.parse_args()

    if (arg.add_note):
        try:
            insert_into_db(arg.add_note[0], arg.add_note[1])
        except IndexError:
            print('You have to give two values [NOTE, TAGS]')

    elif (arg.read_all):
        read_from_db()

    elif (arg.update):
        try:
            modify_data(arg.update[0], arg.update[1])
        except:
            print('You have to give two values [ID, MODIFIED TEXT]')

    elif (arg.delete):
        delete_using_id(arg.delete)

    elif (arg.read_tags):
        read_tags()

    elif (arg.update_tag):
        try:
            update_tag(arg.update_tag[0], arg.update_tag[1])
        except:
            print('You have to give two values [ID, MODIFIED TAG]')

    elif (arg.reminder):
        try:
            reminder(arg.reminder[0], arg.reminder[1])
        except:
            print('You have to give two values [REMINDER TEXT, "DATE(dd-mm-yyyy) TIME(hh:ss)"]')

    elif (arg.read_clean):
        read_clean()

    elif (arg.search_using_tags):
        search_using_tags(arg.search_using_tags)

    else:
        print('Reading Data from Database..')
        read_from_db()


if __name__ == '__main__':
    argumentParser()
