##Introduction
This project is designed to provide a basic demonstration of designing and interacting with a PostgreSQL database through Python's psyopg2 API.

##Files
The following files are included:

+ tournament.sql
  - contains the SQL commands for creating the tables used for the project
+ tournament.py
  - contains functions for:
    + registering players
    + reporting match results
    + returning player standings
    + pairing players with opponents in Swiss pairing style
+ tournament_test.py
  - contains a series of unit tests for the methods implemented

##Running the code
In order to run the code, you will need to

+ install python 2.7
+ install vagrant
+ install virtualbox
+ clone this repository

Next, you will use vagrant to navigate to directory of these files on your local machine.  From there:

+ open psql and run the command ```create database tournament```
+ still in psql ```\c tournament```
+ still in psql ```\i tournament.sql```
+ ```\q``` to exit psql
+ python tournament_test.py

Following these steps should create a database called 'tournament' and populate it with the correct tables for tournament_test.py to execute its unit tests.