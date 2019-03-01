#!/usr/bin/env python3

#=======================================================================================================================
# Imports
#=======================================================================================================================
from collections import OrderedDict
import datetime
import os
import sys

from peewee import *    # '*' will import everything from peewee (not best practice)

#=======================================================================================================================
# Create database
#=======================================================================================================================
db = SqliteDatabase('diary.db')


#=======================================================================================================================
# Create Model
#=======================================================================================================================
class Entry(Model):     #extends from Model which comes from peewee
    # content
    content = TextField()

    # timestamp
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

#=======================================================================================================================
# Initialize Everything
#=======================================================================================================================
def initialize():
    """Create the database and the table if they dont exist."""
    db.connect()
    db.create_tables([Entry], safe=True)

#=======================================================================================================================
# Clear Function
#=======================================================================================================================
def clear():
    # this will clear the screen so that you dont have to scroll instead will be on just the content
    os.system('cls' if os.name == 'nt' else 'clear')     # lets us call a program on the system

#=======================================================================================================================
# Menu loop
#=======================================================================================================================
def menu_loop():
    """Show the menu"""
    choice = None   # None is a pretty good and common way, of initializing a variable without giving it a value.

    while choice != 'q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():     #  menu.items gives us a tuple/ key,value in OrderedDict
            print('{} {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()      # back to menu, find the choice that is selected and run it

#=======================================================================================================================
# Create/Add
#=======================================================================================================================
def add_entry():
    """Add an entries."""
    print("Enter your entry. Press CTRL+D when finished.")  # tells the user how to exit the program when finished
    data = sys.stdin.read().strip()     # capture the user input

    if data:        # need to make sure you got data from the user input
        if input('Save entry? [Yn] ').lower() != 'n':       # make sure they want to save
            Entry.create(content=data)      # create entry using the model
            print("Saved successfully!")

#=======================================================================================================================
# Read/View
#=======================================================================================================================
def view_entries(search_query=None):    # search_query, equals None, by default.
    """View previous entries."""
    entries = Entry.select().order_by(Entry.timestamp.desc())   # Grabs the entries to be looked at and do things with
    if search_query:    # a search query came in
        entries = entries.where(Entry.content.contains(search_query))   # getting everything out and ordered/filter

    for entry in entries:   # Once grabed, you can loop through them

        # %A-weekday/Wednesday, %B-Month/January, %d-number/22, %Y-year/2019, %I-hour/12hour clock, %M-minutes, %p-am/pm
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')    # set timestamp before printing, make a string
        clear()
        print(timestamp)
        print('='*len(timestamp))   # If there's 15 characters in timestamp, print 15 equal sign
        print(entry.content)
        print('\n\n'+'='*len(timestamp))    # 2 new lines
        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = input('Action: [Ndq] ').lower().strip()    # This will allow you to enter a input
        if next_action == 'q':  # If the input you entered is 'q' the for loop will break
            break
        elif next_action == 'd':    # if the input you entered is 'd' will delete the entry
            delete_entry(entry)     # call the function delete_entry to delete current entry

#=======================================================================================================================
# Search Entries
#=======================================================================================================================
def search_entries():
    """Search entries for a string/text"""
    view_entries(input('Search query: '))   # Call view_entries function with an input
    pass

#=======================================================================================================================
# Delete Entries
#=======================================================================================================================
def delete_entry(entry):
    """Delete an entry"""
    if input('Are you sure? [yN] ').lower() == 'y':
        entry.delete_instance()
        print("Entry deleted!")


#=======================================================================================================================
# Create Menu
#=======================================================================================================================
menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
])

#=======================================================================================================================
# This is how you will import this file
#=======================================================================================================================
if __name__ == '__main__':
    initialize()
    menu_loop()





#=======================================================================================================================
# New Terms
#=======================================================================================================================
# TextField() - a field that holds a blob of text of any size
# DateTimeField() - a field for holding a date and a time
# OrderedDict - a handy container from the collections module that works like a dict but maintains the order that keys
# are added
# .__doc__ - a magic variable that holds the docstring of a function, method, or class
# sys - a Python module that contains functionality for interacting with the system
# sys.stdin - a Python object that represents the standard input stream. In most cases, this will be the keyboard
# .where() - method that lets us filter our .select() results
# .contains() - method that specifies the input should be inside the specified field
# os - Python module that lets us integrate with the underlying OS
# os.name - attribute that holds a name for the style of OS
# os.system() - method to allow Python code to call OS-level programs
#=======================================================================================================================
# Terminal Notes
#=======================================================================================================================
# chmod +x diary.py ///// its changes 'python diary.py' being typed in the terminal to just '/.diary'
# /.diary